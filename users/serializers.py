import re

from rest_framework             import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSignUpSerializer(ModelSerializer):
    """
    Assignee: 김동규
    
    detail:
      - 유저 회원가입 시리얼라이저[POST 기능 유효성 검사]
      - 패스워드 정규식 표현을 기준으로 패스워드 형식 유효성 검사
      - 유저정보 중 패스워드는 해싱 후, DB에 저장
    model: User
    """
    
    def create(self, validated_data):
        password = validated_data.get('password')
        
        if not password:
            raise serializers.ValidationError({'detail': ['패스워드는 필수 입력값입니다.']})
        
        """
        패스워드 정규식표현(길이 8~20 자리, 최소 1개 이상의 소문자, 대문자, 숫자, (숫자키)특수문자로 구성)
        """
        password_regex = '^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,20}$'
        
        if not re.match(password_regex, password):
            raise serializers.ValidationError({'detail': ['올바른 비밀번호를 입력하세요.']})
        
        """
        유저정보 DB에 저장(패스워드 해싱)
        """
        user = User.objects\
                   .create_user(**validated_data)
        
        return user
        
    class Meta:
        model  = User
        fields = [
            'email', 'nickname', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }