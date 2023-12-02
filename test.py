# Here's a simple Python code that can help you manage and track your investment allocation.

class InvestmentPortfolio:
    def __init__(self, total_amount):
        self.total_amount = total_amount
        self.high_risk = 0
        self.medium_risk = 0
        self.low_risk = 0
        self.cashflow = 0
        self.allocate_investment()

    def allocate_investment(self):
        self.high_risk = self.total_amount * 0.20
        self.medium_risk = self.total_amount * 0.40
        self.low_risk = self.total_amount * 0.20
        self.cashflow = self.total_amount * 0.20

    def display_allocations(self):
        return f"High Risk: RM {self.high_risk:.2f}\nMedium Risk: RM {self.medium_risk:.2f}\nLow Risk: RM {self.low_risk:.2f}\nCash Flow: RM {self.cashflow:.2f}"

    def update_total_amount(self, new_total_amount):
        self.total_amount = new_total_amount
        self.allocate_investment()

# Example usage
portfolio = InvestmentPortfolio(7800)
print(portfolio.display_allocations())
