import re
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Drink:
    name: str
    quantity: int
    price: Decimal

    def dispense(self) -> bool:
        if self.quantity <= 0:
            return False
        self.quantity -= 1
        return True


@dataclass
class VendingMachine:
    drinks: dict[str, Drink]
    balance: Decimal = Decimal("0.00")

    def __init__(self):
        self.drinks = {}
        reservoir = [
            Drink(name="Water", quantity=5, price=Decimal("2.00")),
            Drink(name="Soda", quantity=3, price=Decimal("3.50")),
            Drink(name="Coffee", quantity=2, price=Decimal("5.00")),
        ]
        for drink in reservoir:
            self.drinks[drink.name] = drink

    @property
    def available_drinks(self) -> list[Drink]:
        return list(filter(lambda drink: drink.quantity > 0, self.drinks.values()))

    @property
    def is_closed(self) -> bool:
        return not any(drink.quantity > 0 for drink in self.drinks.values())

    def reload(self, amount: Decimal):
        self.balance += amount

    def pay(self, amount: Decimal) -> bool:
        if self.balance < amount:
            return False
        self.balance -= amount
        return True

    def dispense(self, drink_name: str) -> bool:
        drink = self.drinks.get(drink_name)

        if not drink:
            print("Invalid drink")
            return False

        if not self.pay(drink.price):
            print("Not enough balance")
            return False

        if not drink.dispense():
            print(f"{drink.name} out of stock")
            self.reload(drink.price)
            return False

        return True


def show_available_drinks(machine: VendingMachine) -> list[Drink]:
    print("\nWe have following drinks:")
    print(f"{'No.':<3} {'Name':<10} {'Price':>5} {'Quantity':>9}")
    available_drinks = machine.available_drinks

    for idx, drink in enumerate(available_drinks, 1):
        print(f"{idx:<3} {drink.name:<10} {drink.price:>5.2f} {drink.quantity:>9}")
    return available_drinks


def reload_balance(machine: VendingMachine):
    reload_complete = False

    while not reload_complete:
        reload_input = input("\nType your reload amount (in int, b to back)\n-> ")
        if reload_input == "b":
            reload_complete = True
            continue
        elif re.search(r"[^0-9]", reload_input):
            print("Only accept notes in integer.")
        else:
            machine.reload(Decimal(reload_input))
            print(f"\nYou had reloaded {Decimal(reload_input):.2f}")
            reload_complete = True


def purchase_drinks(machine: VendingMachine):
    purchase_complete = False

    while not purchase_complete:
        available_drinks = machine.available_drinks
        drink_nos = [idx + 1 for idx in range(len(available_drinks))]
        purchase_input = input(
            "\nWhich drink you wish to purchase (in int, s to show drinks, b to back)\n-> "
        )
        if purchase_input == "b":
            purchase_complete = True
        if purchase_input == "s":
            show_available_drinks(machine)
        elif re.search(r"[^0-9]", purchase_input):
            print(f"Acceptable drink no.: {drink_nos}")
        elif int(purchase_input) not in drink_nos:
            print(f"Acceptable drink no.: {drink_nos}")
        else:
            print()
            drink = available_drinks[int(purchase_input) - 1]
            purchase_complete = machine.dispense(drink.name)

            if purchase_complete:
                print(f"{drink} is dispensed.")


if __name__ == "__main__":
    print("Hello! Welcome to Vending Machine!")
    vending_machine = VendingMachine()

    while not vending_machine.is_closed:
        available_drinks = show_available_drinks(vending_machine)
        print(f"\nYour current balance: {vending_machine.balance}")

        base_input = input(
            "May I help you? (r to reload, p to purchase drink, q to quit)\n-> "
        )

        if base_input == "q":
            break
        elif base_input == "r":
            reload_balance(vending_machine)
        elif base_input == "p":
            purchase_drinks(vending_machine)
        else:
            print("\nInvalid input...")

    if vending_machine.balance > 0:
        print(
            f"\nExtra balance: {vending_machine.balance:.2f}, returning the change..."
        )

    if vending_machine.is_closed:
        print("\nVending machine is out of stock...")
    print("\nThank you for visiting XD")
