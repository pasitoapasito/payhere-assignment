from django.urls import path

from users.views.user_signup  import UserSignUpView
from users.views.user_signin  import UserSignInView
from users.views.user_signout import UserSignOutView


"""
유저 회원가입/로그인/로그아웃 url patterns
"""
urlpatterns = [
    path('/signup', UserSignUpView.as_view()),
    path('/signin', UserSignInView.as_view()),
    path('/signout', UserSignOutView.as_view()),
]