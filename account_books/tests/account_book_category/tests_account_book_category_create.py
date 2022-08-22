import json

from rest_framework.test  import APITestCase, APIClient

from users.models import User


class AccountBookCategoryCreateTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(1개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(2개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    2. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) request body(name)
            - 필수 파라미터 확인
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저 정보)
    """
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects\
                       .create_user(
                           email    = 'user@example.com',
                           nickname = 'user',
                           password = 'userPassw0rd!'
                       )
                       
        cls.f_client = APIClient()
        cls.f_client.force_authenticate(user=cls.user)
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_create_account_book_category(self):
        data = {
            'name': 'category'
        }
        
        response = self.f_client\
                       .post('/api/account-books/categories', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                'id'      : 1,
                'nickname': 'user',
                'name'    : 'category',
                'status'  : 'in_use'
            }
        )
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_create_account_book_category_due_to_unauthorized_user(self):
        data = {
            'name': 'category',
        }
        
        response = self.client\
                       .post('/api/account-books/categories', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
    
    def test_fail_create_account_book_category_due_to_name_required(self):
        data = {}
        
        response = self.f_client\
                       .post('/api/account-books/categories', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'name': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )