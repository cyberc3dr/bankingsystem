from utils import MyEnum


class TransactionType(MyEnum):
    DEPOSIT = 0
    WITHDRAW = 1
    INTEREST = 2
    CLOSE = 3


class Transaction:
    def __init__(self,
                 transaction_id: str,
                 date: float,
                 transaction_type: TransactionType,
                 amount: float,
                 account_id: str):
        self.transaction_id = transaction_id
        self.date = date
        self.transaction_type = transaction_type
        self.amount = amount
        self.account_id = account_id

    @staticmethod
    def deserialize(arr: list[str]) -> 'Transaction':
        if len(arr) != 5:
            raise ValueError("Invalid number of fields for Transaction")

        return Transaction(
            transaction_id=arr[0],
            date=float(arr[1]),
            transaction_type=TransactionType.value_of(arr[2]),
            amount=float(arr[3]),
            account_id=arr[4]
        )

    def serialize(self) -> list[str]:
        return [
            self.transaction_id,
            str(self.date),
            str(self.transaction_type),
            str(self.amount),
            self.account_id
        ]
