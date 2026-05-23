import random

COMPETITOR_NAMES = [
    "넥스트코어", "블루웨이브", "스타트엣지", "퓨처랩", "알파테크",
    "제로원", "노바시스템", "브이엔씨", "오픈마인드", "그린소프트"
]

INDUSTRIES = ["앱", "하드웨어", "서비스"]


class Competitor:

    def __init__(self, name, industry):
        self.name = name
        self.industry = industry
        self.reputation = random.randint(30, 70)   # 초기 평판
        self.cash = random.randint(5000, 20000)     # 초기 자금 (만원)
        self.products = []                          # 출시한 제품명 목록
        self.attack_power = random.randint(5, 20)  # 공격력 (평판 깎는 정도)

    # ── 행동 1: 제품 출시
    def launch_product(self):
        """분기마다 일정 확률로 신제품 출시"""
        if random.random() < 0.3:
            product_name = f"{self.name}_제품{len(self.products) + 1}"
            self.products.append(product_name)
            self.reputation = min(100, self.reputation + random.randint(3, 10))
            return product_name
        return None

    # ── 행동 2: 플레이어 회사 공격
    def attack(self, company):
        """분기마다 일정 확률로 플레이어 회사 평판 공격"""
        if random.random() < 0.25:
            damage = random.randint(1, self.attack_power)
            company.reputation -= damage
            company.reputation = max(0, company.reputation)
            return damage
        return 0

    # ── 자체 성장: 매 분기 소폭 성장
    def grow(self):
        """분기마다 자체적으로 소폭 성장"""
        self.cash += random.randint(500, 2000)
        self.reputation = min(100, self.reputation + random.randint(0, 3))

    def to_dict(self):
        return {
            "name": self.name,
            "industry": self.industry,
            "reputation": self.reputation,
            "cash": self.cash,
            "products": self.products,
            "attack_power": self.attack_power
        }

    @classmethod
    def from_dict(cls, data):
        comp = cls(data["name"], data["industry"])
        comp.reputation = data["reputation"]
        comp.cash = data["cash"]
        comp.products = data["products"]
        comp.attack_power = data["attack_power"]
        return comp


def generate_competitors():
    """랜덤으로 2~4개의 경쟁사 생성"""
    count = random.randint(2, 4)
    names = random.sample(COMPETITOR_NAMES, count)
    competitors = []
    for name in names:
        industry = random.choice(INDUSTRIES)
        competitors.append(Competitor(name, industry))
    return competitors
