class Category:
    # When objects are created, they are passed in the name of the category
    def __init__(self, name):
        self.name = name
        self.ledger = []

    # deposit method that accepts an amount and description
    def deposit(self, amount, description=""):
        # If no description is given, it should default to an empty string
        # Append an object to the ledger list in the form of {"amount": amount, "description": description}.
        deposit = {"amount": amount, "description": description}
        self.ledger.append(deposit)
        return deposit

    def check_funds(self, amount):
        funds = 0
        for item in self.ledger:
            funds += item["amount"]
        return False if amount > funds else True

    # withdraw method similar to deposit method
    def withdraw(self, amount, description=""):
        withdraw = {"amount": -amount, "description": description}
        if self.check_funds(amount):
            # amount passed should be stored in the ledger as a negative number
            self.ledger.append(withdraw)
            return True
        else:
            return False

    # get_balance method that current balance of the budget category based on the deposits and withdrawals that have occurred.
    def get_balance(self):
        balance = 0
        for item in self.ledger:
            balance += item["amount"]
        return balance

    # transfer method that accepts an amount and another budget category as arguments
    def transfer(self, amount, obj):
        # add a withdrawal with the amount and the description
        # if there aren't not enough funds, nothing should be added to either ledgers
        # return True if the transfer took place, and false otherwise
        if self.withdraw(amount, "Transfer to " + obj.name):
            obj.deposit(amount, "Transfer from " + self.name)
            return True
        return False

    # check_funds method that accepts an amount as an argument
    def check_funds(self, amount):
        # returns false if the amount is greater than the balance of the budget category and returns True otherwise
        # This method should be used by both the withdraw method and transfer method
        return amount <= self.get_balance()

    def create_spend_ledger(self):
        # A title line of 30 characters where the name of the category is centered in a line of * characters.
        # A list of the items in the ledger.
        # Each line should show the description and amount.
        # The first 23 characters of the description should be displayed, then the amount.
        # The amount should be right aligned, contain two decimal places, and display a maximum of 7 characters.
        # A line displaying the category total.
        output = ""
        output += self.name.center(30, "*") + "\n"

        total = 0
        for item in self.ledger:
            total += item["amount"]

            output += item["description"].ljust(23, " ")[:23]
            output += "{0:>7.2f}".format(item["amount"])
            output += "\n"

        output = "Total: " + "{0:.2f}".format(total)
        return output


def create_spend_chart(categories):
    # return a string that is a bar chart
    # chart should show the percentage spent in each category passed in to the function
    # percentage spent should be calculated only with withdrawls and not with deposits
    # left side of the chart should be lebels 0-100
    # the bars in the bar chart should be made out of the 0 character
    # the height of each bar should be rounded down to the nearest 10
    # the horizontal line below the bars should go two spaces past the final bar
    # each category name should be written vertically below the bar
    # there should be a title at the top that says percentage spent by category
    output = "Percentage spent by category\n"

    total = 0
    expenses = []
    names = []
    len_names = 0

    for item in categories:
        expense = sum([-x["amount"] for x in item.ledger if x["amount"] < 0])
        total += expense

        if len(item.name) > len_names:
            len_names = len(item.name)

        expenses.append(expense)
        names.append(item.name)

    expenses = [(x / total) * 100 for x in expenses]
    names = [name.ljust(len_names, " ") for name in names]

    for c in range(100, -1, -10):
        output += str(c).rjust(3, " ") + "|"
        for x in expenses:
            output += " o " if x >= c else "   "
        output += " \n"

    output += "    " + "---" * len(names) + "-\n"

    for i in range(len_names):
        output += "    "
        for name in names:
            output += " " + name[i] + " "
        output += " \n"

    return output.strip("\n")
