import json

from datetime             import datetime
from rest_framework.test  import APITestCase, APIClient

from users.models         import User
from account_books.models import AccountBook, AccountBookCategory, AccountBookLog


class AccountBookLogUpdateTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(2개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(8개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    2. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) path param(필수 입력값)
            - book obj
              * 가계부 존재여부 확인(존재하지 않는 가계부는 수정할 수 없음)
              * 가계부 유저정보 확인(다른 유저의 가계부는 수정할 수 없음)
            - log obj
              * 가계부 기록 존재여부 확인(존재하지 않는 기록은 수정할 수 없음)
              * 가계부 기록 유저정보 확인(다른 유저의 기록은 수정할 수 없음)
              * 가계부 기록 유효성 확인(요청한 가계부의 기록인지 확인)
        3) query string(선택 입력값)
            - category obj
              * 카테고리 존재여부 확인(존재하지 않는 카테고리로 수정할 수 없음)
              * 카테고리 유저정보 확인(다른 유저의 카테고리로 수정할 수 없음)
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/가계부/가계부 카테고리/가계부 기록 정보)
    """
    
    def setUp(self):
        self.f_user = User.objects\
                          .create_user(
                              email    = 'user@example.com',
                              nickname = 'user',
                              password = 'userPassw0rd!'
                          )

        self.s_user = User.objects\
                          .create_user(
                              email    = 'test@example.com',
                              nickname = 'test',
                              password = 'testPassw0rd!'
                          )
                        
        self.client = APIClient()
        self.client.force_authenticate(user=self.f_user)
        
        self.f_book = AccountBook.objects\
                                 .create(
                                     id     = 1,
                                     user   = self.f_user,
                                     name   = 'accountbook',
                                     budget = 100000,
                                     status = 'in_use'
                                 )
        
        self.s_book = AccountBook.objects\
                                 .create(
                                     id     = 2,
                                     user   = self.s_user,
                                     name   = 'accountbook',
                                     budget = 200000,
                                     status = 'in_use'
                                 )
                                 
        self.t_book = AccountBook.objects\
                                 .create(
                                     id     = 3,
                                     user   = self.f_user,
                                     name   = 'accountbook2',
                                     budget = 200000,
                                     status = 'in_use'
                                 )
        
        self.f_category = AccountBookCategory.objects\
                                             .create(    
                                                 id     = 1,
                                                 user   = self.f_user,
                                                 name   = 'category',
                                                 status = 'in_use'
                                             )
                                          
        self.s_category = AccountBookCategory.objects\
                                             .create(
                                                 id     = 2,
                                                 user   = self.s_user,
                                                 name   = 'category',
                                                 status = 'in_use'
                                             )
                                             
        self.t_category = AccountBookCategory.objects\
                                             .create(    
                                                 id     = 3,
                                                 user   = self.f_user,
                                                 name   = 'category2',
                                                 status = 'in_use'
                                             )
                                             
        AccountBookLog.objects.create(
            id          = 1,
            book        = self.f_book,
            category    = self.f_category,
            title       = 'log',
            price       = 10000,
            description = '1st log',
            types       = 'expenditure',
            status      = 'in_use'
        )
        
        AccountBookLog.objects.create(
            id          = 2,
            book        = self.s_book,
            category    = self.s_category,
            title       = 'log',
            price       = 10000,
            description = '1st log',
            types       = 'expenditure',
            status      = 'in_use'
        )
        
        AccountBookLog.objects.create(
            id          = 3,
            book        = self.t_book,
            category    = self.f_category,
            title       = 'log',
            price       = 10000,
            description = '1st log',
            types       = 'income',
            status      = 'in_use'
        )            
    
    """
    테스트 데이터 삭제
    """
    
    def tearDown(self):
        User.objects.all()
        AccountBook.objects.all().delete()
        AccountBookCategory.objects.all().delete()
        AccountBookLog.objects.all().delete()
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_update_account_book_log_first_case(self):
        data = {
            'title'      : 'updatedlog',
            'types'      : 'income',
            'price'      : 100001,
            'description': '1st log'
        }

        response = self.client\
                       .patch('/api/account-books/1/logs/1', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'id'         : 1,
                'title'      : 'updatedlog',
                'types'      : 'income',
                'price'      : '100001',
                'description': '1st log',
                'status'     : 'in_use',
                'category'   : 'category',
                'book'       : 'accountbook',
                'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
            }
        )
    
    def test_success_update_account_book_log_second_case(self):
        data = {
            'types': 'expenditure',
            'price': 100001
        }

        category = '3'
        response = self.client\
                       .patch(f'/api/account-books/1/logs/1?category={category}', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'id'         : 1,
                'title'      : 'log',
                'types'      : 'expenditure',
                'price'      : '100001',
                'description': '1st log',
                'status'     : 'in_use',
                'category'   : 'category2',
                'book'       : 'accountbook',
                'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
            }
        )
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_update_account_book_log_due_to_unauthorized_user(self):
        self.client = APIClient()

        data = {
            'title'      : 'updatedlog',
            'types'      : 'income',
            'price'      : 100001,
            'description': '1st log'
        }

        response = self.client\
                       .patch('/api/account-books/1/logs/1', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
    
    def test_fail_update_account_book_log_due_to_not_existed_book(self):
        data = {
            'title'      : 'updatedlog',
            'types'      : 'income',
            'price'      : 100001,
            'description': '1st log'
        }

        response = self.client\
                       .patch('/api/account-books/10/logs/1', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 10(id)는 존재하지 않습니다.'
            }
        )
    
    def test_fail_update_account_book_log_due_to_not_own_book(self):
        data = {
            'title'      : 'updatedlog',
            'types'      : 'income',
            'price'      : 100001,
            'description': '1st log'
        }

        response = self.client\
                       .patch('/api/account-books/2/logs/1', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 가계부입니다.'
            }
        )
    
    def test_fail_update_account_book_log_due_to_not_existed_log(self):
        data = {
            'title'      : 'updatedlog',
            'types'      : 'income',
            'price'      : 100001,
            'description': '1st log'
        }

        response = self.client\
                       .patch('/api/account-books/1/logs/10', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 기록 10(id)는 존재하지 않습니다.'
            }
        )
    
    def test_fail_update_account_book_log_due_to_not_own_log(self):
        data = {
            'title'      : 'updatedlog',
            'types'      : 'income',
            'price'      : 100001,
            'description': '1st log'
        }

        response = self.client\
                       .patch('/api/account-books/1/logs/2', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 가계부 기록입니다.'
            }
        )
    
    def test_fail_update_account_book_log_due_to_not_included_log_in_requested_book(self):
        data = {
            'title'      : 'updatedlog',
            'types'      : 'income',
            'price'      : 100001,
            'description': '1st log'
        }

        response = self.client\
                       .patch('/api/account-books/1/logs/3', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '해당 기록은 가계부 1(id)의 기록이 아닙니다.'
            }
        )
    
    def test_fail_update_account_book_log_due_to_not_existed_category(self):
        data = {
            'title'      : 'updatedlog',
            'types'      : 'income',
            'price'      : 100001,
            'description': '1st log'
        }

        category = '10'
        response = self.client\
                       .patch(f'/api/account-books/1/logs/1?category={category}', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 카테고리 10(id)는 존재하지 않습니다.'
            }
        )
    
    def test_fail_update_account_book_log_due_to_not_own_category(self):
        data = {
            'title'      : 'updatedlog',
            'types'      : 'income',
            'price'      : 100001,
            'description': '1st log'
        }

        category = '2'
        response = self.client\
                       .patch(f'/api/account-books/1/logs/1?category={category}', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 가계부 카테고리입니다.'
            }
        )