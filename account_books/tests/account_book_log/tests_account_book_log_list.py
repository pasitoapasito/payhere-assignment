from datetime             import datetime
from rest_framework.test  import APITestCase, APIClient

from users.models         import User
from account_books.models import AccountBook, AccountBookCategory, AccountBookLog


class AccountBookLogListTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(12개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(3개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    2. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) path param(필수 파라미터)
            - account_book_id
        3) query string(선택 파라미터: 다수의 조건을 동시적용 가능)
            - search
            - types
            - status
            - categories
              * 복수의 카테고리 선택 가능
            - sort
              * up_to_date : 최신순
              * out_of_date: 오래된순
              * high_price : 높은 가격순
              * low_price  : 낮은 가격순
            - offset/limit(default: 10개의 데이터 반환)
              * in data range: 데이터 범위 내(해당 개수의 데이터 반환)
              * out of data range: 데이터 범위 밖(0개의 데이터 반환)
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/가계부/가계부 카테고리/가계부 기록 정보)
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
        
        cls.f_book = AccountBook.objects\
                                .create(
                                    id     = 1,
                                    user   = cls.f_user,
                                    name   = 'accountbook',
                                    budget = 100000,
                                    status = 'in_use'
                                )
        
        cls.s_book = AccountBook.objects\
                                .create(
                                    id     = 2,
                                    user   = cls.s_user,
                                    name   = 'accountbook',
                                    budget = 200000,
                                    status = 'in_use'
                                )
        
        cls.f_category = AccountBookCategory.objects\
                                            .create(    
                                                id     = 1,
                                                user   = cls.f_user,
                                                name   = 'category',
                                                status = 'in_use'
                                            )
                                          
        cls.s_category = AccountBookCategory.objects\
                                            .create(
                                                id     = 2,
                                                user   = cls.f_user,
                                                name   = 'category2',
                                                status = 'deleted'
                                            )
        
        cls.t_category = AccountBookCategory.objects\
                                            .create(    
                                                id     = 3,
                                                user   = cls.f_user,
                                                name   = 'category3',
                                                status = 'in_use'
                                            )
                                            
        AccountBookLog.objects.create(
            id          = 1,
            book        = cls.f_book,
            category    = cls.f_category,
            title       = 'log',
            price       = 10000,
            description = '1st log',
            types       = 'expenditure',
            status      = 'in_use'
        )
        
        AccountBookLog.objects.create(
            id          = 2,
            book        = cls.f_book,
            category    = cls.t_category,
            title       = 'log2',
            price       = 20000,
            description = '2nd log',
            types       = 'expenditure',
            status      = 'in_use'
        )
        
        AccountBookLog.objects.create(
            id          = 3,
            book        = cls.f_book,
            category    = cls.s_category,
            title       = 'log3',
            price       = 30000,
            description = '3rd log',
            types       = 'expenditure',
            status      = 'in_use'
        )
        
        AccountBookLog.objects.create(
            id          = 4,
            book        = cls.f_book,
            category    = cls.f_category,
            title       = 'log4',
            price       = 40000,
            description = '4th log',
            types       = 'income',
            status      = 'in_use'
        )
        
        AccountBookLog.objects.create(
            id          = 5,
            book        = cls.f_book,
            category    = cls.f_category,
            title       = 'log5',
            price       = 50000,
            description = '5th log',
            types       = 'expenditure',
            status      = 'deleted'
        )
        
        AccountBookLog.objects.create(
            id          = 6,
            book        = cls.f_book,
            category    = cls.s_category,
            title       = 'log6',
            price       = 60000,
            description = '6th log',
            types       = 'income',
            status      = 'deleted'
        )
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_list_account_book_log_without_any_condition(self):
        response = self.f_client\
                       .get('/api/account-books/1/logs', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'user',
                'expected_budget'  : 100000.0,
                'total_income'     : 40000.0,
                'total_expenditure': 60000.0,
                'logs': [
                    {
                    'id'         : 4,
                    'title'      : 'log4',
                    'types'      : 'income',
                    'price'      : '40000',
                    'description': '4th log',
                    'status'     : 'in_use',
                    'category'   : 'category',
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 3,
                    'title'      : 'log3',
                    'types'      : 'expenditure',
                    'price'      : '30000',
                    'description': '3rd log',
                    'status'     : 'in_use',
                    'category'   : None,
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 2,
                    'title'      : 'log2',
                    'types'      : 'expenditure',
                    'price'      : '20000',
                    'description': '2nd log',
                    'status'     : 'in_use',
                    'category'   : 'category3',
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
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
                ]
            }  
        )
        
    def test_success_list_account_book_log_with_search_filtering(self):
        search   = 'log'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?search={search}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'user',
                'expected_budget'  : 100000.0,
                'total_income'     : 40000.0,
                'total_expenditure': 60000.0,
                'logs': [
                    {
                    'id'         : 4,
                    'title'      : 'log4',
                    'types'      : 'income',
                    'price'      : '40000',
                    'description': '4th log',
                    'status'     : 'in_use',
                    'category'   : 'category',
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 3,
                    'title'      : 'log3',
                    'types'      : 'expenditure',
                    'price'      : '30000',
                    'description': '3rd log',
                    'status'     : 'in_use',
                    'category'   : None,
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 2,
                    'title'      : 'log2',
                    'types'      : 'expenditure',
                    'price'      : '20000',
                    'description': '2nd log',
                    'status'     : 'in_use',
                    'category'   : 'category3',
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
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
                ]
            }  
        )
        
    def test_success_list_account_book_log_with_categories_filtering(self):
        categories = '1,3'
        response   = self.f_client\
                         .get(f'/api/account-books/1/logs?categories={categories}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'user',
                'expected_budget'  : 100000.0,
                'total_income'     : 40000.0,
                'total_expenditure': 30000.0,
                'logs': [
                    {
                    'id'         : 4,
                    'title'      : 'log4',
                    'types'      : 'income',
                    'price'      : '40000',
                    'description': '4th log',
                    'status'     : 'in_use',
                    'category'   : 'category',
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 2,
                    'title'      : 'log2',
                    'types'      : 'expenditure',
                    'price'      : '20000',
                    'description': '2nd log',
                    'status'     : 'in_use',
                    'category'   : 'category3',
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
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
                ]
            }  
        )
    
    def test_success_list_account_book_log_with_deleted_status_filtering(self):
        status   = 'in_use'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?status={status}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'user',
                'expected_budget'  : 100000.0,
                'total_income'     : 60000.0,
                'total_expenditure': 50000.0,
                'logs': [
                    {
                    'id'         : 6,
                    'title'      : 'log6',
                    'types'      : 'income',
                    'price'      : '60000',
                    'description': '6th log',
                    'status'     : 'deleted',
                    'category'   : None,
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 5,
                    'title'      : 'log5',
                    'types'      : 'expenditure',
                    'price'      : '50000',
                    'description': '5th log',
                    'status'     : 'deleted',
                    'category'   : 'category',
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    }
                ]
            }  
        )
    
    def test_success_list_account_book_log_with_income_type_filtering(self):
        types    = 'income'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?types={types}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'user',
                'expected_budget'  : 100000.0,
                'total_income'     : 40000.0,
                'total_expenditure': None,
                'logs': [
                    {
                    'id'         : 4,
                    'title'      : 'log4',
                    'types'      : 'income',
                    'price'      : '40000',
                    'description': '4th log',
                    'status'     : 'in_use',
                    'category'   : 'category',
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    }
                ]
            }  
        )
    
    def test_success_list_account_book_log_with_expenditure_type_filtering(self):
        types    = 'expenditure'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?types={types}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'user',
                'expected_budget'  : 100000.0,
                'total_income'     : None,
                'total_expenditure': 60000.0,
                'logs': [
                    {
                    'id'         : 3,
                    'title'      : 'log3',
                    'types'      : 'expenditure',
                    'price'      : '30000',
                    'description': '3rd log',
                    'status'     : 'in_use',
                    'category'   : None,
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 2,
                    'title'      : 'log2',
                    'types'      : 'expenditure',
                    'price'      : '20000',
                    'description': '2nd log',
                    'status'     : 'in_use',
                    'category'   : 'category3',
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
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
                ]
            }  
        )
    
    def test_success_list_account_book_log_with_up_to_date_sorting(self):
        sort     = 'up_to_date'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?sort={sort}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'user',
                'expected_budget'  : 100000.0,
                'total_income'     : 40000.0,
                'total_expenditure': 60000.0,
                'logs': [
                    {
                    'id'         : 4,
                    'title'      : 'log4',
                    'types'      : 'income',
                    'price'      : '40000',
                    'description': '4th log',
                    'status'     : 'in_use',
                    'category'   : 'category',
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 3,
                    'title'      : 'log3',
                    'types'      : 'expenditure',
                    'price'      : '30000',
                    'description': '3rd log',
                    'status'     : 'in_use',
                    'category'   : None,
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 2,
                    'title'      : 'log2',
                    'types'      : 'expenditure',
                    'price'      : '20000',
                    'description': '2nd log',
                    'status'     : 'in_use',
                    'category'   : 'category3',
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
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
                ]
            }  
        )
    
    def test_success_list_account_book_log_with_out_of_date_sorting(self):
        sort     = 'out_of_date'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?sort={sort}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'user',
                'expected_budget'  : 100000.0,
                'total_income'     : 40000.0,
                'total_expenditure': 60000.0,
                'logs': [
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
                    },
                    {
                    'id'         : 2,
                    'title'      : 'log2',
                    'types'      : 'expenditure',
                    'price'      : '20000',
                    'description': '2nd log',
                    'status'     : 'in_use',
                    'category'   : 'category3',
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 3,
                    'title'      : 'log3',
                    'types'      : 'expenditure',
                    'price'      : '30000',
                    'description': '3rd log',
                    'status'     : 'in_use',
                    'category'   : None,
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 4,
                    'title'      : 'log4',
                    'types'      : 'income',
                    'price'      : '40000',
                    'description': '4th log',
                    'status'     : 'in_use',
                    'category'   : 'category',
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    }
                ]
            }  
        )
    
    def test_success_list_account_book_log_with_high_price_sorting(self):
        sort     = 'high_price'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?sort={sort}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'user',
                'expected_budget'  : 100000.0,
                'total_income'     : 40000.0,
                'total_expenditure': 60000.0,
                'logs': [
                    {
                    'id'         : 4,
                    'title'      : 'log4',
                    'types'      : 'income',
                    'price'      : '40000',
                    'description': '4th log',
                    'status'     : 'in_use',
                    'category'   : 'category',
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 3,
                    'title'      : 'log3',
                    'types'      : 'expenditure',
                    'price'      : '30000',
                    'description': '3rd log',
                    'status'     : 'in_use',
                    'category'   : None,
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 2,
                    'title'      : 'log2',
                    'types'      : 'expenditure',
                    'price'      : '20000',
                    'description': '2nd log',
                    'status'     : 'in_use',
                    'category'   : 'category3',
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
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
                ]
            }  
        )
    
    def test_success_list_account_book_log_with_low_price_sorting(self):
        sort     = 'low_price'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?sort={sort}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'user',
                'expected_budget'  : 100000.0,
                'total_income'     : 40000.0,
                'total_expenditure': 60000.0,
                'logs': [
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
                    },
                    {
                    'id'         : 2,
                    'title'      : 'log2',
                    'types'      : 'expenditure',
                    'price'      : '20000',
                    'description': '2nd log',
                    'status'     : 'in_use',
                    'category'   : 'category3',
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 3,
                    'title'      : 'log3',
                    'types'      : 'expenditure',
                    'price'      : '30000',
                    'description': '3rd log',
                    'status'     : 'in_use',
                    'category'   : None,
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 4,
                    'title'      : 'log4',
                    'types'      : 'income',
                    'price'      : '40000',
                    'description': '4th log',
                    'status'     : 'in_use',
                    'category'   : 'category',
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    }
                ]
            }  
        )
    
    def test_success_list_account_book_log_with_offset_limit_in_data_range(self):
        offset   = '0'
        limit    = '2'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?offset={offset}&limit={limit}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'user',
                'expected_budget'  : 100000.0,
                'total_income'     : 40000.0,
                'total_expenditure': 60000.0,
                'logs': [
                    {
                    'id'         : 4,
                    'title'      : 'log4',
                    'types'      : 'income',
                    'price'      : '40000',
                    'description': '4th log',
                    'status'     : 'in_use',
                    'category'   : 'category',
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 3,
                    'title'      : 'log3',
                    'types'      : 'expenditure',
                    'price'      : '30000',
                    'description': '3rd log',
                    'status'     : 'in_use',
                    'category'   : None,
                    'book'       : 'accountbook',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'updated_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    }
                ]
            }  
        )
    
    def test_success_list_account_book_log_with_offset_limit_out_of_data_range(self):
        offset   = '10'
        limit    = '2'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?offset={offset}&limit={limit}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'user',
                'expected_budget'  : 100000.0,
                'total_income'     : 40000.0,
                'total_expenditure': 60000.0,
                'logs': []
            }  
        )
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_list_account_book_log_due_to_unauthorized_user(self):
        response = self.client\
                       .get('/api/account-books/1/logs', content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
    
    def test_fail_list_account_book_log_due_to_not_existed_book(self):
        response = self.f_client\
                       .get('/api/account-books/10/logs', content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 10(id)는 존재하지 않습니다.'
            }
        )
    
    def test_fail_list_account_book_log_due_to_not_own_book(self):
        response = self.f_client\
                       .get('/api/account-books/2/logs', content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 가계부입니다.'
            }
        )