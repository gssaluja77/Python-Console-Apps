# Banking Application with Rich TUI

from uuid import uuid4
import os, sys, json, bcrypt
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text
from rich.align import Align
from rich import box
from getpass import getpass

console = Console()

if getattr(sys, "frozen", False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))


def load_existing_bank_data(file_name="bank_data.json"):
    full_path = os.path.join(base_dir, file_name)

    if not os.path.exists(full_path):
        try:
            with open(full_path, "w") as f:
                json.dump({}, f)
        except IOError:
            console.print(f"[red3]Unable to create {full_path} file![/red3]")
            return {}

    try:
        with open(full_path, "r") as f:
            data = f.read().strip()
            if not data:
                return {}
            bank_data = json.loads(data)
            return bank_data
    except json.JSONDecodeError:
        console.print(f"[red3]Warning: Data in {full_path} is corrupted![/red3]")
        return {}
    except IOError as e:
        console.print(f"[red3]Error: Unable to read {full_path} file! {e}[/red3]")
        return {}


def save_bank_data(account_objects, file_name="bank_data.json"):
    full_path = os.path.join(base_dir, file_name)
    serializable_data = {
        acc_num: account.account_to_dict()
        for acc_num, account in account_objects.items()
    }
    with open(full_path, "w") as f:
        json.dump(serializable_data, f)


def validate_amount(amount):
    if not amount:
        return False
    try:
        amount = float(amount)
        if amount <= 0:
            console.print("[red3]❌ Invalid amount![/red3]")
            return False
        return True
    except ValueError:
        console.print("[red3]❌ Invalid amount![/red3]")
        return False


class Account:
    def __init__(self, name, account_number, password, balance=0.0):
        self.name = name
        self.account_number = account_number
        self.password = password
        self.balance = balance

    def account_to_dict(self):
        return {
            "name": self.name,
            "account_number": self.account_number,
            "password": self.password,
            "balance": self.balance,
        }

    @classmethod
    def from_dict_to_account(cls, data):
        return cls(
            name=data["name"],
            account_number=data["account_number"],
            password=data["password"],
            balance=data["balance"],
        )


class Bank:
    def __init__(self):
        bank_raw_data = load_existing_bank_data()
        self.accounts = {
            acc_num: Account.from_dict_to_account(acc_data)
            for acc_num, acc_data in bank_raw_data.items()
        }

    def create_account(self, name, password, balance=0.0):
        unique_account_number = uuid4()
        while str(unique_account_number) in self.accounts:
            unique_account_number = uuid4()
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt(rounds=12)
        )
        self.accounts[str(unique_account_number)] = Account(
            name.strip(),
            str(unique_account_number),
            hashed_password.decode("utf-8"),
            balance,
        )

        # Success panel
        success_panel = Panel(
            f"[green4]✅ Account created successfully![/green4]\n\n"
            f"[dark_orange]Account Number:[/dark_orange] [blue3]{unique_account_number}[/blue3]\n"
            f"[dim]Please note it down for future use.[/dim]",
            title="[bold green4]Account Created[/bold green4]",
            border_style="green4",
            box=box.ROUNDED,
        )
        console.print(success_panel)

    def deposit(self, account_number, amount):
        if not validate_amount(amount):
            return
        amount = float(amount)
        self.accounts[account_number].balance += amount
        console.print(f"[green4]✅ ${amount:.2f} deposited successfully![/green4]")

    def withdraw(self, account_number, amount):
        if not validate_amount(amount):
            return
        amount = float(amount)
        if self.accounts[account_number].balance - amount > 0:
            self.accounts[account_number].balance -= amount
            console.print(f"[green4]✅ ${amount:.2f} withdrawn successfully![/green4]")
        else:
            console.print("[red3]❌ Insufficient funds![/red]")

    def get_current_balance(self, account_number):
        if account_number in self.accounts:
            balance = self.accounts[account_number].balance
            balance_panel = Panel(
                f"[blue3]💰 Current Balance:[/blue3] [green4 bold]${balance:.2f}[/green4 bold]",
                border_style="blue3",
                box=box.ROUNDED,
            )
            console.print(balance_panel)

    def transfer_money(self, from_acc_num, to_acc_num, amount):
        if from_acc_num == to_acc_num:
            console.print("[red3]❌ You can't transfer money to yourself![/red]")
            return
        if not validate_amount(amount):
            return
        amount = float(amount)
        if to_acc_num in self.accounts:
            from_acc = self.accounts[from_acc_num]
            to_acc = self.accounts[to_acc_num]
            if from_acc.balance - amount >= 0:
                from_acc.balance -= amount
                to_acc.balance += amount
                console.print(
                    f"[green4]✅ ${amount:.2f} transferred successfully to {self.accounts[to_acc_num].name}![/green4]"
                )
            else:
                console.print("[red3]❌ You don't have enough funds to transfer![/red]")
        else:
            console.print("[red3]❌ The receiver's account doesn't exist![/red]")


bank = Bank()


