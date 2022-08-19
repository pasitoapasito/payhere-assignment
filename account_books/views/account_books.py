from django.db.models           import Q

from drf_yasg                   import openapi
from drf_yasg.utils             import swagger_auto_schema

from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated

from account_books.models       import AccountBook
from account_books.serializers  import AccountBookSerializer

from core.utils.decorator       import query_debugger


class AccountBookView(APIView):
    """
    Assignee: 김동규
    
    query string: sort, search, status, offset, limit
    request body: name, budget
    return: json
    detail:
      - GET: 인증/인가에 통과한 유저는 본인의 가계부 리스트(조회) 정보를 호출할 수 있습니다.
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
        Q 객체를 활용하여 검색기능 및 필터링(본인의 가계부) 기능 구현 
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