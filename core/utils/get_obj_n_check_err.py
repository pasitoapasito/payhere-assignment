from typing import Tuple, Any

from account_books.models import AccountBook
from users.models         import User


class GetAccountBook:
    """
    Assignee: 김동규
    
    param: account_book_id, user
    return: obj, err
    detail:
      - 가계부 id를 통해 가계부 객체(정보)의 존재여부 확인
      - 가계부 객체의 유저정보와 API를 요청한 유저정보가 일치하는지 확인
    """
    
    def get_book_n_check_error(account_book_id: int, user: User) -> Tuple[Any, str]:
        """
        가계부 존재여부 확인
        """
        try:
            book = AccountBook.objects\
                              .get(id=account_book_id)                   
        except AccountBook.DoesNotExist:
            return None, f'가계부 {account_book_id}(id)는 존재하지 않습니다.'
        
        """
        본인의 가계부인지 확인
        """
        if not user.nickname == book.user.nickname:
            return None, f'다른 유저의 가계부입니다.'
        
        return book, None