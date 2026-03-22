import random

class Employee:
    LAST_NAMES = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임"]
    FIRST_NAMES = ["찬솔", "시우", "재윤", "성용", "진우", "도훈", "민혁", "서윤", "준서", "하준"]
    ROLES = ["개발자", "디자이너", "마케터", "영업", "관리자"]
    SALARY_RANGE = {
        "개발자": (400, 600),
        "디자이너": (300, 450),
        "마케터": (300, 450),
        "영업": (250, 400),
        "관리자": (350, 500)
    }

    def __init__(self):
        self.name = random.choice(self.LAST_NAMES) + random.choice(self.FIRST_NAMES)
        self.role = random.choice(self.ROLES)
        min_sal, max_sal = self.SALARY_RANGE[self.role]
        self.salary = random.randint(min_sal, max_sal)
        self.productivity = random.randint(0, 100)
        self.experience = 0
    
    def work(self):
        # 생산성에 따라 회사 수익에 기여
        self.experience += 1
        if self.experience % 10 == 0:  # 10 쌓일 때마다
            # productivity + 5, 단 100 초과 금지
            self.productivity = min(100, self.productivity + 5)

    def to_dict(self):
        return {
            "name": self.name,
            "salary": self.salary,
            "role": self.role,
            "productivity": self.productivity,
            "experience": self.experience
        }
    
    @classmethod
    def from_dict(cls, data):
        emp = cls()   # 일단 랜덤으로 생성
        emp.name = data["name"]
        emp.role = data["role"]
        emp.salary = data["salary"]
        emp.productivity = data["productivity"]
        emp.experience = data["experience"]
        return emp

