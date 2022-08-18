import json

from rest_framework.test             import APITestCase
from rest_framework_simplejwt.tokens import OutstandingToken

from users.models import User


class UserRefreshTokenTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(1개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
              * API 응답 데이터에 access 토큰이 존재하는지 확인
              * API 응답 데이터에 refresh 토큰이 존재하는지 확인
        2) fail test case(4개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    3. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) refresh token
            - 필수 파라미터 확인
            - 유효한 토큰인지 확인
            - 만료된 토큰인지 확인
            - 토큰 타입이 일치하는지 확인(액세스 토큰 사용불가)
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저 회원가입/로그인/토큰 정보)
    """
    
    def setUp(self):
        self.user = User.objects\
                        .create_user(
                            email    = 'user@example.com',
                            nickname = 'user',
                            password = 'userPassw0rd!'
                        )
        """
        유저 로그인
        """                
        data = {
            'email'   : 'user@example.com',
            'password': 'userPassw0rd!'
        }
        response = self.client\
                       .post('/api/users/signin', data=json.dumps(data), content_type='application/json')
        
        """
        유저의 액세스/리프레시 토큰
        """
        self.access  = response.json()['access']
        self.refresh = OutstandingToken.objects\
                                       .get(token=response.json()['refresh'])\
                                       .token
    
    """
    테스트 데이터 삭제
    """
                                       
    def teatDown(self):
        User.objects.all().delete()
        OutstandingToken.objects.all().delete() 
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_user_refresh_token(self):
        data = {
            'refresh': self.refresh
        }
        
        response = self.client\
                       .post('/api/users/token/refresh', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
        self.assertNotIn('refresh', response.json())
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_user_refresh_token_due_to_refresh_token_required(self):
        data = {}
        
        response = self.client\
                       .post('/api/users/token/refresh', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'refresh': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_user_refresh_token_due_to_invalid_refresh_token(self):
        data = {
            'refresh': ' '
        }
        
        response = self.client\
                       .post('/api/users/token/refresh', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'refresh': [
                    '이 필드는 blank일 수 없습니다.'
                ]
            }
        )
    
    def test_fail_user_refresh_token_due_to_refresh_token_mismatch(self):
        data = {
            'refresh': 'fake token'
        }
        
        response = self.client\
                       .post('/api/users/token/refresh', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '유효하지 않거나 만료된 토큰',
                'code'  : 'token_not_valid'
            }
        )
    
    def test_fail_user_refresh_token_due_to_token_type_mismatch(self):
        data = {
            'refresh': self.access
        }
        
        response = self.client\
                       .post('/api/users/token/refresh', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '잘못된 토큰 타입',
                'code'  : 'token_not_valid'
            }
        )