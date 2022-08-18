from django.urls import path

from users.views.user_signup import UserSignUpView
from users.views.user_signin import UserSignInView


"""
유저 회원가입/로그인 url patterns
"""
urlpatterns = [
    path('/signup', UserSignUpView.as_view()),
    path('/signin', UserSignInView.as_view()),
]