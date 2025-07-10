import time
from utils import MyEnum


class AccountStatus(MyEnum):
    OPEN = 0
    CLOSED = 1


class AccountCategory(MyEnum):
    STANDARD = 0
    PREFERENTIAL = 1
    PREMIUM = 2


class Account:

    def __init__(self,
                 account_id: str,
                 status: AccountStatus,
                 open_date: float,
                 close_date: float,
                 category: AccountCategory):
        self.account_id = account_id
        self.status = status
        self.open_date = open_date
        self.close_date = close_date
        self.category = category

    def close(self) -> bool:
        if self.status == AccountStatus.OPEN:
            self.status = AccountStatus.CLOSED
            self.close_date = time.time()
            return True
        return False

    @staticmethod
    def deserialize(arr: list[str]) -> 'Account':
        if len(arr) != 5:
            raise ValueError("Invalid number of fields for Account")

        return Account(
            account_id=arr[0],
            status=AccountStatus.value_of(arr[1]),
            open_date=float(arr[2]),
            close_date=float(arr[3]),
            category=AccountCategory.value_of(arr[4])
        )

    def serialize(self) -> list[str]:
        return [
            self.account_id,
            str(self.status),
            str(self.open_date),
            str(self.close_date),
            str(self.category)
        ]
