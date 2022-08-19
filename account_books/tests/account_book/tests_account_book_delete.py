from rest_framework.test  import APITestCase, APIClient

from account_books.models import AccountBook
from users.models         import User


class AccountBookDeleteTest(APITestCase):
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
        2) book obj(path param)
            - 가계부 존재여부 확인(존재하지 않는 가계부는 삭제할 수 없음)
            - 가계부 유저정보 확인(다른 유저의 가계부는 삭제할 수 없음)
            - 가계부 상태정보 확인(이미 삭제된 가계부는 다시 삭제할 수 없음)
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/가계부 정보)
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
        
        AccountBook.objects.create(
            id     = 1,
            user   = self.f_user,
            name   = 'accountbook',
            budget = 100000,
            status = 'in_use'
        )
        
        AccountBook.objects.create(
            id     = 2,
            user   = self.s_user,
            name   = 'accountbook',
            budget = 100000,
            status = 'in_use'
        )
        
        AccountBook.objects.create(
            id     = 3,
            user   = self.f_user,
            name   = 'accountbook2',
            budget = 200000,
            status = 'deleted'
        )
    
    """
    테스트 데이터 삭제
    """ 
        
    def tearDown(self):
        User.objects.all().delete()
        AccountBook.objects.all().delete()
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_delete_account_book(self):
        response = self.client\
                       .delete('/api/account-books/1', content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 1(id)가 삭제되었습니다.'
            }
        )
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_delete_account_book_due_to_unauthorized_user(self):
        self.client = APIClient()
        
        response = self.client\
                       .delete('/api/account-books/1', content_type='application/json')
    
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
    
    def test_fail_delete_account_book_due_to_not_existed_book(self):
        response = self.client\
                       .delete('/api/account-books/10', content_type='application/json')
    
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 10(id)는 존재하지 않습니다.'
            }
        )
    
    def test_fail_delete_account_book_due_to_not_own_book(self):
        response = self.client\
                       .delete('/api/account-books/2', content_type='application/json')
    
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 가계부입니다.'
            }
        )
    
    def test_fail_delete_account_book_due_to_already_deleted_book(self):
        response = self.client\
                       .delete('/api/account-books/3', content_type='application/json')
    
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 3(id)는 이미 삭제된 상태입니다.'
            }
        )