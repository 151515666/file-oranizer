from events import get_random_events, apply_event, EVENTS


def process_turn(company, competitors):
    """
    한 분기를 처리하고 결과 로그를 반환한다.
    순서: 제품 개발 → 경쟁사 행동 → 이벤트 → 급여 지급 → 매출 계산 → 분기 진행
    """
    log = []

    # ── 1. 제품 개발
    log.append("=== 제품 개발 ===")
    for product in company.products:
        if not product.is_launched:
            product.develop()
            if product.is_launched:
                log.append(f"[출시] {product.name} 이(가) 출시되었습니다!")
            else:
                log.append(f"[개발중] {product.name} 진행도: {product.progress}/{product.dev_turns}")

    # ── 2. 경쟁사 행동
    log.append("=== 경쟁사 행동 ===")
    for comp in competitors:
        # 제품 출시
        launched = comp.launch_product()
        if launched:
            log.append(f"[경쟁사] {comp.name} 이(가) 신제품 '{launched}' 을(를) 출시했습니다.")

        # 플레이어 공격
        damage = comp.attack(company)
        if damage > 0:
            log.append(f"[경쟁사] {comp.name} 의 공격! 평판 -{damage} (현재: {company.reputation})")

        # 자체 성장
        comp.grow()

    # ── 3. 이벤트
    log.append("=== 이벤트 ===")
    triggered = get_random_events(EVENTS)
    if not triggered:
        log.append("이번 분기에는 특별한 이벤트가 없었습니다.")
    for event in triggered:
        results = apply_event(event, company)
        log.append(f"[이벤트] {event['name']}: {event['description']}")
        for r in results:
            log.append(f"  → {r}")

    # ── 4. 급여 지급
    log.append("=== 급여 지급 ===")
    salary_total = company.get_total_salary() * 3
    company.pay_salaries()
    log.append(f"급여 지급: -{salary_total:,}만원 (현재 자금: {company.cash:,}만원)")

    # ── 5. 매출 계산
    log.append("=== 매출 계산 ===")
    total_revenue = 0
    for product in company.products:
        if product.is_launched:
            rev = product.calculate_revenue(company.employees)
            total_revenue += rev
            log.append(f"[매출] {product.name}: {rev:,}만원")
    company.revenue += total_revenue
    company.cash += total_revenue
    if total_revenue == 0:
        log.append("출시된 제품이 없어 매출이 없습니다.")
    else:
        log.append(f"총 매출: {total_revenue:,}만원")

    # ── 6. 분기 진행
    company.cash_history.append(company.cash)
    company.quarter += 1
    if company.quarter > 4:
        company.quarter = 1
        company.year += 1

    log.append("=== 분기 종료 ===")
    log.append(f"현재 자금: {company.cash:,}만원 | 평판: {company.reputation} | {company.year}년 Q{company.quarter}")

    # 파산 체크
    is_over, reason = company.check_game_over()
    if is_over:
        log.append(f"[게임오버] {reason}")

    return log, is_over
