class Product:
    def __init__(self, name, category, dev_cost, price):
        self.name = name
        self.category = category
        self.dev_cost = dev_cost
        self.price = price
        self.sales = 0
        self.is_launched = False
        self.is_alive = True
        self.lifespan = 0
        self.dev_progress = 0
        self.quality = 0

        #dev_cost에 따라서 dev_time 자동 계산
        if dev_cost < 10000000:
            self.dev_time = 1
        elif dev_cost < 50000000:
            self.dev_time = 2
        else:
            self.dev_time = 3

    #아직 출시 안된상품에 한해서 매 분기 호출되는 메서드인데 개발 진행도를 1씩 올림
    def update_dev(self):
        if not self.is_launched:
            self.dev_progress += 1

    #출시 가능 여부를 True/False로 반환
    def is_ready(self):
        return self.dev_progress >= self.dev_time and not self.is_launched

    #상품을 출시하는 메서드 (company 객체를 받아서 직원 정보로 품질 개선)
    def launch(self, company):
        if not self.is_ready():
            return False
        #개발자/ 디자이너 필터링
        relevant = [e for e in company.employees
                    if e.role in ["개발자", "디자이너"]]

        if len(relevant) > 0:
            avg_skill = sum(e.skill for e in relevant) / len(relevant)
            self.quality = min(int(avg_skill * 10), 100)
        else:
            self.quality = 0
        self.is_launched = True
        self.lifespan = 4
        return True
    #매 분기 판매량을 계산하는 메서드
    def calculate_sales(self, company):
        if not self.is_launched or not self.is_alive:
            return 0

        base_sales = int(self.quality * company.reputation / self.price * 1000)
        self.sales += base_sales
        self.lifespan -= 1
        return base_sales

    #상품 수명 확인 후 마감 처리
    def update_lifespan(self):
        if self.lifespan <= 0:
            self.is_alive = False

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "dev_cost": self.dev_cost,
            "price": self.price,
            "sales": self.sales,
            "is_launched": self.is_launched,
            "is_alive": self.is_alive,
            "lifespan": self.lifespan,
            "dev_progress": self.dev_progress,
            "quality": self.quality,
            "dev_time": self.dev_time
        }
    @classmethod
    def from_dict(cls, data):
        product = cls(
            name = data["name"],
            category = data["category"],
            dev_cost = data["dev_cost"],
            price = data["price"],
        )
        product.sales = data["sales"]
        product.is_launched = data["is_launched"]
        product.is_alive = data["is_alive"]
        product.lifespan = data["lifespan"]
        product.dev_progress = data["dev_progress"]
        product.quality = data["quality"]
        return product