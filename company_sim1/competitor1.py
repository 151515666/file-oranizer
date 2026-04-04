import random
COMPETITOR_NAMES = [
    "삼성전자", "SK하이닉스", "한화오션",
    "두산에너빌리티", "마이크론 테크놀로지", "마이크로소프트",
    "TSMC", "알파벳 A"
]

class Competitor:
    def __init__(self):
        self.name = random.choice(COMPETITOR_NAMES)
        self.strength = random.randint(1, 10)
        self.is_active = True

    #매 분기 경쟁사가 행동하는 메서드 strength 기반으로 플레이어 수익 감소
    def act(self, company):
        if not self.is_active:
            return None

        damage = self.strength * 100000
        company.revenue -= damage
        return f"{self.name} 이 시장을 공략해 수익이 {damage}원 감소했습니다."

    def to_dict(self):
        return {
            "name": self.name,
            "strength": self.strength,
            "is_active": self.is_active
        }

    @classmethod
    def from_dict(cls, data):
        competitor = cls()
        competitor.name = data["name"]
        competitor.strength = data["strength"]
        competitor.is_active = data["is_active"]
        return competitor