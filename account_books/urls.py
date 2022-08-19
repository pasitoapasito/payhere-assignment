from django.urls import path

from account_books.views.account_books import AccountBookView, AccountBookDetailView, AccountBookRestoreView


"""
가계부 url patterns
"""
urlpatterns = [
    path('', AccountBookView.as_view()),
    path('/<int:account_book_id>', AccountBookDetailView.as_view()),
    path('/<int:account_book_id>/restore', AccountBookRestoreView.as_view()),
]