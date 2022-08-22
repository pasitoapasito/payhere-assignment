import json

from datetime             import datetime
from rest_framework.test  import APITestCase, APIClient

from users.models         import User
from account_books.models import AccountBook, AccountBookCategory


class AccountBookLogCreateTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(1개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(9개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    2. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) query string/path param
            - book obj(path param: 필수 입력값)
              * 존재하는 가계부인지 확인
              * 본인의 가계부인지 확인
            - category obj(query string: 필수 입력값)
              * 존재하는 카테고리인지 확인
              * 본인의 카테고리인지 확인  
        3) request body
            - 필수 파라미터 확인(title/price)
            - 선택 파라미터 확인(types/description)
            - 파라미터 유효성 확인(price)
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/가계부/가계부 카테고리 정보)
    """
    
    @classmethod
    def setUpTestData(cls):
        cls.f_user = User.objects\
                         .create_user(
                             email    = 'user@example.com',
                             nickname = 'user',
                             password = 'userPassw0rd!'
                         )
                         
        cls.s_user = User.objects\
                         .create_user(
                             email    = 'test@example.com',
                             nickname = 'test',
                             password = 'testPassw0rd!'
                         )
                       
        cls.f_client = APIClient()
        cls.f_client.force_authenticate(user=cls.f_user)
        
        AccountBook.objects.create(
            id     = 1,
            user   = cls.f_user,
            name   = 'accountbook',
            budget = 100000,
            status = 'in_use'
        )
        
        AccountBook.objects.create(
            id     = 2,
            user   = cls.s_user,
            name   = 'accountbook',
            budget = 100000,
            status = 'in_use'
        )
        
        AccountBookCategory.objects.create(
            id     = 1,
            user   = cls.f_user,
            name   = 'category',
            status = 'in_use'
        )
        
        AccountBookCategory.objects.create(
            id     = 2,
            user   = cls.s_user,
            name   = 'category',
            status = 'in_use'
        )
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_create_account_book_log(self):
        data = {
            'title'      : 'log',
            'types'      : 'expenditure',
            'price'      : 10000,
            'description': '1st log'
        }
        
        response = self.f_client\
                       .post('/api/account-books/1/logs?category=1', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                'id'         : 1,
                'title'      : 'log',
                'types'      : 'expenditure',
                'price'      : '10000', 
                'description': '1st log',
                'status'     : 'in_use',
                'category'   : 'category',
                'book'       : 'accountbook',
                'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
            }
        )
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_create_account_book_log_due_to_unauthorized_user(self):
        data = {
            'title'      : 'log',
            'types'      : 'expenditure',
            'price'      : 10000,
            'description': '1st log'
        }
        
        response = self.client\
                       .post('/api/account-books/1/logs?category=1', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
    
    def test_fail_create_account_book_log_due_to_category_required(self):
        data = {
            'title'      : 'log',
            'types'      : 'expenditure',
            'price'      : 10000,
            'description': '1st log'
        }
        
        response = self.f_client\
                       .post('/api/account-books/1/logs', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 카테고리는 필수 입력값입니다.'
            }
        )
    
    def test_fail_create_account_book_log_due_to_not_existed_book(self):
        data = {
            'title'      : 'log',
            'types'      : 'expenditure',
            'price'      : 10000,
            'description': '1st log'
        }
        
        response = self.f_client\
                       .post('/api/account-books/10/logs?category=1', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 10(id)는 존재하지 않습니다.'
            }
        )
    
    def test_fail_create_account_book_log_due_to_not_own_book(self):
        data = {
            'title'      : 'log',
            'types'      : 'expenditure',
            'price'      : 10000,
            'description': '1st log'
        }
        
        response = self.f_client\
                       .post('/api/account-books/2/logs?category=1', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 가계부입니다.'
            }
        )
    
    def test_fail_create_account_book_log_due_to_not_existed_category(self):
        data = {
            'title'      : 'log',
            'types'      : 'expenditure',
            'price'      : 10000,
            'description': '1st log'
        }
        
        response = self.f_client\
                       .post('/api/account-books/1/logs?category=10', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 카테고리 10(id)는 존재하지 않습니다.'
            }
        )
    
    def test_fail_create_account_book_log_due_to_not_own_category(self):
        data = {
            'title'      : 'log',
            'types'      : 'expenditure',
            'price'      : 10000,
            'description': '1st log'
        }
        
        response = self.f_client\
                       .post('/api/account-books/1/logs?category=2', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 가계부 카테고리입니다.'
            }
        )
    
    def test_fail_create_account_book_log_due_to_title_required(self):
        data = {
            'types'      : 'expenditure',
            'price'      : 10000,
            'description': '1st log'
        }
        
        response = self.f_client\
                       .post('/api/account-books/1/logs?category=1', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'title': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_create_account_book_log_due_to_price_required(self):
        data = {
            'title'      : 'log',
            'types'      : 'expenditure',
            'description': '1st log'
        }
        
        response = self.f_client\
                       .post('/api/account-books/1/logs?category=1', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'price': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_create_account_book_log_due_to_invalid_price(self):
        data = {
            'title'      : 'log',
            'types'      : 'expenditure',
            'price'      : 'price',
            'description': '1st log'
        }
        
        response = self.f_client\
                       .post('/api/account-books/1/logs?category=1', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'price': [
                    '유효한 숫자를 넣어주세요.'
                ]
            }
        )