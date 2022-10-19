import json

from rest_framework.test  import APITestCase, APIClient

from users.models import User


class AccountBookCreateTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(1개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(4개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    2. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) request body(name/budget)
            - 필수 파라미터 확인
            - 유효한 파라미터인지 확인
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
        
    def test_success_create_account_book(self):
        data = {
            'name'  : 'accountbook',
            'budget': 100000
        }
        
        response = self.f_client\
                       .post('/api/account-books', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                'id'      : 1,
                'nickname': 'user',
                'name'    : 'accountbook',
                'budget'  : '100000',
                'status'  : 'in_use'
            }
        )
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_create_account_book_due_to_unauthorized_user(self):        
        data = {
            'name': 'accountbook',
            'budget': 100000
        }
        
        response = self.client\
                       .post('/api/account-books', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
    
    def test_fail_create_account_book_due_to_name_required(self):
        data = {
            'budget': 100000
        }
        
        response = self.f_client\
                       .post('/api/account-books', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'name': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_create_account_book_due_to_budget_required(self):
        data = {
            'name': 'accountbook'
        }
        
        response = self.f_client\
                       .post('/api/account-books', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'budget': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_create_account_book_due_to_budget_type_mismatch(self):
        data = {
            'name'  : 'accountbook',
            'budget': 'budget'
        }
        
        response = self.f_client\
                       .post('/api/account-books', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'budget': [
                    '유효한 숫자를 넣어주세요.'
                ]
            }
        )