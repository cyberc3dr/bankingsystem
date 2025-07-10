from utils import MyEnum


class DepositType(MyEnum):
    DEMAND = 0
    TERM = 1
    SAVINGS = 2

class Deposit:

    def __init__(self,
                 deposit_id: str,
                 deposit_type: DepositType,
                 open_date: float,
                 balance: float,
                 interest_rate: float,
                 closed: bool,
                 client_id: str,
                 account_id: str):
        self.deposit_id = deposit_id
        self.deposit_type = deposit_type
        self.open_date = open_date
        self.balance = balance
        self.interest_rate = interest_rate
        self.closed = closed
        self.client_id = client_id
        self.account_id = account_id

    def withdraw(self, amount: float) -> bool:
        if self.closed or amount > self.balance or amount <= 0:
            return False
        self.balance -= amount
        return True

    def deposit(self, amount: float):
        if not self.closed and amount > 0:
            self.balance += amount

    def calculate_interest(self, to_date: float) -> float:
        if self.closed: return 0.0

        days_diff = (to_date - self.open_date) / 86400  # Convert seconds to days
        year_fraction = days_diff / 365

        return self.balance * self.interest_rate * year_fraction / 100

    def close(self) -> bool:
        if not self.closed:
            self.closed = True
            return True
        return False

    @staticmethod
    def deserialize(arr: list[str]) -> 'Deposit':
        if len(arr) != 8:
            raise ValueError("Invalid number of fields for Deposit")

        return Deposit(
            deposit_id=arr[0],
            deposit_type=DepositType.value_of(arr[1]),
            open_date=float(arr[2]),
            balance=float(arr[3]),
            interest_rate=float(arr[4]),
            closed=arr[5].lower() in ("true", "1"),
            client_id=arr[6],
            account_id=arr[7]
        )

    def serialize(self) -> list[str]:
        return [
            self.deposit_id,
            str(self.deposit_type),
            str(self.open_date),
            str(self.balance),
            str(self.interest_rate),
            "1" if self.closed else "0",
            self.client_id,
            self.account_id
        ]
