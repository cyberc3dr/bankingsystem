import asyncio

from bankingsystem import BankingSystem
from deposit import DepositType
from utils import clear_screen, parse_date


class UserInterface:
    def __init__(self):
        self.banking_system = BankingSystem()
        self.running = True

    async def run(self):
        while self.running:
            await self.show_main_menu()

    async def show_main_menu(self):
        clear_screen()
        print("\n" + "="*50)
        print("БАНКОВСКАЯ СИСТЕМА УПРАВЛЕНИЯ ВКЛАДАМИ")
        print("="*50)
        print("1. Управление клиентами")
        print("2. Управление вкладами")
        print("3. Отчеты")
        print("4. Выход")
        choice = await self.get_int_input("Выберите пункт (1-4): ", 1, 4)
        if choice == 1:
            await self.client_management()
        elif choice == 2:
            await self.deposit_management()
        elif choice == 3:
            await self.reporting()
        elif choice == 4:
            print("Выход из системы...")
            self.running = False

    async def client_management(self):
        while True:
            clear_screen()
            print("\n" + "="*30)
            print("УПРАВЛЕНИЕ КЛИЕНТАМИ")
            print("="*30)
            print("1. Добавить нового клиента")
            print("2. Просмотреть информацию о клиенте")
            print("3. Изменить данные клиента")
            print("4. Удалить клиента")
            print("5. Список всех клиентов")
            print("6. Назад в главное меню")
            choice = await self.get_int_input("Выберите пункт (1-6): ", 1, 6)
            if choice == 1:
                await self.add_client()
            elif choice == 2:
                await self.view_client()
            elif choice == 3:
                await self.update_client()
            elif choice == 4:
                await self.delete_client()
            elif choice == 5:
                await self.list_all_clients()
            elif choice == 6:
                break

    async def deposit_management(self):
        while True:
            clear_screen()
            print("\n" + "="*30)
            print("УПРАВЛЕНИЕ ВКЛАДАМИ")
            print("="*30)
            print("1. Открыть новый вклад")
            print("2. Просмотреть информацию о вкладе")
            print("3. Пополнить вклад")
            print("4. Снять средства со вклада")
            print("5. Начислить проценты")
            print("6. Закрыть вклад")
            print("7. Список вкладов клиента")
            print("8. Назад в главное меню")
            choice = await self.get_int_input("Выберите пункт (1-8): ", 1, 8)
            if choice == 1:
                await self.add_deposit()
            elif choice == 2:
                await self.view_deposit()
            elif choice == 3:
                await self.deposit_funds()
            elif choice == 4:
                await self.withdraw_funds()
            elif choice == 5:
                await self.calculate_interest()
            elif choice == 6:
                await self.close_deposit()
            elif choice == 7:
                await self.list_client_deposits()
            elif choice == 8:
                break

    async def reporting(self):
        while True:
            clear_screen()
            print("\n" + "="*30)
            print("ФОРМИРОВАНИЕ ОТЧЕТОВ")
            print("="*30)
            print("1. Отчет по клиенту")
            print("2. Отчет по всем клиентам")
            print("3. Отчет по типу вклада")
            print("4. Отчет по операциям со счетом")
            print("5. Сводный отчет по системе")
            print("6. Назад в главное меню")
            choice = await self.get_int_input("Выберите пункт (1-6): ", 1, 6)
            if choice == 1:
                await self.generate_client_report()
            elif choice == 2:
                await self.generate_all_clients_report()
            elif choice == 3:
                await self.generate_deposit_type_report()
            elif choice == 4:
                await self.generate_transaction_report()
            elif choice == 5:
                await self.generate_system_summary_report()
            elif choice == 6:
                break

    # --- Клиенты ---
    async def add_client(self):
        clear_screen()
        full_name = await self.get_str_input("Введите ФИО клиента: ")
        if self.banking_system.add_client(full_name):
            print("Клиент успешно добавлен.")
        else:
            print("Ошибка: Не удалось добавить клиента.")
        await self.wait_for_keypress()

    async def view_client(self):
        clear_screen()
        clients = self.banking_system.get_all_clients()
        if not clients:
            print("В системе нет зарегистрированных клиентов.")
            await self.wait_for_keypress()
            return
        print("Список клиентов:")
        for c in clients:
            print(f"{c.client_id} - {c.full_name}")
        client_id = await self.get_str_input("Введите ID клиента: ")
        client = self.banking_system.get_client(client_id)
        clear_screen()
        if client:
            print(self.banking_system.generate_client_report(client_id))
        else:
            print(f"Клиент с ID {client_id} не найден.")
        await self.wait_for_keypress()

    async def update_client(self):
        clear_screen()
        clients = self.banking_system.get_all_clients()
        if not clients:
            print("В системе нет зарегистрированных клиентов.")
            await self.wait_for_keypress()
            return
        print("Список клиентов:")
        for c in clients:
            print(f"{c.client_id} - {c.full_name}")
        client_id = await self.get_str_input("Введите ID клиента: ")
        client = self.banking_system.get_client(client_id)
        clear_screen()
        if client:
            print(f"Текущее ФИО: {client.full_name}")
            new_name = await self.get_str_input("Введите новое ФИО клиента: ")
            if self.banking_system.update_client(client_id, new_name):
                print("Данные клиента успешно обновлены.")
            else:
                print("Ошибка: Не удалось обновить данные клиента.")
        else:
            print(f"Клиент с ID {client_id} не найден.")
        await self.wait_for_keypress()

    async def delete_client(self):
        clear_screen()
        clients = self.banking_system.get_all_clients()
        if not clients:
            print("В системе нет зарегистрированных клиентов.")
            await self.wait_for_keypress()
            return
        print("Список клиентов:")
        for c in clients:
            print(f"{c.client_id} - {c.full_name}")
        client_id = await self.get_str_input("Введите ID клиента для удаления: ")
        deposits = self.banking_system.get_client_deposits(client_id)
        clear_screen()
        if deposits:
            print("Ошибка: Нельзя удалить клиента, у которого есть вклады. Сначала закройте все вклады клиента.")
            await self.wait_for_keypress()
            return
        if self.banking_system.delete_client(client_id):
            print("Клиент успешно удален.")
        else:
            print("Ошибка: Не удалось удалить клиента.")
        await self.wait_for_keypress()

    async def list_all_clients(self):
        clear_screen()
        clients = self.banking_system.get_all_clients()
        if not clients:
            print("В системе нет зарегистрированных клиентов.")
        else:
            print("ID    | ФИО                            | Кол-во вкладов")
            print("-"*55)
            for c in clients:
                deps = self.banking_system.get_client_deposits(c.client_id)
                print(f"{c.client_id:5} | {c.full_name:30} | {len(deps):14}")
        await self.wait_for_keypress()

    # --- Вклады ---
    async def add_deposit(self):
        clear_screen()
        clients = self.banking_system.get_all_clients()
        if not clients:
            print("В системе нет зарегистрированных клиентов. Сначала добавьте клиента.")
            await self.wait_for_keypress()
            return
        print("Список клиентов:")
        for c in clients:
            print(f"{c.client_id} - {c.full_name}")
        client_id = await self.get_str_input("Введите ID клиента: ")
        dep_type = await self.get_deposit_type_input()
        initial_balance = await self.get_float_input("Введите начальную сумму вклада: ", 0.0)
        interest_rate = await self.get_float_input("Введите процентную ставку (% годовых): ", 0.0)
        clear_screen()
        if self.banking_system.add_deposit(client_id, dep_type, initial_balance, interest_rate):
            print("Вклад успешно открыт.")
        else:
            print("Ошибка: Не удалось открыть вклад.")
        await self.wait_for_keypress()

    async def view_deposit(self):
        clear_screen()
        deposit_id = await self.get_str_input("Введите ID вклада: ")
        deposit = self.banking_system.get_deposit(deposit_id)
        clear_screen()
        if deposit:
            print(self.banking_system.generate_deposit_type_report(deposit.deposit_type))
        else:
            print(f"Вклад с ID {deposit_id} не найден.")
        await self.wait_for_keypress()

    async def deposit_funds(self):
        clear_screen()
        deposit_id = await self.get_str_input("Введите ID вклада: ")
        deposit = self.banking_system.get_deposit(deposit_id)
        if deposit and not deposit.closed:
            amount = await self.get_float_input("Введите сумму пополнения: ", 0.01)
            clear_screen()
            if self.banking_system.deposit_funds(deposit_id, amount):
                print("Вклад успешно пополнен.")
            else:
                print("Ошибка: Не удалось пополнить вклад.")
        else:
            clear_screen()
            print("Вклад не найден или закрыт.")
        await self.wait_for_keypress()

    async def withdraw_funds(self):
        clear_screen()
        deposit_id = await self.get_str_input("Введите ID вклада: ")
        deposit = self.banking_system.get_deposit(deposit_id)
        if deposit and not deposit.closed:
            amount = await self.get_float_input("Введите сумму для снятия: ", 0.01, deposit.balance)
            clear_screen()
            if self.banking_system.withdraw_funds(deposit_id, amount):
                print("Средства успешно сняты.")
            else:
                print("Ошибка: Не удалось снять средства со вклада.")
        else:
            clear_screen()
            print("Вклад не найден или закрыт.")
        await self.wait_for_keypress()

    async def calculate_interest(self):
        clear_screen()
        deposit_id = await self.get_str_input("Введите ID вклада: ")
        deposit = self.banking_system.get_deposit(deposit_id)
        if deposit and not deposit.closed:
            date_str = await self.get_str_input("Введите дату (дд.мм.гггг): ")
            try:
                to_date = parse_date(date_str)
            except Exception as e:
                clear_screen()
                print(str(e))
                await self.wait_for_keypress()
                return
            clear_screen()
            if self.banking_system.calculate_interest(deposit_id, to_date):
                print("Проценты успешно начислены.")
            else:
                print("Ошибка: Не удалось начислить проценты.")
        else:
            clear_screen()
            print("Вклад не найден или закрыт.")
        await self.wait_for_keypress()

    async def close_deposit(self):
        clear_screen()
        deposit_id = await self.get_str_input("Введите ID вклада: ")
        deposit = self.banking_system.get_deposit(deposit_id)
        if deposit and not deposit.closed:
            confirm = await self.get_bool_input("Вы уверены, что хотите закрыть вклад? (д/н): ")
            clear_screen()
            if confirm:
                if self.banking_system.close_deposit(deposit_id):
                    print("Вклад успешно закрыт.")
                else:
                    print("Ошибка: Не удалось закрыть вклад.")
            else:
                print("Операция отменена.")
        else:
            clear_screen()
            print("Вклад не найден или уже закрыт.")
        await self.wait_for_keypress()

    async def list_client_deposits(self):
        clear_screen()
        clients = self.banking_system.get_all_clients()
        if not clients:
            print("В системе нет зарегистрированных клиентов.")
            await self.wait_for_keypress()
            return
        print("Список клиентов:")
        for c in clients:
            print(f"{c.client_id} - {c.full_name}")
        client_id = await self.get_str_input("Введите ID клиента: ")
        client = self.banking_system.get_client(client_id)
        clear_screen()
        if client:
            deposits = self.banking_system.get_client_deposits(client_id)
            print(f"Клиент: {client.full_name} ({client_id})")
            print(f"Количество вкладов: {len(deposits)}")
            if not deposits:
                print("У клиента нет открытых вкладов.")
            else:
                print("ID    | Тип              | Баланс     | Ставка % | Состояние")
                for d in deposits:
                    status = "Закрыт" if d.closed else "Активен"
                    print(f"{d.deposit_id:5} | {str(d.deposit_type):16} | {d.balance:10.2f} | {d.interest_rate:8.2f} | {status:8}")
        else:
            print(f"Клиент с ID {client_id} не найден.")
        await self.wait_for_keypress()

    # --- Отчеты ---
    async def generate_client_report(self):
        clear_screen()
        client_id = await self.get_str_input("Введите ID клиента: ")
        clear_screen()
        print(self.banking_system.generate_client_report(client_id))
        await self.wait_for_keypress()

    async def generate_all_clients_report(self):
        clear_screen()
        print(self.banking_system.generate_all_clients_report())
        await self.wait_for_keypress()

    async def generate_deposit_type_report(self):
        clear_screen()
        dep_type = await self.get_deposit_type_input()
        clear_screen()
        print(self.banking_system.generate_deposit_type_report(dep_type))
        await self.wait_for_keypress()

    async def generate_transaction_report(self):
        clear_screen()
        deposit_id = await self.get_str_input("Введите ID вклада: ")
        deposit = self.banking_system.get_deposit(deposit_id)
        if not deposit:
            clear_screen()
            print(f"Вклад с ID {deposit_id} не найден.")
            await self.wait_for_keypress()
            return
        account_id = deposit.account_id
        from_date_str = await self.get_str_input("Введите начальную дату (дд.мм.гггг): ")
        to_date_str = await self.get_str_input("Введите конечную дату (дд.мм.гггг): ")
        try:
            from_date = parse_date(from_date_str)
            to_date = parse_date(to_date_str)
        except Exception as e:
            clear_screen()
            print(str(e))
            await self.wait_for_keypress()
            return
        clear_screen()
        print(self.banking_system.generate_transaction_report(account_id, from_date, to_date))
        await self.wait_for_keypress()

    async def generate_system_summary_report(self):
        clear_screen()
        print(self.banking_system.generate_system_summary_report())
        await self.wait_for_keypress()

    # --- Вспомогательные методы ---
    async def get_str_input(self, prompt: str) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: input(prompt).strip())

    async def get_int_input(self, prompt: str, min_value: int, max_value: int = 999999) -> int:
        while True:
            value = await self.get_str_input(prompt)
            try:
                ivalue = int(value)
                if min_value <= ivalue <= max_value:
                    return ivalue
            except Exception:
                pass
            print(f"Введите целое число от {min_value} до {max_value}.")

    async def get_float_input(self, prompt: str, min_value: float = 0.0, max_value: float = 1e12) -> float:
        while True:
            value = await self.get_str_input(prompt)
            try:
                fvalue = float(value)
                if min_value <= fvalue <= max_value:
                    return fvalue
            except Exception:
                pass
            print(f"Введите число от {min_value} до {max_value}.")

    async def get_bool_input(self, prompt: str) -> bool:
        value = (await self.get_str_input(prompt)).lower()
        return value in ("д", "да", "y", "yes")

    async def get_deposit_type_input(self) -> DepositType:
        print("Типы вкладов:\n1. До востребования\n2. Срочный\n3. Накопительный")
        choice = await self.get_int_input("Выберите тип вклада (1-3): ", 1, 3)
        if choice == 1:
            return DepositType.DEMAND
        elif choice == 2:
            return DepositType.TERM
        else:
            return DepositType.SAVINGS

    async def wait_for_keypress(self):
        await self.get_str_input("Нажмите Enter для продолжения...")
