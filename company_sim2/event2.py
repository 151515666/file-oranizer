# events.py
import random

EVENTS = [
    {
        "name": "경제 위기",
        "description": "글로벌 경제 위기로 자금 사정이 악화되었습니다.",
        "probability": 0.15,
        "effects": {
            "cash": (-5000, -1000),
            "reputation": (-10, -3),
        }
    },
    {
        "name": "언론 악재",
        "description": "부정적인 언론 보도로 회사 이미지가 손상되었습니다.",
        "probability": 0.2,
        "effects": {
            "reputation": (-20, -5),
        }
    },
    {
        "name": "직원 번아웃",
        "description": "과로로 인해 직원들의 생산성이 떨어졌습니다.",
        "probability": 0.2,
        "effects": {
            "employee_productivity": (-15, -5),
        }
    },
    {
        "name": "품질 사고",
        "description": "제품 결함이 발견되어 품질과 평판이 하락했습니다.",
        "probability": 0.15,
        "effects": {
            "product_quality": (-15, -5),
            "reputation": (-10, -3),
        }
    },
    {
        "name": "세금 폭탄",
        "description": "예상치 못한 세금 고지서가 날아왔습니다.",
        "probability": 0.1,
        "effects": {
            "cash": (-8000, -3000),
        }
    },
    {
        "name": "투자 유치",
        "description": "외부 투자자로부터 투자를 받았습니다.",
        "probability": 0.15,
        "effects": {
            "cash": (2000, 8000),
        }
    },
    {
        "name": "언론 호재",
        "description": "긍정적인 언론 보도로 회사 이미지가 상승했습니다.",
        "probability": 0.2,
        "effects": {
            "reputation": (5, 20),
        }
    },
    {
        "name": "직원 동기부여",
        "description": "팀 빌딩 성공으로 직원들의 사기가 올랐습니다.",
        "probability": 0.2,
        "effects": {
            "employee_productivity": (5, 15),
        }
    },
    {
        "name": "기술 혁신",
        "description": "내부 연구 성과로 제품 품질이 향상되었습니다.",
        "probability": 0.15,
        "effects": {
            "product_quality": (5, 15),
        }
    },
    {
        "name": "바이럴 마케팅 성공",
        "description": "SNS 바이럴로 브랜드 인지도와 매출이 급상승했습니다.",
        "probability": 0.1,
        "effects": {
            "cash": (1000, 5000),
            "reputation": (10, 25),
        }
    },
]


def get_random_events(events, max_count=3):
    """확률 기반으로 최대 max_count개의 이벤트를 선택해 반환"""
    triggered = []
    for event in events:
        if random.random() < event["probability"]:
            triggered.append(event)
    
    # 최대 개수 초과 시 랜덤으로 추려냄
    if len(triggered) > max_count:
        triggered = random.sample(triggered, max_count)
    
    return triggered


def apply_event(event, company):
    """이벤트 효과를 company 객체에 적용"""
    results = []
    effects = event["effects"]

    if "cash" in effects:
        min_val, max_val = effects["cash"]
        amount = random.randint(min_val, max_val)
        company.cash += amount
        results.append(f"현금 {amount:+,}만원")

    if "reputation" in effects:
        min_val, max_val = effects["reputation"]
        amount = random.randint(min_val, max_val)
        company.reputation += amount
        company.reputation = max(0, min(100, company.reputation))  # 0~100 클램핑
        results.append(f"평판 {amount:+}")

    if "employee_productivity" in effects:
        if company.employees:
            min_val, max_val = effects["employee_productivity"]
            for emp in company.employees:
                amount = random.randint(min_val, max_val)
                emp.productivity += amount
                emp.productivity = max(0, min(100, emp.productivity))  # 0~100 클램핑
            results.append(f"직원 생산성 {min_val}~{max_val:+} 변동")

    if "product_quality" in effects:
        if company.products:
            min_val, max_val = effects["product_quality"]
            for prod in company.products:
                amount = random.randint(min_val, max_val)
                prod.quality += amount
                prod.quality = max(0, min(100, prod.quality))  # 0~100 클램핑
            results.append(f"상품 품질 {min_val}~{max_val:+} 변동")

    return results