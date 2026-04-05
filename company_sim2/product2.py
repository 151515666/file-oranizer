import random

class Product:

    CATEGORIES = ["앱", "하드웨어", "서비스"]

    CATEGORY_STATS = {
        "앱":       {"dev_cost": (100, 300), "dev_turns": (1, 2),  "quality": (40, 80)},
        "하드웨어": {"dev_cost": (500, 1000),"dev_turns": (3, 5),  "quality": (30, 70)},
        "서비스":   {"dev_cost": (200, 500), "dev_turns": (2, 3),  "quality": (40, 75)},
    }

    def __init__(self, name, category):
        stats = self.CATEGORY_STATS[category]

        self.name = name
        self.category = category
        self.dev_cost = random.randint(stats["dev_cost"][0], stats["dev_cost"][1])   
        self.dev_turns = random.randint(stats["dev_turns"][0], stats["dev_turns"][1])  
        self.quality = random.randint(stats["quality"][0], stats["quality"][1])   

        self.progress = 0         # 초기값
        self.is_launched = False  # 초기값
        self.revenue = 0          # 초기값

    def develop(self):
        if self.is_launched:
            return

        self.progress += 1

        if self.progress >= self.dev_turns:
            self.is_launched = True

    def to_dict(self): # 저장
        return {
            "name": self.name,
            "category": self.category,
            "dev_cost": self.dev_cost,
            "dev_turns": self.dev_turns,
            "quality": self.quality,
            "progress": self.progress,
            "is_launched": self.is_launched,
            "revenue": self.revenue
        }
    @classmethod
    def from_dict(cls, data): # 불러오기
        prod = cls(data["name"], data["category"])
        prod.dev_cost = data["dev_cost"]
        prod.dev_turns = data["dev_turns"]
        prod.quality = data["quality"]
        prod.progress = data["progress"]
        prod.is_launched = data["is_launched"]
        prod.revenue = data["revenue"]
        return prod
    
    def calculate_revenue(self, employees): # 매출 계산 함수
        if not self.is_launched:
            return 0

        if len(employees) == 0:
            avg_productivity = 10  # 직원 없을 때 최소값
        else:
            avg_productivity = sum(e.productivity for e in employees) / len(employees)

        self.revenue = int(self.quality * avg_productivity * 10)
        return self.revenue