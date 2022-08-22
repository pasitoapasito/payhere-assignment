from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import AllowAny

from drf_yasg.utils    import swagger_auto_schema

from users.serializers import UserSignUpSerializer


class UserSignUpView(APIView):
    """
    Assignee: 김동규
    
    request body: email, nickname, password
    return: json
    detail:
      - 유저 회원가입 기능입니다.
      - 이메일, 닉네임, 패스워드는 필수 입력값입니다.
      - 이메일과 패스워드는 정해진 형식에 맞아야 됩니다.
      - 이메일과 닉네임은 중복이 허용되지 않습니다.
    """
    
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=UserSignUpSerializer, responses={201: UserSignUpSerializer})
    def post(self, request):
        """
        POST: 유저 회원가입 기능
        """
        serializer = UserSignUpSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)