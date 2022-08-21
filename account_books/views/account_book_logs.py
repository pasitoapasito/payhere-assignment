from django.db.models           import Q, Sum

from drf_yasg                   import openapi
from drf_yasg.utils             import swagger_auto_schema

from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated

from account_books.models       import AccountBookLog
from account_books.serializers  import AccountBookLogSerializer, AccountBookLogSchema

from core.utils.decorator           import query_debugger
from core.utils.get_obj_n_check_err import GetAccountBook, GetAccountBookCategory


class AccountBookLogView(APIView):
    """
    Assignee: 김동규
    
    query string: search, sort, types, status, categories, offset, limit
    path param: account_book_id
    request body: title, types, price, description
    return: json
    detail:
      - GET: 인증/인가에 통과한 유저는 본인의 가계부 기록 리스트 정보를 조회할 수 있습니다.
        > 부가기능
          * 가계부 기록 검색기능(가계부 기록 이름/설명/카테고리(복수 선택가능)를 기준으로 검색 키워드 적용)
          * 정렬 기능(생성일자, 가격을 기준으로 정렬)
          * 가계부 기록 필터링 기능(사용중인/삭제된 가계부 기록을 기준으로 필터링)
          * 페이지네이션 기능(원하는 크기의 데이터 개수를 호출)
      - POST: 인증/인가에 통과한 유저는 가계부 기록을 생성할 수 있습니다.
        > 필수 입력값: title, price, category(query string), book id(path param)
    """
    
    permission_classes = [IsAuthenticated]
    
    search     = openapi.Parameter('search', openapi.IN_QUERY, required=False, pattern='?search=', type=openapi.TYPE_STRING)
    sort       = openapi.Parameter('sort', openapi.IN_QUERY, required=False, pattern='?sort=', type=openapi.TYPE_STRING)
    types      = openapi.Parameter('types', openapi.IN_QUERY, required=False, pattern='?types=', type=openapi.TYPE_STRING)
    status     = openapi.Parameter('status', openapi.IN_QUERY, required=False, pattern='?status=', type=openapi.TYPE_STRING)
    categories = openapi.Parameter('categories', openapi.IN_QUERY, required=False, pattern='?categories=', type=openapi.TYPE_STRING)
    offset     = openapi.Parameter('offset', openapi.IN_QUERY, required=False, pattern='?offset=', type=openapi.TYPE_STRING)
    limit      = openapi.Parameter('limit', openapi.IN_QUERY, required=False, pattern='?limit=', type=openapi.TYPE_STRING)
    book_id    = openapi.Parameter('account_book_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @query_debugger
    @swagger_auto_schema(
        responses={200: AccountBookLogSchema}, manual_parameters=[search, sort, types, status, categories, offset, limit, book_id]
    ) 
    def get(self, request, account_book_id):
        """
        GET: 가계부 기록 조회(리스트) 기능
        """
        user = request.user
        
        search     = request.GET.get('search', None)
        sort       = request.GET.get('sort', 'up_to_date')
        types      = request.GET.get('types', None)
        status     = request.GET.get('status', 'deleted') 
        categories = request.GET.get('categories', None)
        offset     = int(request.GET.get('offset', 0))
        limit      = int(request.GET.get('limit', 10))
        
        """
        정렬 기준
        """ 
        sort_set = {
            'up_to_date' : '-created_at',
            'out_of_date': 'created_at',
            'high_price' : '-price',
            'low_price'  : 'price',    
        }
        
        """
        가계부 객체/유저정보 확인
        """
        book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        """
        Q 객체 활용:
          - 검색 기능(가계부 기록 제목/설명/카테고리를 기준으로 검색 필터링)
          - 필터링 기능(가계부 기록 카테고리/타입을 기준으로 필터링)
          - 필터링 기능(본인의 가계부 기록 필터링)
        """
        q = Q()
        
        if search:
            q |= Q(title__icontains = search)
            q |= Q(description__icontains = search)
            q |= Q(category__name__icontains = search)
        
        if account_book_id:
            q &= Q(book_id = book.id)
            
        if categories:
            categories_id = categories.split(',')
            
            q &= Q(category_id__in = categories_id)
            
        if types:
            q &= Q(types__iexact = types)
            
        logs = AccountBookLog.objects\
                             .select_related('category', 'book')\
                             .filter(q)\
                             .exclude(status__iexact=status)\
                             .order_by(sort_set[sort])
        """
        총수입/총지출 기록 산출
        """                      
        income      = logs.filter(types='income').aggregate(total=Sum('price'))
        expenditure = logs.filter(types='expenditure').aggregate(total=Sum('price'))
        
        """
        가계부 기록 최종 데이터(페이지네이션 기능 포함)
        """
        data = {
            'nickname'         : user.nickname,
            'expected_budget'  : book.budget,
            'total_income'     : income['total'],
            'total_expenditure': expenditure['total'],
            'logs'             : (AccountBookLogSerializer(logs, many=True).data)[offset:offset+limit]
        }
        return Response(data, status=200)
        
    category = openapi.Parameter('category', openapi.IN_QUERY, required=True, pattern='?category=', type=openapi.TYPE_STRING)
    book_id  = openapi.Parameter('account_book_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(
        request_body=AccountBookLogSerializer, responses={201: AccountBookLogSerializer},\
        manual_parameters=[book_id, category]
    )    
    def post(self, request, account_book_id):
        """
        POST: 가계부 기록 생성 기능
        """
        user = request.user
        
        """
        가계부 카테고리 정보(필수값)
        """
        account_book_category_id = request.GET.get('category', None)
        if not account_book_category_id:
            return Response({'detail': '가계부 카테고리는 필수 입력값입니다.'}, status=400)
        
        """
        가계부 객체/유저정보 확인
        """
        book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        """
        가계부 카테고리 객체/유저정보 확인
        """
        category, err = GetAccountBookCategory.get_category_n_check_error(account_book_category_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        serializer = AccountBookLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(book=book, category=category)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)   