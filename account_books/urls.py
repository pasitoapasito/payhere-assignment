from django.urls import path

from account_books.views.account_books import AccountBookView


"""
가계부 url patterns
"""
urlpatterns = [
    path('', AccountBookView.as_view()),
]