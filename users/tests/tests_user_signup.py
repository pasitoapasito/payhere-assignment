import json

from rest_framework.test import APITestCase

from users.models import User


class UserSignUpTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(1개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(16개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    3. Parameters
        1) email
            - 필수 파라미터 확인
            - 이메일 형식인지 확인
            - 이미 존재하는 이메일인지 확인
        2) nickname
            - 필수 파라미터 확인
            - 이미 존재하는 닉네임인지 확인
        3) password
            - 필수 파라미터 확인
            - 패스워드가 8~20자리인지 확인
            - 패스워드가 최소 1개 이상의 숫자/소문자/대문자/(숫자키)특수문자로 구성되어있는지 확인
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
            
    def test_success_user_signup(self):
        data = {
            'email'   : 'test@example.com',
            'nickname': 'test',
            'password': 'testPassw0rd!'
        }
        
        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                'email'   : 'test@example.com',
                'nickname': 'test'
            }
        )
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_user_signup_due_to_email_required(self):
        data = {
            'nickname': 'test',
            'password': 'testPassw0rd!'
        }
        
        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'email': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_invalid_email_format_first_case(self):
        data = {
            'email'   : 'test@example',
            'nickname': 'test',
            'password': 'testPassw0rd!'
        }
        
        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'email': [
                    '유효한 이메일 주소를 입력하십시오.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_invalid_email_format_second_case(self):
        data = {
            'email'   : 'test@.com',
            'nickname': 'test',
            'password': 'testPassw0rd!'
        }
        
        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'email': [
                    '유효한 이메일 주소를 입력하십시오.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_invalid_email_format_third_case(self):
        data = {
            'email'   : '.test@example.com',
            'nickname': 'test',
            'password': 'testPassw0rd!'
        }
        
        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'email': [
                    '유효한 이메일 주소를 입력하십시오.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_already_existed_email(self):
        data = {
            'email'   : 'user@example.com',
            'nickname': 'test',
            'password': 'testPassw0rd!'
        }
        
        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'email': [
                    'user의 email은/는 이미 존재합니다.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_already_existed_email_n_nickname(self):
        data = {
            'email'   : 'user@example.com',
            'nickname': 'user',
            'password': 'testPassw0rd!'
        }
        
        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'email': [
                    'user의 email은/는 이미 존재합니다.'
                ],
                'nickname': [
                    'user의 nickname은/는 이미 존재합니다.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_nickname_required(self):
        data = {
            'email'   : 'test@example.com',
            'password': 'testPassw0rd!'
        }
        
        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'nickname': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_already_existed_nickname(self):
        data = {
            'email'   : 'test@example.com',
            'nickname': 'user',
            'password': 'testPassw0rd!'
        }
        
        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'nickname': [
                    'user의 nickname은/는 이미 존재합니다.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_required(self):
        data = {
            'email'   : 'test@example.com',
            'nickname': 'test'
        }
        
        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'password': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_gt_20_digit(self):
        data = {
            'email'   : 'test@example.com',
            'nickname': 'test',
            'password': 'loooooooooongPassw0rd!'
        }
        
        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_lt_8_digit(self):
        data = {
            'email'   : 'test@example.com',
            'nickname': 'test',
            'password': 'Pass!'
        }
        
        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_no_small_letters_in_password(self):
        data = {
            'email'   : 'test@example.com',
            'nickname': 'test',
            'password': 'TESTPASSW0RD!'
        }
        
        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_no_capital_letters_in_password(self):
        data = {
            'email'   : 'test@example.com',
            'nickname': 'test',
            'password': 'testpassw0rd!'
        }
        
        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_no_number_in_password(self):
        data = {
            'email'   : 'test@example.com',
            'nickname': 'test',
            'password': 'testPassword!'
        }
        
        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_no_special_letters_in_password(self):
        data = {
            'email'   : 'test@example.com',
            'nickname': 'test',
            'password': 'testPassw0rd'
        }
        
        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_unexpected_special_letters_in_password(self):
        data = {
            'email'   : 'test@example.com',
            'nickname': 'test',
            'password': 'testPassw0rd?'
        }
        
        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )