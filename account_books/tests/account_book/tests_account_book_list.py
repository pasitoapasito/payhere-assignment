from rest_framework.test  import APITestCase, APIClient

from account_books.models import AccountBook
from users.models         import User


class AccountBookListTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(9개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(1개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    2. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) query string(선택 파라미터)
            - search
              > 가계부 이름을 기준으로 검색 필터링 적용
            - status
              > 사용중인/삭제된 가계부를 기준으로 필터링 적용
                * in use account book
                * deleted account book
            - offset/limit
              > 페이지네이션 적용(default: 10개의 응답 데이터 반환)
                * in data range: 데이터 범위 내(해당 개수의 응답 데이터 반환)
                * out of data range: 데이터 범위 밖(0개의 응답 데이터 반환)
            - sorting
              > 생성일자/예산을 기준으로 정렬 적용
                * up_to_date : 최신순
                * out_of_date: 오래된순
                * high_budget: 높은 예산순
                * low_budget : 낮은 예산순
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/가계부 정보)
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
            user   = cls.f_user,
            name   = 'accountbook2',
            budget = 200000,
            status = 'in_use'
        )
        
        AccountBook.objects.create(
            id     = 3,
            user   = cls.f_user,
            name   = 'accountbook3',
            budget = 300000,
            status = 'deleted'
        )
        
        AccountBook.objects.create(
            id     = 4,
            user   = cls.f_user,
            name   = 'accountbook4',
            budget = 400000,
            status = 'in_use'
        )
        
        AccountBook.objects.create(
            id     = 5,
            user   = cls.f_user,
            name   = 'accountbook5',
            budget = 500000,
            status = 'deleted'
        )
        
        AccountBook.objects.create(
            id     = 6,
            user   = cls.s_user,
            name   = 'accountbook',
            budget = 100000,
            status = 'in_use'
        )
        
        AccountBook.objects.create(
            id     = 7,
            user   = cls.s_user,
            name   = 'accountbook2',
            budget = 200000,
            status = 'in_use'
        )
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_list_account_book_without_any_condition(self):
        response = self.f_client\
                       .get('/api/account-books', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 4,
                    'nickname': 'user',
                    'name'    : 'accountbook4',
                    'budget'  : '400000',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 2,
                    'nickname': 'user',
                    'name'    : 'accountbook2',
                    'budget'  : '200000',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 1,
                    'nickname': 'user',
                    'name'    : 'accountbook',
                    'budget'  : '100000',
                    'status'  : 'in_use'
                }
            ]
        )
        
    def test_success_list_account_book_with_search_filtering(self):
        search   = 'book'
        response = self.f_client\
                       .get(f'/api/account-books?search={search}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 4,
                    'nickname': 'user',
                    'name'    : 'accountbook4',
                    'budget'  : '400000',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 2,
                    'nickname': 'user',
                    'name'    : 'accountbook2',
                    'budget'  : '200000',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 1,
                    'nickname': 'user',
                    'name'    : 'accountbook',
                    'budget'  : '100000',
                    'status'  : 'in_use'
                }
            ]
        )
    
    def test_success_list_account_book_with_deleted_status_filtering(self):
        status   = 'in_use'
        response = self.f_client\
                       .get(f'/api/account-books?status={status}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 5,
                    'nickname': 'user',
                    'name'    : 'accountbook5',
                    'budget'  : '500000',
                    'status'  : 'deleted'
                },
                {
                    'id'      : 3,
                    'nickname': 'user',
                    'name'    : 'accountbook3',
                    'budget'  : '300000',
                    'status'  : 'deleted'
                }
            ]
        )
    
    def test_success_list_account_book_with_up_to_date_sorting(self):
        sort     = 'up_to_date'
        response = self.f_client\
                       .get(f'/api/account-books?sort={sort}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 4,
                    'nickname': 'user',
                    'name'    : 'accountbook4',
                    'budget'  : '400000',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 2,
                    'nickname': 'user',
                    'name'    : 'accountbook2',
                    'budget'  : '200000',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 1,
                    'nickname': 'user',
                    'name'    : 'accountbook',
                    'budget'  : '100000',
                    'status'  : 'in_use'
                }
            ]
        )
    
    def test_success_list_account_book_with_out_of_date_sorting(self):
        sort     = 'out_of_date'
        response = self.f_client\
                       .get(f'/api/account-books?sort={sort}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 1,
                    'nickname': 'user',
                    'name'    : 'accountbook',
                    'budget'  : '100000',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 2,
                    'nickname': 'user',
                    'name'    : 'accountbook2',
                    'budget'  : '200000',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 4,
                    'nickname': 'user',
                    'name'    : 'accountbook4',
                    'budget'  : '400000',
                    'status'  : 'in_use'
                }   
            ]
        )
    
    def test_success_list_account_book_with_high_budget_sorting(self):
        sort     = 'high_budget'
        response = self.f_client\
                       .get(f'/api/account-books?sort={sort}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 4,
                    'nickname': 'user',
                    'name'    : 'accountbook4',
                    'budget'  : '400000',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 2,
                    'nickname': 'user',
                    'name'    : 'accountbook2',
                    'budget'  : '200000',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 1,
                    'nickname': 'user',
                    'name'    : 'accountbook',
                    'budget'  : '100000',
                    'status'  : 'in_use'
                }
            ]
        )
    
    def test_success_list_account_book_with_low_budget_sorting(self):
        sort     = 'low_budget'
        response = self.f_client\
                       .get(f'/api/account-books?sort={sort}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 1,
                    'nickname': 'user',
                    'name'    : 'accountbook',
                    'budget'  : '100000',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 2,
                    'nickname': 'user',
                    'name'    : 'accountbook2',
                    'budget'  : '200000',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 4,
                    'nickname': 'user',
                    'name'    : 'accountbook4',
                    'budget'  : '400000',
                    'status'  : 'in_use'
                }   
            ]
        )
    
    def test_success_list_account_book_with_offset_limit_in_data_range(self):
        offset   = '0'
        limit    = '1'
        response = self.f_client\
                       .get(f'/api/account-books?offset={offset}&limit={limit}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 4,
                    'nickname': 'user',
                    'name'    : 'accountbook4',
                    'budget'  : '400000',
                    'status'  : 'in_use'
                }
            ]
        )
    
    def test_success_list_account_book_with_offset_limit_out_of_data_range(self):
        offset   = '10'
        limit    = '1'
        response = self.f_client\
                       .get(f'/api/account-books?offset={offset}&limit={limit}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_list_account_book_due_to_unauthorized_user(self):
        response = self.client\
                       .get('/api/account-books', content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )