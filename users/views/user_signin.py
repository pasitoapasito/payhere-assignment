from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import AllowAny

from drf_yasg.utils    import swagger_auto_schema

from users.serializers import UserSignInSerializer, UserSignInSchema


class UserSignInView(APIView):
    """
    Assignee: 김동규
    
    request body: email, password
    return: json
    detail:
      - 유저 로그인 기능입니다.
      - 이메일, 패스워드는 필수 입력값입니다.
      - 이메일 입력값이 유저정보와 일치하는지 확인합니다.
      - 패스워드 입력값이 유저정보와 일치하는지 확인합니다.
    """
    
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=UserSignInSerializer, responses={200: UserSignInSchema})
    def post(self, request):
        """
        POST: 유저 로그인 기능
        """
        serializer = UserSignInSerializer(data=request.data)
        
        if serializer.is_valid():
            token = serializer.validated_data
            return Response(token, status=200)
        return Response(serializer.errors, status=400)