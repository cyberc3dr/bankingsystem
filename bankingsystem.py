import time

from account import AccountStatus, Account
from deposit import DepositType, Deposit
from filedatabase import FileDatabase
from transaction import TransactionType, Transaction
from client import Client

from typing import List, Optional


class BankingSystem:
    def __init__(self):
        self.db = FileDatabase("data")

    # Клиенты
    def add_client(self, full_name: str) -> bool:
        return self.db.add_client(full_name)

    def update_client(self, client_id: str, full_name: str) -> bool:
        client = self.db.get_client(client_id)
        if not client:
            return False
        client.full_name = full_name
        return self.db.update_client(client)

    def delete_client(self, client_id: str) -> bool:
        return self.db.delete_client(client_id)

    def get_all_clients(self) -> List[Client]:
        return self.db.clients

    def get_client(self, client_id: str) -> Optional[Client]:
        return self.db.get_client(client_id)

    # Вклады
    def add_deposit(self, client_id: str, dep_type: DepositType, initial_balance: float, interest_rate: float) -> bool:
        return self.db.add_deposit(client_id, dep_type, initial_balance, interest_rate)

    def deposit_funds(self, deposit_id: str, amount: float) -> bool:
        return self.db.deposit_funds(deposit_id, amount)

    def withdraw_funds(self, deposit_id: str, amount: float) -> bool:
        return self.db.withdraw_funds(deposit_id, amount)

    def calculate_interest(self, deposit_id: str, to_date: float) -> bool:
        return self.db.calculate_and_add_interest(deposit_id, to_date)

    def close_deposit(self, deposit_id: str) -> bool:
        return self.db.close_deposit(deposit_id)

    def get_deposit(self, deposit_id: str) -> Optional[Deposit]:
        return self.db.get_deposit(deposit_id)

    def get_client_deposits(self, client_id: str) -> List[Deposit]:
        return self.db.get_client_deposits(client_id)

    def get_all_deposits(self) -> List[Deposit]:
        return self.db.deposits

    # Счета
    def get_account(self, account_id: str) -> Optional[Account]:
        return self.db.get_account(account_id)

    def get_deposit_account(self, deposit_id: str) -> Optional[Account]:
        return self.db.get_deposit_account(deposit_id)

    # Транзакции
    def get_account_transactions(self, account_id: str) -> List[Transaction]:
        return self.db.get_account_transactions(account_id)

    # Отчёты
    def generate_client_report(self, client_id: str) -> str:
        client = self.db.get_client(client_id)
        if not client:
            return f"Клиент с ID {client_id} не найден."
        deposits = self.db.get_client_deposits(client_id)
        report = []
        report.append("ОТЧЕТ ПО КЛИЕНТУ\n================\n")
        report.append(f"ID клиента: {client.client_id}\nФИО: {client.full_name}\nКоличество вкладов: {len(deposits)}\n")
        if not deposits:
            report.append("У клиента нет открытых вкладов.\n")
        else:
            report.append("Список вкладов:\n")
            report.append("ID    | Тип               | Дата открытия | Баланс       | Ставка % | Статус\n")
            total_balance = 0.0
            for d in deposits:
                status = "Закрыт" if d.closed else "Активен"
                report.append(f"{d.deposit_id:5} | {str(d.deposit_type):17} | {time.strftime('%d.%m.%Y', time.localtime(d.open_date)):13} | {d.balance:12.2f} | {d.interest_rate:8.2f} | {status}\n")
                if not d.closed:
                    total_balance += d.balance
            report.append(f"Итого по активным вкладам: {total_balance:.2f}\n")
        return "".join(report)

    def generate_all_clients_report(self) -> str:
        clients = self.db.clients
        deposits = self.db.deposits
        report = []
        report.append("ОТЧЕТ ПО ВСЕМ КЛИЕНТАМ\n=====================\n")
        report.append(f"Всего клиентов: {len(clients)}\n")
        if not clients:
            report.append("В системе нет зарегистрированных клиентов.\n")
        else:
            report.append("ID    | ФИО                            | Кол-во вкладов | Общий баланс\n")
            for client in clients:
                client_deps = [d for d in deposits if d.client_id == client.client_id and not d.closed]
                total_balance = sum(d.balance for d in client_deps)
                report.append(f"{client.client_id:5} | {client.full_name:30} | {len(client_deps):14} | {total_balance:12.2f}\n")
        return "".join(report)

    def generate_deposit_type_report(self, dep_type: DepositType) -> str:
        deposits = [d for d in self.db.deposits if d.deposit_type == dep_type and not d.closed]
        clients = {c.client_id: c.full_name for c in self.db.clients}
        report = []
        report.append(f"ОТЧЕТ ПО ТИПУ ВКЛАДА: {dep_type}\n==============================\n")
        report.append(f"Всего вкладов данного типа: {len(deposits)}\n")
        if not deposits:
            report.append("Нет активных вкладов данного типа.\n")
        else:
            report.append("ID    | ФИО клиента                    | Дата открытия | Баланс       | Ставка %\n")
            total_balance = 0.0
            avg_interest = 0.0
            for d in deposits:
                client_name = clients.get(d.client_id, "Неизвестно")
                report.append(f"{d.deposit_id:5} | {client_name:30} | {time.strftime('%d.%m.%Y', time.localtime(d.open_date)):13} | {d.balance:12.2f} | {d.interest_rate:8.2f}\n")
                total_balance += d.balance
                avg_interest += d.interest_rate
            avg_interest /= len(deposits)
            report.append(f"Итого по всем вкладам: {total_balance:.2f}\n")
            report.append(f"Средняя процентная ставка: {avg_interest:.2f}%\n")
        return "".join(report)

    def generate_transaction_report(self, account_id: str, from_date: float, to_date: float) -> str:
        account = self.db.get_account(account_id)
        if not account:
            return f"Счет с ID {account_id} не найден."
        txs = [t for t in self.db.get_account_transactions(account_id) if from_date <= t.date <= to_date]
        report = []
        report.append("ОТЧЕТ ПО ОПЕРАЦИЯМ СО СЧЕТОМ\n===========================\n")
        report.append(f"ID счета: {account_id}\nСтатус счета: {'Открыт' if account.status == AccountStatus.OPEN else 'Закрыт'}\n")
        report.append(f"Дата открытия: {time.strftime('%d.%m.%Y', time.localtime(account.open_date))}\n")
        if account.status == AccountStatus.CLOSED:
            report.append(f"Дата закрытия: {time.strftime('%d.%m.%Y', time.localtime(account.close_date))}\n")
        report.append(f"Категория счета: {account.category}\n")
        report.append(f"Период отчета: с {time.strftime('%d.%m.%Y', time.localtime(from_date))} по {time.strftime('%d.%m.%Y', time.localtime(to_date))}\n")
        report.append(f"Количество операций за период: {len(txs)}\n")
        if not txs:
            report.append("За указанный период операций не производилось.\n")
        else:
            report.append("ID Транзакции  | Дата       | Операция     | Сумма\n")
            total_deposit = total_withdraw = total_interest = 0.0
            for t in txs:
                report.append(f"{t.transaction_id:14} | {time.strftime('%d.%m.%Y', time.localtime(t.date))} | {t.transaction_type:12} | {t.amount:10.2f}\n")
                if t.transaction_type == TransactionType.DEPOSIT:
                    total_deposit += t.amount
                elif t.transaction_type == TransactionType.WITHDRAW:
                    total_withdraw += t.amount
                elif t.transaction_type == TransactionType.INTEREST:
                    total_interest += t.amount
            report.append(f"Итого пополнений: {total_deposit:.2f}\n")
            report.append(f"Итого снятий: {total_withdraw:.2f}\n")
            report.append(f"Итого начислено процентов: {total_interest:.2f}\n")
            report.append(f"Общий оборот: {(total_deposit - total_withdraw + total_interest):.2f}\n")
        return "".join(report)

    def generate_system_summary_report(self) -> str:
        clients = self.db.clients
        deposits = self.db.deposits
        accounts = self.db.accounts
        demand = [d for d in deposits if d.deposit_type == DepositType.DEMAND and not d.closed]
        term = [d for d in deposits if d.deposit_type == DepositType.TERM and not d.closed]
        savings = [d for d in deposits if d.deposit_type == DepositType.SAVINGS and not d.closed]
        total_balance = sum(d.balance for d in deposits if not d.closed)
        report = ["СВОДНЫЙ ОТЧЕТ ПО БАНКОВСКОЙ СИСТЕМЕ\n==================================\n",
                  f"Всего клиентов: {len(clients)}\n",
                  f"Всего вкладов: {len(deposits)} (активных: {len(demand) + len(term) + len(savings)})\n",
                  f"Всего счетов: {len(accounts)}\n", "Распределение вкладов по типам:\n",
                  f"До востребования: {len(demand)} на сумму {sum(d.balance for d in demand):.2f}\n",
                  f"Срочные: {len(term)} на сумму {sum(d.balance for d in term):.2f}\n",
                  f"Накопительные: {len(savings)} на сумму {sum(d.balance for d in savings):.2f}\n",
                  f"Итого по всем вкладам: {total_balance:.2f}\n"]
        if total_balance > 0:
            report.append("Структура портфеля вкладов:\n")
            report.append(f"До востребования: {sum(d.balance for d in demand)/total_balance*100:.2f}%\n")
            report.append(f"Срочные: {sum(d.balance for d in term)/total_balance*100:.2f}%\n")
            report.append(f"Накопительные: {sum(d.balance for d in savings)/total_balance*100:.2f}%\n")
        return "".join(report)
