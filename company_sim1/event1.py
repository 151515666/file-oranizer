import random

EVENTS = [
    {
        "name": "투자 유치 성공",
        "description": "삼성전자로부터 투자를 유치했습니다!",
        "effect": {"cash": 5000000, "reputation": 10, "morale": 0}
    },
    {
        "name": "언론 호평",
        "description": "주요 언론에서 회사를 긍정적으로 보도했습니다!",
        "effect": {"cash": 0, "reputation": 15, "morale": 10}
    },
    {
        "name": "핵심 직원 이탈",
        "description": "핵심 직원이 경쟁사로 이직했습니다.",
        "effect": {"cash": 0, "reputation": -5, "morale": -15}
    },
    {
        "name": "소비자 불매운동",
        "description": "소비자 불매운동이 발생했습니다.",
        "effect": {"cash": -3000000, "reputation": -20, "morale": -10}
    },
    {
        "name": "세금 감면 혜택",
        "description": "정부 세금 감면 혜택을 받았습니다!",
        "effect": {"cash": 2000000, "reputation": 0, "morale": 5}
    },
]

CRISIS_EVENTS = [
    {
        "name": "코로나 팬데믹",
        "description": "전세계 팬데믹으로 경기가 급격히 침체됩니다.",
        "effect": {"cash": -10000000, "reputation": -10, "morale": -20}
    },
    {
        "name": "금융위기",
        "description": "글로벌 금융위기가 발생했습니다.",
        "effect": {"cash": -8000000, "reputation": -15, "morale": -15}
    },
    {
        "name": "AI 혁명",
        "description": "AI 기술 혁명으로 시장이 급변합니다.",
        "effect": {"cash": 0, "reputation": 10, "morale": 10}
    },
]

def get_random_event():
    return random.choice(EVENTS)

#이벤트 효과를 company 에 적용하는 함수
def apply_event(company, event):
    effect = event["effect"]

    company.cash += effect["cash"]
    company.reputation += effect["reputation"]

    for employee in company.employees:
        employee.adjust_morale(effect["morale"])
    return event["name"]