def login(account_number, password):
    if account_number in bank.accounts:
        input_password = password.encode("utf-8")
        hashed_password = bank.accounts[account_number].password.encode("utf-8")
        isAuthenticated = bcrypt.checkpw(input_password, hashed_password)
        return isAuthenticated
    else:
        return False


def register():
    console.print()
    console.print(
        "[dark_orange]ℹ️  You will be assigned an account number after registration.[/dark_orange]"
    )
    console.print()

    name = Prompt.ask("[blue3]Enter your name[/blue3]").strip()

    while True:
        password = getpass("Enter your password: ")
        if password == "":
            console.print("[red3]❌ Password cannot be empty![/red]")
            continue
        confirm_password = getpass("Confirm your password: ")
        if password != confirm_password:
            console.print("[red3]❌ Passwords do not match![/red]")
            continue
        break

    while True:
        balance = Prompt.ask(
            "[blue3]Enter initial deposit (press enter to skip)[/blue3]",
        ).strip()
        if balance == "":
            balance = 0.0
            break
        if not validate_amount(balance):
            continue
        balance = float(balance)
        break

    bank.create_account(name, password, balance)
    save_bank_data(bank.accounts)


def private(account_number):
    while True:
        console.print()

        # Create menu table
        menu_table = Table(show_header=False, box=box.SIMPLE, border_style="blue")
        menu_table.add_column(style="cyan", justify="left")
        menu_table.add_row("1️⃣  Deposit Money")
        menu_table.add_row("2️⃣  Withdraw Money")
        menu_table.add_row("3️⃣  Transfer Money")
        menu_table.add_row("4️⃣  Check Balance")
        menu_table.add_row("5️⃣  Logout")
        console.print(menu_table)
        console.print()

        choice = Prompt.ask("[dark_orange]Enter your choice[/dark_orange]").strip()

        if choice == "1":
            amount = Prompt.ask("[blue3]Enter amount to deposit[/blue3]")
            if amount:
                bank.deposit(account_number, amount)

        elif choice == "2":
            amount = Prompt.ask("[blue3]Enter amount to withdraw[/blue3]")
            if amount:
                bank.withdraw(account_number, amount)

        elif choice == "3":
            to_acc = Prompt.ask(
                "[blue3]Enter receiver's account number[/blue3]",
            )
            if to_acc:
                amount = Prompt.ask("[blue3]Enter amount to transfer[/blue3]")
                if amount:
                    bank.transfer_money(account_number, to_acc, amount)

        elif choice == "4":
            bank.get_current_balance(account_number)

        elif choice == "5":
            save_bank_data(bank.accounts)
            goodbye_panel = Panel(
                "[green4]👋 Thanks for visiting![/green4]",
                border_style="green4",
                box=box.ROUNDED,
            )
            console.print(goodbye_panel)
            break
        else:
            if choice:
                console.print("[red3]❌ Invalid choice![/red3]")

        save_bank_data(bank.accounts)


def main():
    console.clear()

    # Title
    title_panel = Panel(
        Align.center(Text("🏦 BANKING APPLICATION 🏦", style="bold purple4")),
        border_style="blue3",
        box=box.DOUBLE,
        padding=(1, 2),
    )
    console.print(title_panel)

    while True:
        console.print()

        # Main menu table
        main_menu = Table(show_header=False, box=box.SIMPLE, border_style="magenta3")
        main_menu.add_column(style="dark_orange", justify="left")
        main_menu.add_row("1️⃣  Login to your account")
        main_menu.add_row("2️⃣  Register for a new account")
        main_menu.add_row("3️⃣  Exit")
        console.print(main_menu)
        console.print()

        choice = Prompt.ask("[dark_orange]Enter your choice[/dark_orange]").strip()

        if choice == "1":
            account_number = Prompt.ask(
                "[blue3]Enter your account number[/blue3]"
            ).strip()
            password = getpass("Enter your password: ")
            isAuthenticated = login(account_number, password)
            if isAuthenticated:
                console.print()
                welcome_panel = Panel(
                    f"[green4]✨ Hi {bank.accounts[account_number].name.split()[0]}, you are logged in![/green4]\n"
                    f"[blue3]How can I help you?[/blue3]",
                    title="[bold green4]Welcome[/bold green4]",
                    border_style="green4",
                    box=box.ROUNDED,
                )
                console.print(welcome_panel)
                private(account_number)
            else:
                console.print("[red3]❌ Invalid account number or password![/red3]")

        elif choice == "2":
            register()

        elif choice == "3":
            goodbye_panel = Panel(
                "[dark_orange]👋 Have a nice day![/dark_orange]",
                border_style="dark_orange",
                box=box.ROUNDED,
            )
            console.print(goodbye_panel)
            break

        else:
            if choice:
                console.print("[red3]❌ Invalid choice![/red3]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print()
        console.print()
        goodbye_panel = Panel(
            "[dark_orange]👋 Have a nice day![/dark_orange]",
            border_style="dark_orange",
            box=box.ROUNDED,
        )
        console.print(goodbye_panel)
