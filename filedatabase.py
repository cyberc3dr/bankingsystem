import random
import time
import os

from pystreamapi import Stream

from account import Account, AccountStatus, AccountCategory
from client import Client
from deposit import Deposit, DepositType
from transaction import Transaction, TransactionType
from utils import read_file, write_to_file


class FileDatabase:
    def __init__(self, data_dir: str):
        os.makedirs(data_dir, exist_ok=True)

        self.clients_file = f"{data_dir}/clients.csv"
        self.deposits_file = f"{data_dir}/deposits.csv"
        self.accounts_file = f"{data_dir}/accounts.csv"
        self.transactions_file = f"{data_dir}/transactions.csv"

        self.clients = []
        self.deposits = []
        self.accounts = []
        self.transactions = []

        self.load_all()

    def load_all(self):
        self.load_clients()
        self.load_deposits()
        self.load_accounts()
        self.load_transactions()

    def load_clients(self):
        self.clients.clear()

        Stream.of(read_file(self.clients_file)) \
            .for_each(lambda line: self.clients.append(Client.deserialize(line)))

    def load_deposits(self):
        self.deposits.clear()

        Stream.of(read_file(self.deposits_file)) \
            .for_each(lambda line: self.deposits.append(Deposit.deserialize(line)))

    def load_accounts(self):
        self.accounts.clear()

        Stream.of(read_file(self.accounts_file)) \
            .for_each(lambda line: self.accounts.append(Account.deserialize(line)))

    def load_transactions(self):
        self.transactions.clear()

        Stream.of(read_file(self.transactions_file)) \
            .for_each(lambda line: self.transactions.append(Transaction.deserialize(line)))

    def save_clients(self):
        write_to_file(self.clients_file, [client.serialize() for client in self.clients])

    def save_deposits(self):
        write_to_file(self.deposits_file, [deposit.serialize() for deposit in self.deposits])

    def save_accounts(self):
        write_to_file(self.accounts_file, [account.serialize() for account in self.accounts])

    def save_transactions(self):
        write_to_file(self.transactions_file, [transaction.serialize() for transaction in self.transactions])

    def save_all(self):
        self.save_clients()
        self.save_deposits()
        self.save_accounts()
        self.save_transactions()

    def generate_client_id(self) -> str:
        while True:
            cid = f"C{random.randint(0, 9999)}"
            if all(c.client_id != cid for c in self.clients):
                return cid

    def generate_deposit_id(self) -> str:
        while True:
            did = f"D{random.randint(0, 9999)}"
            if all(d.deposit_id != did for d in self.deposits):
                return did

    def generate_account_id(self) -> str:
        while True:
            aid = f"A{random.randint(0, 9999)}"
            if all(a.account_id != aid for a in self.accounts):
                return aid

    def generate_transaction_id(self) -> str:
        return f"T{int(time.time())}{random.randint(0, 999)}"

    def get_client(self, client_id: str) -> Client:
        return Stream.of(self.clients) \
            .filter(lambda c: c.client_id == client_id) \
            .find_first() \
            .or_else(None)

    def add_client(self, full_name: str) -> bool:
        if not full_name:
            return False
        client_id = self.generate_client_id()
        client = Client(client_id, full_name)
        self.clients.append(client)
        self.save_clients()
        return True

    def update_client(self, client: Client) -> bool:
        for idx, c in enumerate(self.clients):
            if c.client_id == client.client_id:
                self.clients[idx] = client
                self.save_clients()
                return True
        return False

    def delete_client(self, client_id: str) -> bool:
        if any(d.client_id == client_id for d in self.deposits):
            return False
        for idx, c in enumerate(self.clients):
            if c.client_id == client_id:
                del self.clients[idx]
                self.save_clients()
                return True
        return False

    def get_deposit(self, deposit_id: str) -> Deposit:
        return Stream.of(self.deposits) \
            .filter(lambda d: d.deposit_id == deposit_id) \
            .find_first() \
            .or_else(None)

    def get_client_deposits(self, client_id: str) -> list:
        return Stream.of(self.deposits) \
            .filter(lambda d: d.client_id == client_id) \
            .to_list()

    def add_deposit(self, client_id: str, dep_type: DepositType, initial_balance: float, interest_rate: float) -> bool:
        if not any(c.client_id == client_id for c in self.clients) or initial_balance < 0 or interest_rate < 0:
            return False
        deposit_id = self.generate_deposit_id()
        account_id = self.generate_account_id()
        import time
        now = int(time.time())
        account = Account(account_id, AccountStatus.OPEN, now, 0, AccountCategory.STANDARD)
        self.accounts.append(account)
        deposit = Deposit(deposit_id, dep_type, now, initial_balance, interest_rate, False, client_id, account_id)
        self.deposits.append(deposit)
        if initial_balance > 0:
            self.add_transaction(account_id, TransactionType.DEPOSIT, initial_balance)
        self.save_accounts()
        self.save_deposits()
        return True

    def update_deposit(self, deposit: Deposit) -> bool:
        for idx, d in enumerate(self.deposits):
            if d.deposit_id == deposit.deposit_id:
                self.deposits[idx] = deposit
                self.save_deposits()
                return True
        return False

    def delete_deposit(self, deposit_id: Deposit) -> bool:
        for idx, d in enumerate(self.deposits):
            if d.deposit_id == deposit_id:
                if not d.closed:
                    return False
                account = self.get_account(d.account_id)
                if not account or account.status != AccountStatus.CLOSED:
                    return False
                del self.deposits[idx]
                self.save_deposits()
                return True
        return False

    def get_account(self, account_id: str) -> Account:
        return Stream.of(self.accounts) \
            .filter(lambda a: a.account_id == account_id) \
            .find_first() \
            .or_else(None)

    def get_deposit_account(self, deposit_id: str) -> Account | None:
        deposit = self.get_deposit(deposit_id)
        if not deposit:
            return None
        return self.get_account(deposit.account_id)

    def add_account(self, deposit_id: str, category: AccountCategory) -> bool:
        deposit = self.get_deposit(deposit_id)
        if not deposit:
            return False
        account_id = self.generate_account_id()
        import time
        now = int(time.time())
        account = Account(account_id, AccountStatus.OPEN, now, 0, category)
        self.accounts.append(account)
        deposit.account_id = account_id
        self.save_accounts()
        self.save_deposits()
        return True

    def update_account(self, account: Account) -> bool:
        for idx, a in enumerate(self.accounts):
            if a.account_id == account.account_id:
                self.accounts[idx] = account
                self.save_accounts()
                return True
        return False

    def close_account(self, account_id: str) -> bool:
        account = self.get_account(account_id)
        if not account:
            return False
        for deposit in self.deposits:
            if deposit.account_id == account_id and not deposit.closed:
                if not self.close_deposit(deposit.deposit_id):
                    return False
        if hasattr(account, "close"):
            success = account.close()
        else:
            account.status = AccountStatus.CLOSED
            success = True
        if success:
            self.save_accounts()
        return success

    def get_all_transactions(self) -> list:
        return sorted(self.transactions, key=lambda t: t.date, reverse=True)

    def get_account_transactions(self, account_id: str) -> list:
        txs = [t for t in self.transactions if t.account_id == account_id]
        return sorted(txs, key=lambda t: t.date, reverse=True)

    def add_transaction(self, account_id: str, tx_type: TransactionType, amount: float) -> bool:
        if not self.get_account(account_id) or amount < 0:
            return False
        tx_id = self.generate_transaction_id()
        import time
        now = int(time.time())
        transaction = Transaction(tx_id, now, tx_type, amount, account_id)
        self.transactions.append(transaction)
        self.save_transactions()
        return True

    def deposit_funds(self, deposit_id: str, amount: float) -> bool:
        if amount <= 0:
            return False
        deposit = self.get_deposit(deposit_id)
        if not deposit or deposit.closed:
            return False
        deposit.deposit(amount)
        self.add_transaction(deposit.account_id, TransactionType.DEPOSIT, amount)
        self.save_deposits()
        return True

    def withdraw_funds(self, deposit_id: str, amount: float) -> bool:
        if amount <= 0:
            return False
        deposit = self.get_deposit(deposit_id)
        if not deposit or deposit.closed:
            return False
        if not deposit.withdraw(amount):
            return False
        self.add_transaction(deposit.account_id, TransactionType.WITHDRAW, amount)
        self.save_deposits()
        return True

    def calculate_and_add_interest(self, deposit_id: str, to_date: float) -> bool:
        deposit = self.get_deposit(deposit_id)
        if not deposit or deposit.closed:
            return False
        interest = deposit.calculate_interest(to_date)
        if interest <= 0:
            return False
        deposit.deposit(interest)
        self.add_transaction(deposit.account_id, TransactionType.INTEREST, interest)
        self.save_deposits()
        return True

    def close_deposit(self, deposit_id: str) -> bool:
        deposit = self.get_deposit(deposit_id)
        if not deposit or deposit.closed:
            return False
        balance = deposit.balance
        if hasattr(deposit, "close"):
            closed = deposit.close()
        else:
            deposit.closed = True
            closed = True
        if not closed:
            return False
        self.add_transaction(deposit.account_id, TransactionType.CLOSE, balance)
        account = self.get_account(deposit.account_id)
        if account:
            if hasattr(account, "close"):
                account.close()
            else:
                account.status = AccountStatus.CLOSED
        self.save_deposits()
        self.save_accounts()
        return True
