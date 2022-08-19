from django.db.models           import Q

from drf_yasg                   import openapi
from drf_yasg.utils             import swagger_auto_schema

from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated

from account_books.models       import AccountBookCategory
from account_books.serializers  import AccountBookCategorySerializer

from core.utils.decorator       import query_debugger


class AccountBookCategoryView(APIView):
    """
    Assignee: 김동규
    
    query string: search, sort, status, offset, limit
    request body: name
    return: json
    detail:
      - GET: 인증/인가에 통과한 유저는 본인의 카테고리 리스트 정보를 조회할 수 있습니다.
        > 부가기능
          * 카테고리 검색기능(카테고리 이름을 기준으로 검색 키워드 적용)
          * 정렬 기능(생성일자를 기준으로 정렬)
          * 카테고리 필터링 기능(사용중인/삭제된 카테고리를 기준으로 필터링)
          * 페이지네이션 기능(원하는 크기의 데이터 개수를 호출)
      - POST: 인증/인가에 통과한 유저는 카테고리를 생성할 수 있습니다.
        > 필수 입력값: name
    """
    
    permission_classes = [IsAuthenticated]
    
    search = openapi.Parameter('search', openapi.IN_QUERY, required=False, pattern='?search=', type=openapi.TYPE_STRING)
    sort   = openapi.Parameter('sort', openapi.IN_QUERY, required=False, pattern='?sort=', type=openapi.TYPE_STRING)
    status = openapi.Parameter('status', openapi.IN_QUERY, required=False, pattern='?status=', type=openapi.TYPE_STRING)
    offset = openapi.Parameter('offset', openapi.IN_QUERY, required=False, pattern='?offset=', type=openapi.TYPE_STRING)
    limit  = openapi.Parameter('limit', openapi.IN_QUERY, required=False, pattern='?limit=', type=openapi.TYPE_STRING)
    
    @query_debugger
    @swagger_auto_schema(responses={200: AccountBookCategorySerializer}, manual_parameters=[search, sort, status, offset, limit])
    def get(self, request):
        """
        GET: 가계부 카테고리 조회(리스트) 기능
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
            'out_of_date': 'created_at'
        }
        
        """
        Q 객체 활용:
          - 검색 기능(카테고리 이름을 기준으로 검색 필터링)
          - 필터링 기능(본인의 카테고리 필터링)
        """
        q = Q()
        
        if search:
            q |= Q(name__icontains=search)
            
        if user:
            q &= Q(user=user)
            
        categories = AccountBookCategory.objects\
                                        .select_related('user')\
                                        .filter(q)\
                                        .exclude(status__iexact=status)\
                                        .order_by(sort_set[sort])[offset:offset+limit]
        
        serializer = AccountBookCategorySerializer(categories, many=True)
        return Response(serializer.data, status=200)
    
    @swagger_auto_schema(request_body=AccountBookCategorySerializer, responses={201: AccountBookCategorySerializer})
    def post(self, request):
        """
        POST: 가계부 카테고리 생성 기능
        """
        user = request.user
        
        serializer = AccountBookCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)