from django.urls import path

from users.views.user_signup  import UserSignUpView
from users.views.user_signin  import UserSignInView
from users.views.user_signout import UserSignOutView

from rest_framework_simplejwt.views import TokenRefreshView


"""
유저 회원가입/로그인/로그아웃 url patterns
"""
urlpatterns = [
    path('/signup', UserSignUpView.as_view()),
    path('/signin', UserSignInView.as_view()),
    path('/signout', UserSignOutView.as_view()),
]

"""
유저 토큰 재발급 url patterns
  - 토큰 리프레시 성공 시, 액세스 토큰을 재발급합니다.(리프레시 토큰 재발급 X)
"""
urlpatterns += [
    path('/token/refresh', TokenRefreshView.as_view()),
]