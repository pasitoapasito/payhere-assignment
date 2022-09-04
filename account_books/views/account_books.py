from django.db.models           import Q

from drf_yasg                   import openapi
from drf_yasg.utils             import swagger_auto_schema

from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated

from account_books.models       import AccountBook
from account_books.serializers  import AccountBookSerializer, AccountBookDetailSerializer

from core.utils.decorator           import query_debugger
from core.utils.get_obj_n_check_err import GetAccountBook


class AccountBookView(APIView):
    """
    Assignee: 김동규
    
    query string: sort, search, status, offset, limit
    request body: name, budget
    return: json
    detail:
      - GET: 인증/인가에 통과한 유저는 본인의 가계부 리스트 정보를 조회할 수 있습니다.
        > 부가기능
          * 가계부 검색기능(가계부 이름을 기준으로 검색 키워드 적용)
          * 정렬 기능(생성일자, 예산을 기준으로 정렬)
          * 가계부 필터링 기능(사용중인/삭제된 가계부를 기준으로 필터링)
          * 페이지네이션 기능(원하는 크기의 데이터 개수를 호출)
      - POST: 인증/인가에 통과한 유저는 가계부를 생성할 수 있습니다.
        > 필수 입력값: name, budget
    """
    
    permission_classes = [IsAuthenticated]
    
    sort   = openapi.Parameter('sort', openapi.IN_QUERY, required=False, pattern='?sort=', type=openapi.TYPE_STRING)
    search = openapi.Parameter('search', openapi.IN_QUERY, required=False, pattern='?search=', type=openapi.TYPE_STRING)
    status = openapi.Parameter('status', openapi.IN_QUERY, required=False, pattern='?status=', type=openapi.TYPE_STRING)
    offset = openapi.Parameter('offset', openapi.IN_QUERY, required=False, pattern='?offset=', type=openapi.TYPE_STRING)
    limit  = openapi.Parameter('limit', openapi.IN_QUERY, required=False, pattern='?limit=', type=openapi.TYPE_STRING)
    
    @query_debugger
    @swagger_auto_schema(responses={200: AccountBookSerializer}, manual_parameters=[sort, search, status, offset, limit])
    def get(self, request):
        """
        GET: 가계부 조회(리스트) 기능
        """
        user = request.user
        
        search = request.GET.get('search', None)
        sort   = request.GET.get('sort', 'up_to_date')
        status = request.GET.get('status', 'deleted')
        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 10))
        
        """
        정렬 기준
        """ 
        sort_set = {
            'up_to_date' : '-created_at',
            'out_of_date': 'created_at',
            'high_budget': '-budget',
            'low_budget' : 'budget'
        }
        
        """
        Q 객체 활용:
          - 검색 기능(가계부 이름을 기준으로 검색 필터링)
          - 필터링 기능(본인의 가계부 필터링)
        """
        q = Q()
        
        if search:
            q |= Q(name__icontains=search)
            
        if user:
            q &= Q(user=user)
            
        books = AccountBook.objects\
                           .select_related('user')\
                           .filter(q)\
                           .exclude(status__iexact=status)\
                           .order_by(sort_set[sort])[offset:offset+limit]
        
        serializer = AccountBookSerializer(books, many=True)
        return Response(serializer.data, status=200)
    
    @swagger_auto_schema(request_body=AccountBookSerializer, responses={201: AccountBookSerializer})
    def post(self, request):
        """
        POST: 가계부 생성 기능
        """
        user = request.user

        serializer = AccountBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    
class AccountBookDetailView(APIView):
    """
    Assignee: 김동규
    
    path param: account_book_id
    return: json
    detail:
      - PATCH: 인증/인가에 통과한 유저는 본인의 가계부를 수정할 수 있습니다.
      - DELETE: 인증/인가에 통과한 유저는 본인의 가계부를 삭제할 수 있습니다.
    """
    
    permission_classes = [IsAuthenticated]
    
    book_id = openapi.Parameter('account_book_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(
        request_body=AccountBookDetailSerializer, responses={200: AccountBookDetailSerializer},\
        manual_parameters=[book_id]
    )
    def patch(self, request, account_book_id):
        """
        PATCH: 가계부 수정 기능
        """
        user = request.user
        
        """
        가계부 객체/유저정보 확인
        """
        book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        serializer = AccountBookDetailSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    book_id = openapi.Parameter('account_book_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(responses={204: '가계부가 삭제되었습니다.'}, manual_parameters=[book_id])
    def delete(self, request, account_book_id):
        """
        DELETE: 가계부 삭제 기능
        """
        user = request.user
        
        """
        가계부 객체/유저정보 확인
        """
        book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        if book.status == 'deleted':
            return Response({'detail': f'가계부 {account_book_id}(id)는 이미 삭제된 상태입니다.'}, status=400)
        
        book.status = 'deleted'
        book.save()
        
        return Response(status=204)
    
    
class AccountBookRestoreView(APIView):
    """
    Assignee: 김동규
    
    path param: account_book_id
    return: json
    detail: 
      - PATCH: 인증/인가에 통과한 유저는 본인의 삭제된 가계부를 복구할 수 있습니다.
    """
    
    permission_classes = [IsAuthenticated]
    
    book_id = openapi.Parameter('account_book_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(responses={204: '가계부가 복구되었습니다.'}, manual_parameters=[book_id])
    def patch(self, request, account_book_id):
        """
        PATCH: 가계부 복구 기능
        """
        user = request.user
        
        """
        가계부 객체/유저정보 확인
        """
        book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        if book.status == 'in_use':
            return Response({'detail': f'가계부 {account_book_id}(id)는 이미 사용중입니다.'}, status=400)
        
        book.status = 'in_use'
        book.save()
        
        return Response(status=204)