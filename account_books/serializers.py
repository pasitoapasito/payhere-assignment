from typing                     import OrderedDict
from rest_framework             import serializers
from rest_framework.serializers import ModelSerializer

from account_books.models import AccountBook


class AccountBookSerializer(ModelSerializer):
    """
    Assignee: 김동규
    
    detail: 가계부 데이터 시리얼라이저[GET/POST 기능 유효성 검사]
    model: AccountBook
    """
    
    nickname = serializers.SerializerMethodField()
    
    def get_nickname(self, obj: AccountBook) -> str:
        return obj.user.nickname

    def create(self, validated_data: OrderedDict) -> object:
        book = AccountBook.objects\
                          .create(**validated_data)
        return book    
    
    class Meta:
        model  = AccountBook
        fields = [
            'id', 'nickname', 'name', 'budget', 'status'
        ]
        extra_kwargs = {
            'id'    : {'read_only': True},
            'status': {'read_only': True},
        }
        
        
class AccountBookDetailSerializer(ModelSerializer):
    """
    Assignee: 김동규
    
    detail: 가계부 데이터 시리얼라이저[PATCH 기능 유효성 검사]
    model: AccountBook
    """
    
    nickname = serializers.SerializerMethodField()
    
    def get_nickname(self, obj: AccountBook) -> str:
        return obj.user.nickname

    def update(self, instance: AccountBook, validated_data: OrderedDict) -> object:
        """
        가계부 이름/예산만 수정 가능
        """
        instance.name   = validated_data.get('name', instance.name)
        instance.budget = validated_data.get('budget', instance.budget)   
        
        instance.save()
        
        return instance 
    
    class Meta:
        model  = AccountBook
        fields = [
            'id', 'nickname', 'name', 'budget', 'status' 
        ]
        extra_kwargs = {
            'id'    : {'read_only': True},
            'status': {'read_only': True},
        }