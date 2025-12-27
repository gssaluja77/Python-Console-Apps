# Coffee App with Rich TUI

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.align import Align
from rich import box

console = Console()


class Coffee:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Order:
    def __init__(self):
        self.cart = []
        self.cart_total = 0

    def add_to_cart(self, item):
        self.cart.append(item)
        self.cart_total += item.price

    def view_cart(self):
        if not self.cart:
            console.print("[red3]🛒 Cart is empty![/red3]")
            return

        # Create cart table
        cart_table = Table(
            title="[bold blue3]🛒 Your Cart[/bold blue3]",
            box=box.ROUNDED,
            border_style="blue3",
        )
        cart_table.add_column("#", style="dim", justify="center")
        cart_table.add_column("Item", style="dark_orange")
        cart_table.add_column("Price", style="green4", justify="right")

        for ind, item in enumerate(self.cart):
            cart_table.add_row(str(ind + 1), item.name, f"${item.price:.2f}")

        cart_table.add_row(
            "",
            "[bold]Total[/bold]",
            f"[bold green4]${self.cart_total:.2f}[/bold green4]",
        )
        console.print(cart_table)

    def edit_cart(self):
        while True:
            if not self.cart:
                console.print("[red3]🛒 Cart is empty![/red3]")
                return

            console.print()
            self.view_cart()
            console.print()

            cart_choices = [str(i) for i in range(1, len(self.cart) + 1)]
            remove = (
                Prompt.ask(
                    "[dark_orange]What to remove? (enter number, 'all' to clear, or 'done' to go back)[/dark_orange]"
                )
                .strip()
                .lower()
            )

            if remove == "all":
                if Confirm.ask("[red3]Clear entire cart?[/red3]", default=False):
                    self.cart = []
                    self.cart_total = 0
                    console.print("[green4]✅ Cart cleared![/green4]")
                return

            if remove == "done":
                return

            if remove in cart_choices:
                removed_item = self.cart[int(remove) - 1]
                console.print(
                    f"[green4]✅ {removed_item.name} removed from cart.[/green4]"
                )
                self.cart_total -= removed_item.price
                del self.cart[int(remove) - 1]
                if not self.cart:
                    return
            else:
                console.print("[red3]❌ Invalid choice![/red3]")

    def checkout(self):
        if not self.cart:
            console.print("[red3]🛒 Cart is empty![/red3]")
            return

        console.print()
        self.view_cart()
        console.print()

        if Confirm.ask(
            f"[dark_orange]💳 Make payment of ${self.cart_total:.2f}?[/dark_orange]",
            default=True,
        ):
            # Payment success panel
            success_panel = Panel(
                f"[green4]✅ Payment successful![/green4]\n\n"
                f"[blue3]Order confirmed! Your coffee will be ready soon.[/blue3]\n"
                f"[dark_orange]Thank you for your order! ☕️[/dark_orange]",
                title="[bold green4]Order Confirmed[/bold green4]",
                border_style="green4",
                box=box.DOUBLE,
                padding=(1, 2),
            )
            console.print(success_panel)
            self.cart = []
            self.cart_total = 0
        else:
            console.print("[dark_orange]Payment cancelled.[/dark_orange]")


def fetch_data():
    menu = [
        Coffee("🥃 Espresso", 3),
        Coffee("🍦 Vanilla Latte", 6.5),
        Coffee("🍫 Cafe Mocha", 5.5),
        Coffee("☁️ Cappuccino", 4),
        Coffee("🍯 Caramel Macchiato", 7),
    ]
    return menu


def main():
    console.clear()

    menu = fetch_data()
    menu_len = len(menu)
    choices = [str(i) for i in range(1, menu_len + 1)]
    new_order = Order()

    # Title
    title_panel = Panel(
        Align.center(Text("☕️ COFFEE MENU ☕️", style="bold purple4")),
        border_style="blue3",
        box=box.DOUBLE,
        padding=(1, 2),
    )
    console.print(title_panel)

    while True:
        console.print()

        # Menu table
        menu_table = Table(
            title="[bold dark_orange]Our Menu[/bold dark_orange]",
            box=box.ROUNDED,
            border_style="dark_orange",
        )
        menu_table.add_column("Choice", style="blue3", justify="center")
        menu_table.add_column("Item", style="dark_orange")
        menu_table.add_column("Price", style="green4", justify="right")

        for ind, item in enumerate(menu):
            menu_table.add_row(str(ind + 1), item.name, f"${item.price:.2f}")

        console.print(menu_table)
        console.print()

        # Actions table
        actions_table = Table(show_header=False, box=box.SIMPLE, border_style="dim")
        actions_table.add_column(style="magenta3", justify="left")
        actions_table.add_row(f"{menu_len + 1}. 🛒 View Cart")
        actions_table.add_row(f"{menu_len + 2}. ✏️  Edit Cart")
        actions_table.add_row(f"{menu_len + 3}. 💳 Checkout")
        actions_table.add_row(f"{menu_len + 4}. 🚪 Exit")
        console.print(actions_table)
        console.print()

        inp = Prompt.ask("[dark_orange]Enter your choice[/dark_orange]").strip()

        if inp in choices:
            choice = int(inp) - 1
            new_order.add_to_cart(menu[choice])
            console.print(f"[green4]✅ {menu[choice].name} added to cart![/green4]")

        elif inp == str(menu_len + 1):
            console.print()
            new_order.view_cart()

        elif inp == str(menu_len + 2):
            new_order.edit_cart()

        elif inp == str(menu_len + 3):
            new_order.checkout()

        elif inp == str(menu_len + 4):
            goodbye_panel = Panel(
                "[dark_orange]👋 Goodbye! Please visit again! 😊[/dark_orange]",
                border_style="dark_orange",
                box=box.ROUNDED,
            )
            console.print(goodbye_panel)
            break

        else:
            if inp:
                console.print("[red3]❌ Invalid choice![/red3]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print()
        console.print()
        goodbye_panel = Panel(
            "[dark_orange]👋 Goodbye! Please visit again! 😊[/dark_orange]",
            border_style="dark_orange",
            box=box.ROUNDED,
        )
        console.print(goodbye_panel)
