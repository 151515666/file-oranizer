import random

SALARY_RANGE = {
    "개발자": (3000000, 6000000),
    "마케터": (2500000, 5000000),
    "영업": (2000000, 4500000),
    "디자이너": (2500000, 5000000),
    "관리자": (3500000, 7000000),
    "회계사": (3000000, 6000000),
    "법무담당": (4000000, 8000000),
    "HR담당": (2500000, 5000000),
}


class Employee:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.skill = random.randint(1, 10)
        self.morale = 70
        self.is_striking = False
        self.experience = 0

        # 역할에 맞는 급여 범위에서 랜덤 생성
        min_sal, max_sal = SALARY_RANGE[role]
        self.salary = random.randint(min_sal, max_sal)

    # 직원 1명의 실제 업무 기여도를 숫자로 계산해서 반환
    def get_performance(self):
        if self.is_striking:
            return 0
        return self.skill * (self.morale / 100)

    # 사기 구간별 페널티 값을 반환
    def get_morale_penalty(self):
        if self.morale > 75:
            return 0.1
        elif self.morale > 50:
            return 0
        elif self.morale > 25:
            return -0.1
        elif self.morale > 0:
            return -0.25
        else:
            return -0.5

    # 어떤 이벤트가 발생했는지 문자열로 반환
    def trigger_morale_event(self, company):
        events = ["퇴사", "파업", "태업", "소문", "무사"]
        result = random.choice(events)

        if result == "퇴사":
            company.fire(self)
        elif result == "파업":
            self.is_striking = True
        elif result == "태업":
            self.skill -= 2
            if self.skill < 1:
                self.skill = 1
        elif result == "소문":
            company.reputation -= 10
        return result

    #morale 을 amount 만큼 조정하는거
    def adjust_morale(self, amount):
        self.morale += amount
        if self.morale > 100:
            self.morale = 100
        if self.morale < 0:
            self.morale = 0

    #경력이 쌓이면 능력치 자동 상승
    def gain_experience(self):
        self.experience += 1
        if self.experience % 4 == 0:
            self.skill += 1
            if self.skill > 10:
                self.skill = 10

    def to_dict(self):
        return {
            "name": self.name,
            "role": self.role,
            "skill": self.skill,
            "salary": self.salary,
            "morale": self.morale,
            "is_striking": self.is_striking,
            "experience": self.experience
        }

    @classmethod
    def from_dict(cls, data):
        employee = cls(
            name=data["name"],
            role=data["role"]
        )
        employee.skill = data["skill"]
        employee.salary = data["salary"]
        employee.morale = data["morale"]
        employee.is_striking = data["is_striking"]
        employee.experience = data["experience"]
        return employee
