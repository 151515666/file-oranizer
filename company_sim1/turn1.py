import random
from company1 import Company
from competitor1 import Competitor
from event1 import get_random_event, apply_event, CRISIS_EVENTS

def process_turn(company, competitors):
    log = []

    # 1. 급여 차감
    salary = company.get_total_salary()
    company.cash -= salary * 3
    log.append(f"급여 지출: {salary * 3}원")
    # cash 부족 체크
    if company.cash < 0:
        log.append("⚠️ 자금 부족! 대출을 고려하세요.")

    # 2. 상품 개발 진행 + 출시 가능 상품 자동 출시
    for product in company.products:
        product.update_dev()
        if product.is_ready():            # 출시 가능 여부 체크
            product.launch(company)
            log.append(f"🎉 {product.name} 출시!")

    # 3. 판매량 계산
    revenue = 0
    for product in company.products:
        sold = product.calculate_sales(company)
        revenue += sold
    company.revenue = revenue
    log.append(f"매출: {revenue}원")

    # 4. 새 경쟁사 등장 체크
    result = spawn_competitor(competitors)
    if result:
        log.append(f"🆕 새 경쟁사 등장: {result}")

    # 5. 경쟁사 행동
    for competitor in competitors:
        result = competitor.act(company)
        if result:
            log.append(result)

    # 6. 랜덤 이벤트 (40% 확률)
    if random.random() < 0.4:
        event = get_random_event()
        apply_event(company, event)
        log.append(f"이벤트: {event['name']}")

    # 7. 대형 이벤트 (10분기마다 발생)
    if company.quarter % 10 == 0:
        crisis = random.choice(CRISIS_EVENTS)
        apply_event(company, crisis)
        log.append(f"🚨 대형 이벤트: {crisis['name']}")

    # 8. 직원 사기 체크
    for employee in company.employees:
        if employee.morale <= 0:
            result = employee.trigger_morale_event(company)
            log.append(f"{employee.name}: {result}")

    # 9. 대출 이자
    company.calculate_interest()

    # 10. 자금 업데이트
    company.cash_history.append(company.cash)

    # 11. 직원 경력 상승
    for employee in company.employees:
        employee.gain_experience()

    # 12. 수명 마감 체크
    for product in company.products:
        product.update_lifespan()

    # 13. 분기 증가
    company.quarter += 1

    # 14. 게임 오버 체크
    is_over, message = company.check_game_over()

    return log, is_over, message


def spawn_competitor(competitors):
    # 매 분기 20% 확률로 새 경쟁사 등장
    if random.random() < 0.2:
        new_competitor = Competitor()
        competitors.append(new_competitor)
        return new_competitor.name
    return None