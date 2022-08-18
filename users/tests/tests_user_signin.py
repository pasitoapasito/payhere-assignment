import json

from rest_framework.test             import APITestCase
from rest_framework_simplejwt.tokens import OutstandingToken

from users.models import User


class UserSignInTest(APITestCase):
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
        1) email
            - 필수 파라미터 확인
            - 입력받은 이메일이 유저의 이메일과 일치하는지 확인
        2) password
            - 필수 파라미터 확인
            - 입력받은 패스워드가 유저의 패스워드와 일치하는지 확인
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저 정보)
    """
    
    @classmethod
    def setUpTestData(cls):
        User.objects\
            .create_user(
                email    = 'user@example.com',
                nickname = 'user',
                password = 'userPassw0rd!'
            )
    
    """
    성공 케이스 테스트코드
    """
            
    def test_success_user_signin(self):
        data = {
            'email'   : 'user@example.com',
            'password': 'userPassw0rd!'
        }
        
        response = self.client\
                       .post('/api/users/signin', data=json.dumps(data), content_type='application/json')
        
        user = User.objects\
                   .get(email='user@example.com')
                   
        token = OutstandingToken.objects\
                                .get(user=user)\
                                .token
                                
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['refresh'], token)
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_user_signin_due_to_email_required(self):
        data = {
            'password': 'userPassw0rd!'
        }
        
        response = self.client\
                       .post('/api/users/signin', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'email': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_user_signin_due_to_email_mismatch(self):
        data = {
            'email'   : 'test@example.com',
            'password': 'userPassw0rd!'
        }
        
        response = self.client\
                       .post('/api/users/signin', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'non_field_errors': [
                    'detail : 올바른 유저정보를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signin_due_to_password_required(self):
        data = {
            'email': 'user@example.com'
        }
        
        response = self.client\
                       .post('/api/users/signin', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'password': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_user_signin_due_to_password_mismatch(self):
        data = {
            'email'   : 'user@example.com',
            'password': 'testPassw0rd!'
        }
        
        response = self.client\
                       .post('/api/users/signin', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'non_field_errors': [
                    'detail : 올바른 유저정보를 입력하세요.'
                ]
            }
        )