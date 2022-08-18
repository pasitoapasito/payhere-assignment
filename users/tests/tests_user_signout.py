import json

from rest_framework.test             import APITestCase, APIClient
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken

from users.models import User


class UserSignOutTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(1개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(5개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    2. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) refresh token
            - 필수 파라미터 확인
            - 유효한 토큰인지 확인
            - 만료된 토큰인지 확인
            - 토큰 타입이 일치하는지 확인(액세스 토큰 사용불가)
            - 입력받은 refresh 토큰과 로그아웃으로 blacklist에 포함된 토큰이 일치하는지 확인
            - API 요청자의 유저정보와 리프레시 토큰의 유저정보가 일치하는지 확인
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저 회원가입/로그인/토큰 정보)
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
        """
        첫 번째 유저 로그인
        """                  
        f_data = {
            'email'   : 'user@example.com',
            'password': 'userPassw0rd!'
        }
        f_response = self.client\
                         .post('/api/users/signin', data=json.dumps(f_data), content_type='application/json')
        
        """
        두 번째 유저 로그인
        """               
        s_data = {
            'email'   : 'test@example.com',
            'password': 'testPassw0rd!'
        }
        s_response = self.client\
                         .post('/api/users/signin', data=json.dumps(s_data), content_type='application/json')
        
        """
        첫 번째 유저의 액세스/리프레시 토큰
        """
        self.f_access  = f_response.json()['access']
        self.f_refresh = OutstandingToken.objects\
                                         .get(token=f_response.json()['refresh'])
        
        """
        두 번째 유저의 리프레시 토큰
        """                                 
        self.s_refresh = OutstandingToken.objects\
                                         .get(token=s_response.json()['refresh'])
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.f_user)
    
    """
    테스트 데이터 삭제
    """
                                                
    def tearDown(self):
        User.objects.all().delete()
        OutstandingToken.objects.all().delete()
        BlacklistedToken.objects.all().delete()
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_user_signout(self):
        data = {
            'refesh_token': self.f_refresh.token
        }
        
        response = self.client\
                       .post('/api/users/signout', data=json.dumps(data), content_type='application/json')
                       
        blacklist_token = BlacklistedToken.objects\
                                          .get(token_id=self.f_refresh.id)
                                          
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.f_refresh.id, blacklist_token.token_id)
        self.assertEqual(
            response.json(),
            {
                'message': '유저 user이 로그아웃 되었습니다.'
            }
        )
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_user_signout_due_to_unauthorized_user(self):
        self.client = APIClient()
        
        data = {
            'refesh_token': self.f_refresh.token
        }
        
        response = self.client\
                       .post('/api/users/signout', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
    
    def test_fail_user_signout_due_to_refresh_token_required(self):
        data = {}
        
        response = self.client\
                       .post('/api/users/signout', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '유효하지 않거나 만료된 토큰입니다.'
            }
        )
        
    def test_fail_user_signout_due_to_refresh_token_mismatch(self):
        data = {
            'refesh_token': 'fake token'
        }
        
        response = self.client\
                       .post('/api/users/signout', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '유효하지 않거나 만료된 토큰입니다.'
            }
        )
    
    def test_fail_user_signout_due_to_token_type_mismatch(self):
        data = {
            'refesh_token': self.f_access
        }
        
        response = self.client\
                       .post('/api/users/signout', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '유효하지 않거나 만료된 토큰입니다.'
            }
        )
    
    def test_fail_user_signout_due_to_not_own_refresh_token(self):
        data = {
            'refesh_token': self.s_refresh.token
        }
        
        response = self.client\
                       .post('/api/users/signout', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '유저의 토큰정보가 유효하지 않습니다.'
            }
        )