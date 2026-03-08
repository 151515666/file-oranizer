# company.py가 하는 역할: 회사의 모든 핵심 데이터 보관하는 클래스
# 다른 파일들이 company 객체를 가져다 사용
class Company:
    def __init__(self, name, industry, cash):
        # 기본 정보
        self.name = name
        self.industry = industry
        # 재무
        self.cash = cash
        self.initial_cash = cash
        self.max_loan = cash * 2
        self.cash_history = [cash]
        self.revenue = 0
        self.expenses = 0
        # 상태
        self.reputation = 50
        self.quarter = 1
        # 목록
        self.employees = []
        self.products = []
        # 대출
        self.loan = 0
        self.loan_interest = 0.05

    def hire(self, employee):
        self.employees.append(employee)
        self.cash -= employee.salary

    def fire(self, employee):
        self.employees.remove(employee)

    def get_total_salary(self):
        total = 0
        for employee in self.employees:
            total += employee.salary
        return total

    def take_loan(self, amount):
        if self.loan + amount <= self.max_loan:
            self.cash += amount
            self.loan += amount
        else:
            print("대출할 수 없습니다. 사유:한도 초과")

    def repay_loan(self, amount):
        if amount <= self.loan and amount <= self.cash:
            self.cash -= amount
            self.loan -= amount
        else:
            print("상환할 수 없습니다.")

    def calculate_interest(self):
        if self.loan > 0:
            interest = self.loan * self.loan_interest
            self.cash -= interest

    def is_bankrupt(self):
        if self.reputation <= 0:
            return True
        if self.cash <= 0 and self.loan >= self.max_loan:
            return True
        return False

    def check_game_over(self):
        if self.reputation <= 0:
            return (True, "명성이 바닥났습니다. 게임오버!")
        if self.cash <= 0 and self.loan >= self.max_loan:
            return (True, "자금이 고갈되었습니다. 게임 오버!")
        return (False, "")

    def to_dict(self):
        return {
            "name": self.name,
            "industry": self.industry,
            "cash": self.cash,
            "initial_cash": self.initial_cash,
            "max_loan": self.max_loan,
            "cash_history": self.cash_history,
            "revenue": self.revenue,
            "expenses": self.expenses,
            "quarter": self.quarter,
            "reputation": self.reputation,
            "employees": [],
            "products": [],
            "loan": self.loan,
            "loan_interest": self.loan_interest
        }

    @classmethod
    def from_dict(cls, data):
        company = cls(
            name=data["name"],
            industry=data["industry"],
            cash=data["cash"]
        )
        company.initial_cash = data["initial_cash"]
        company.max_loan = data["max_loan"]
        company.cash_history = data["cash_history"]
        company.revenue = data["revenue"]
        company.expenses = data["expenses"]
        company.reputation = data["reputation"]
        company.quarter = data["quarter"]
        company.loan = data["loan"]
        company.loan_interest = data["loan_interest"]

        return company

# if __name__ == "__main__":
#     c = Company("테크스타트", "IT", 5000000)
#     print(c.name)
#     print(c.cash)
#     print(c.max_loan)
