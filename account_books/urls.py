from django.urls import path

from account_books.views.account_books           import AccountBookView, AccountBookDetailView, AccountBookRestoreView
from account_books.views.account_book_categories import AccountBookCategoryView, AccountBookCategoryDetailView,\
                                                        AccountBookCategoryRestoreView
from account_books.views.account_book_logs       import AccountBookLogView

"""
가계부 url patterns
"""
urlpatterns = [
    path('', AccountBookView.as_view()),
    path('/<int:account_book_id>', AccountBookDetailView.as_view()),
    path('/<int:account_book_id>/restore', AccountBookRestoreView.as_view()),
]

"""
가계부 카테고리 url patterns
"""
urlpatterns += [
    path('/categories', AccountBookCategoryView.as_view()),
    path('/categories/<int:account_book_category_id>', AccountBookCategoryDetailView.as_view()),
    path('/categories/<int:account_book_category_id>/restore', AccountBookCategoryRestoreView.as_view()),
]

"""
가계부 기록 url patterns
"""
urlpatterns += [
    path('/<int:account_book_id>/logs', AccountBookLogView.as_view()),
]