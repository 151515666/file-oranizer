import streamlit as st
from company import Company
from employee import Employee
from product import Product
from competitor import Competitor, generate_competitors
from turn import process_turn
from save_load import save_game, load_game, delete_save, save_exists

st.set_page_config(page_title="가상 회사 시뮬레이터", page_icon="🏢", layout="wide")

# ── 세션 초기화
def init_session():
    if "company" not in st.session_state:
        st.session_state.company = None
    if "competitors" not in st.session_state:
        st.session_state.competitors = []
    if "turn_log" not in st.session_state:
        st.session_state.turn_log = []
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "page" not in st.session_state:
        st.session_state.page = "홈"

init_session()

# ── 사이드바
with st.sidebar:
    st.title("🏢 가상 회사 시뮬레이터")
    st.markdown("---")

    if st.session_state.company:
        c = st.session_state.company
        st.markdown(f"**{c.name}**")
        st.markdown(f"💰 자금: `{c.cash:,}만원`")
        st.markdown(f"⭐ 평판: `{c.reputation}/100`")
        st.markdown(f"📅 {c.year}년 Q{c.quarter}")
        st.markdown("---")

    pages = ["홈", "회사 현황", "직원 관리", "제품 관리", "경쟁사", "분기 진행"]
    for p in pages:
        if st.button(p, key=f"nav_{p}", use_container_width=True):
            st.session_state.page = p

    st.markdown("---")
    if st.session_state.company:
        if st.button("💾 저장", use_container_width=True):
            save_game(st.session_state.company, st.session_state.competitors)
            st.success("저장되었습니다!")
        if st.button("🗑️ 게임 초기화", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

page = st.session_state.page

# ════════════════════════════════════════
# 홈
# ════════════════════════════════════════
if page == "홈":
    st.title("🏢 가상 회사 시뮬레이터")
    st.markdown("회사를 창업하고 경쟁사를 이겨 시장을 지배하세요!")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🆕 새 게임 시작")
        company_name = st.text_input("회사 이름", placeholder="예: 미래테크")
        industry = st.selectbox("업종", ["IT", "제조", "서비스", "금융", "바이오"])
        initial_cash = st.slider("초기 자금 (만원)", 5000, 50000, 10000, step=1000)
        start_year = st.number_input("시작 연도", min_value=2020, max_value=2030, value=2024)
        end_year = st.number_input("종료 연도", min_value=2021, max_value=2040, value=2030)

        if st.button("🚀 게임 시작", use_container_width=True):
            if not company_name:
                st.error("회사 이름을 입력해주세요.")
            elif end_year <= start_year:
                st.error("종료 연도는 시작 연도보다 커야 합니다.")
            else:
                company = Company(company_name, industry, initial_cash, start_year, end_year)
                competitors = generate_competitors()
                st.session_state.company = company
                st.session_state.competitors = competitors
                st.session_state.turn_log = []
                st.session_state.game_over = False
                st.session_state.page = "회사 현황"
                st.success(f"'{company_name}' 창업 완료! 경쟁사 {len(competitors)}개 등장.")
                st.rerun()

    with col2:
        st.subheader("📂 이어하기")
        if save_exists():
            st.info("저장된 게임이 있습니다.")
            if st.button("불러오기", use_container_width=True):
                company, competitors = load_game()
                if company:
                    st.session_state.company = company
                    st.session_state.competitors = competitors
                    st.session_state.turn_log = []
                    st.session_state.game_over = False
                    st.session_state.page = "회사 현황"
                    st.rerun()
            if st.button("저장 파일 삭제", use_container_width=True):
                delete_save()
                st.rerun()
        else:
            st.warning("저장된 게임이 없습니다.")

# ════════════════════════════════════════
# 회사 현황
# ════════════════════════════════════════
elif page == "회사 현황":
    if not st.session_state.company:
        st.warning("먼저 게임을 시작해주세요.")
    else:
        c = st.session_state.company
        st.title(f"🏢 {c.name} — 회사 현황")
        st.markdown("---")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 현재 자금", f"{c.cash:,}만원")
        col2.metric("⭐ 평판", f"{c.reputation}/100")
        col3.metric("👥 직원 수", f"{len(c.employees)}명")
        col4.metric("📦 제품 수", f"{len(c.products)}개")

        st.markdown("---")
        col5, col6, col7 = st.columns(3)
        col5.metric("📅 현재 분기", f"{c.year}년 Q{c.quarter}")
        col6.metric("💳 대출금", f"{c.loan:,}만원")
        col7.metric("📊 누적 매출", f"{c.revenue:,}만원")

        st.markdown("---")
        st.subheader("💰 자금 변동 기록")
        if len(c.cash_history) > 1:
            st.line_chart(c.cash_history)
        else:
            st.info("아직 자금 변동 기록이 없습니다.")

        st.markdown("---")
        st.subheader("🏦 대출 관리")
        col_a, col_b = st.columns(2)
        with col_a:
            loan_amount = st.number_input("대출 금액 (만원)", min_value=0, max_value=int(c.max_loan), step=500)
            if st.button("대출 신청"):
                c.take_loan(loan_amount)
                st.rerun()
        with col_b:
            repay_amount = st.number_input("상환 금액 (만원)", min_value=0, max_value=int(c.loan), step=500)
            if st.button("대출 상환"):
                c.repay_loan(repay_amount)
                st.rerun()

# ════════════════════════════════════════
# 직원 관리
# ════════════════════════════════════════
elif page == "직원 관리":
    if not st.session_state.company:
        st.warning("먼저 게임을 시작해주세요.")
    else:
        c = st.session_state.company
        st.title("👥 직원 관리")
        st.markdown("---")

        st.subheader("➕ 직원 채용")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("직원 채용 (랜덤 생성)", use_container_width=True):
                new_emp = Employee()
                new_emp.hire_date = f"{c.year}년 Q{c.quarter}"
                c.hire(new_emp)
                st.success(f"{new_emp.name} ({new_emp.role}) 채용 완료! 월급: {new_emp.salary:,}만원")
                st.rerun()
        with col2:
            st.metric("분기 급여 총액", f"{c.get_total_salary() * 3:,}만원")

        st.markdown("---")
        st.subheader(f"📋 현재 직원 목록 ({len(c.employees)}명)")

        if not c.employees:
            st.info("채용된 직원이 없습니다.")
        else:
            for i, emp in enumerate(c.employees):
                with st.expander(f"{emp.name} — {emp.role}"):
                    col_a, col_b, col_c, col_d = st.columns(4)
                    col_a.metric("월급", f"{emp.salary:,}만원")
                    col_b.metric("생산성", f"{emp.productivity}/100")
                    col_c.metric("경험치", f"{emp.experience}")
                    col_d.metric("입사일", f"{emp.hire_date}")
                    if st.button(f"해고", key=f"fire_{i}"):
                        c.fire(emp)
                        st.rerun()

# ════════════════════════════════════════
# 제품 관리
# ════════════════════════════════════════
elif page == "제품 관리":
    if not st.session_state.company:
        st.warning("먼저 게임을 시작해주세요.")
    else:
        c = st.session_state.company
        st.title("📦 제품 관리")
        st.markdown("---")

        st.subheader("➕ 신제품 개발 시작")
        col1, col2 = st.columns(2)
        with col1:
            product_name = st.text_input("제품명", placeholder="예: 스마트앱 v1")
            category = st.selectbox("카테고리", ["앱", "하드웨어", "서비스"])
        with col2:
            st.markdown("**카테고리별 예상 스펙**")
            st.markdown("- 앱: 개발비 100~300만원, 1~2분기")
            st.markdown("- 하드웨어: 500~1000만원, 3~5분기")
            st.markdown("- 서비스: 200~500만원, 2~3분기")

        if st.button("🔧 개발 시작", use_container_width=True):
            if not product_name:
                st.error("제품명을 입력해주세요.")
            else:
                new_prod = Product(product_name, category)
                if c.cash >= new_prod.dev_cost:
                    c.cash -= new_prod.dev_cost
                    c.products.append(new_prod)
                    st.success(f"'{product_name}' 개발 시작! 개발비: {new_prod.dev_cost:,}만원 / 소요: {new_prod.dev_turns}분기")
                    st.rerun()
                else:
                    st.error(f"자금 부족! 필요: {new_prod.dev_cost:,}만원 / 보유: {c.cash:,}만원")

        st.markdown("---")
        st.subheader(f"📋 제품 목록 ({len(c.products)}개)")

        if not c.products:
            st.info("개발 중인 제품이 없습니다.")
        else:
            for prod in c.products:
                status = "✅ 출시됨" if prod.is_launched else f"🔧 개발중 ({prod.progress}/{prod.dev_turns}분기)"
                with st.expander(f"{prod.name} [{prod.category}] — {status}"):
                    col_a, col_b, col_c, col_d = st.columns(4)
                    col_a.metric("품질", f"{prod.quality}/100")
                    col_b.metric("개발비", f"{prod.dev_cost:,}만원")
                    col_c.metric("분기 매출", f"{prod.revenue:,}만원")
                    col_d.metric("상태", "출시" if prod.is_launched else "개발중")

# ════════════════════════════════════════
# 경쟁사
# ════════════════════════════════════════
elif page == "경쟁사":
    if not st.session_state.company:
        st.warning("먼저 게임을 시작해주세요.")
    else:
        st.title("🏭 경쟁사 현황")
        st.markdown("---")

        competitors = st.session_state.competitors
        if not competitors:
            st.info("경쟁사 정보가 없습니다.")
        else:
            for comp in competitors:
                with st.expander(f"🏭 {comp.name} [{comp.industry}]"):
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("평판", f"{comp.reputation}/100")
                    col2.metric("자금", f"{comp.cash:,}만원")
                    col3.metric("공격력", f"{comp.attack_power}")
                    col4.metric("출시 제품 수", f"{len(comp.products)}개")
                    if comp.products:
                        st.markdown("**출시 제품:** " + ", ".join(comp.products))

# ════════════════════════════════════════
# 분기 진행
# ════════════════════════════════════════
elif page == "분기 진행":
    if not st.session_state.company:
        st.warning("먼저 게임을 시작해주세요.")
    else:
        c = st.session_state.company
        st.title("📅 분기 진행")
        st.markdown("---")

        if st.session_state.game_over:
            st.error("게임 오버! 새 게임을 시작해주세요.")
        else:
            col1, col2, col3 = st.columns(3)
            col1.metric("현재", f"{c.year}년 Q{c.quarter}")
            col2.metric("목표 종료", f"{c.end_date}년")
            col3.metric("자금", f"{c.cash:,}만원")

            st.markdown("---")

            if c.year >= c.end_date:
                st.success(f"🎉 게임 클리어! 최종 자금: {c.cash:,}만원 / 평판: {c.reputation}")
                st.session_state.game_over = True
            else:
                if st.button("⏩ 다음 분기로 진행", use_container_width=True):
                    log, is_over = process_turn(c, st.session_state.competitors)
                    st.session_state.turn_log = log
                    st.session_state.game_over = is_over
                    save_game(c, st.session_state.competitors)
                    st.rerun()

        if st.session_state.turn_log:
            st.markdown("---")
            st.subheader("📋 분기 결과 로그")
            for line in st.session_state.turn_log:
                if line.startswith("==="):
                    st.markdown(f"**{line}**")
                elif line.startswith("[게임오버]"):
                    st.error(line)
                elif line.startswith("[이벤트]"):
                    st.warning(line)
                elif line.startswith("[경쟁사]"):
                    st.info(line)
                elif line.startswith("[출시]"):
                    st.success(line)
                else:
                    st.text(line)
