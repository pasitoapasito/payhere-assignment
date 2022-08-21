from typing                     import OrderedDict, Optional
from rest_framework             import serializers
from rest_framework.serializers import ModelSerializer

from account_books.models import AccountBook, AccountBookCategory, AccountBookLog


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
        

class AccountBookCategorySerializer(ModelSerializer):
    """
    Assignee: 김동규
    
    detail: 가계부 카테고리 데이터 시리얼라이저[GET/POST 기능 유효성 검사]
    model: AccountBookCategory
    """
    
    nickname = serializers.SerializerMethodField()
    
    def get_nickname(self, obj: AccountBookCategory) -> str:
        return obj.user.nickname
    
    def create(self, validated_data: OrderedDict) -> object:
        category = AccountBookCategory.objects\
                                      .create(**validated_data)
        return category
    
    class Meta:
        model  = AccountBookCategory
        fields = [
            'id', 'nickname', 'name', 'status'
        ]
        extra_kwargs = {
            'id'    : {'read_only': True},
            'status': {'read_only': True},
        }
        
        
class AccountBookCategoryDetailSerializer(ModelSerializer):
    """
    Assignee: 김동규
    
    detail: 가계부 카테고리 데이터 시리얼라이저[PATCH 기능 유효성 검사]
    model: AccountBookCategory
    """
    
    nickname = serializers.SerializerMethodField()
    
    def get_nickname(self, obj: AccountBookCategory) -> str:
        return obj.user.nickname
    
    def update(self, instance: AccountBookCategory, validated_data: OrderedDict) -> object:
        
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        
        return instance 
    
    class Meta:
        model  = AccountBookCategory
        fields = [
            'id', 'nickname', 'name', 'status'
        ]
        extra_kwargs = {
            'id'    : {'read_only': True},
            'status': {'read_only': True},
        }
        
        
class AccountBookLogSerializer(ModelSerializer):
    """
    Assignee: 김동규
    
    detail: 가계부 기록 데이터 시리얼라이저[GET/POST 기능 유효성 검사]
    model: AccountBookLog
    """
    
    category   = serializers.SerializerMethodField()
    book       = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    
    def get_category(self, obj: AccountBookLog) -> Optional[object]:
        if obj.category.status == 'deleted':
            category = None
        else:
            category = obj.category.name
        return category 
    
    def get_book(self, obj: AccountBookLog) -> str:
        return obj.book.name
    
    def get_created_at(self, obj: AccountBookLog) -> str:
        return (obj.created_at).strftime('%Y-%m-%d %H:%M')
    
    def get_updated_at(self, obj: AccountBookLog) -> str:
        return (obj.updated_at).strftime('%Y-%m-%d %H:%M')
    
    def create(self, validated_data: OrderedDict) -> object:
        log = AccountBookLog.objects\
                            .create(**validated_data)
        return log
    
    class Meta:
        model  = AccountBookLog
        fields = [
            'id', 'title', 'types', 'price', 'description', 'status',\
            'category', 'book', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'id'    : {'read_only': True},
            'status': {'read_only': True},
        }
        

class AccountBookLogSchema(serializers.Serializer):
    """
    Assignee: 김동규
    
    detail: 가계부 기록 스키마 시리얼라이저[only used for swagger]
    """

    nickname          = serializers.CharField(max_length=100)
    expected_budget   = serializers.DecimalField(max_digits=10, decimal_places=0)
    total_income      = serializers.DecimalField(max_digits=10, decimal_places=0)
    total_expenditure = serializers.DecimalField(max_digits=10, decimal_places=0)
    logs              = AccountBookLogSerializer(many=True)