class Company:

    def __init__(self, name, industry, cash, start_date, end_date):
        # 기본 정보
        self.name = name # 회사 이름
        self.industry = industry # 업계
        self.start_date = start_date # 게임 시작 날짜
        self.year = self.start_date # 현재 연도
        self.end_date = end_date # 게임 종료 날짜

        self.quarter = 1 # 현재 분기
        self.reputation = 50 # 평판 (0~100)

        # 재정
        self.cash = cash # 초기 자금
        self.initial_cash = cash # 초기 자금 기록
        self.max_loan = cash * 2 # 최대 대출 한도
        self.cash_history = [cash] # 자금 변동 기록
        self.revenue = 0 # 수익
        self.expenses = 0 # 비용

        self.employees = [] # 직원 목록 "employees": [e.to_dict() for e in self.employees],
        self.products = [] # 제품 목록 "products": [p.to_dict() for p in self.products],
        # 대출
        self.loan = 0 # 현재 대출 금액
        self.loan_interest = 0.05 # 대출 이자율
        

    def hire(self, employee):
        self.employees.append(employee)           
    def fire(self, employee):
        if employee in self.employees:
            self.employees.remove(employee)
    def get_total_salary(self):
        total = 0
        for employee in self.employees:
            total += employee.salary
        return total
    def pay_salaries(self):
        total = self.get_total_salary() * 3  # 분기 = 3개월
        self.cash -= total
        self.expenses += total
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
            self.expenses += interest
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
    #객체 -> 딕셔너리
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
    #딕셔너리 -> 객체 (클래스 메서드)
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
    
    #일반 메서드는 객체가 있어야 호출할 수 있다.  from_dict()는 객체를 만들기 위해 호출하는 함수
    #일반 메서드는 "이미 만들어진 회사에게 일을 시키는 것" 회사가 존재해야 호출가능
    #@classmethod는 "회사를 새로 설립하는 공장역할" 회사가 없어도 호출가능함, 호출하면 새 회사를 만들어서 반환