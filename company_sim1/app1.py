import streamlit as st
from company1 import Company
from competitor1 import Competitor
from turn1 import process_turn, spawn_competitor
from save_load1 import save_game, load_game

#session_state 초기화
#아직 게임 시작 전이면 None 또는 빈 리스트로 설정

if "company" not in st.session_state:
    st.session_state.company = None
if "competitors" not in st.session_state:
    st.session_state.competitors = []
if "log" not in st.session_state:
    st.session_state.log = []

if st.session_state.company is None:
    st.title("🏢 가상 회사 시뮬레이션")

    #입력받기
    name = st.text_input("회사 이름을 입력하세요")
    industry = st.text_input("업종을 입력하세요")
    cash = st.number_input("초기 자금", min_value=1000000, step=1000000)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 새 게임 시작"):
            if name and industry:  #이름, 업종 입력했을 때만
                st.session_state.company = Company(name, industry, cash)
                st.rerun()    #화면 즉시 새로고침
    with col2:
        if st.button("📂 불러오기"):
            company, competitors = load_game()
            st.session_state.company = company
            st.session_state.competitors = competitors
            st.rerun()
else:
    company = st.session_state.company
    competitors = st.session_state.competitors

    #사이드바
    st.sidebar.title(f"🏢 {company.name}")
    st.sidebar.metric("💰 자금", f"{company.cash:,}원")
    st.sidebar.metric("⭐ 명성", company.reputation)
    st.sidebar.metric("📅 분기", f"{company.quarter}분기")
    st.sidebar.metric("👥 직원", f"{len(company.employees)}명")
    st.sidebar.metric("📦 상품", f"{len(company.products)}개")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["⚡ 행동", "👥 직원", "📦 상품", "📋 로그"]
    )
    #── 탭1 : 행동 ──────────────────────────
    with tab1:
        st.subheader("이번 분기 행동")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⏩ 다음 분기"):
                log, is_over, message = process_turn(
                    company,
                    competitors
                )
                st.session_state.log = log
                if is_over:
                    st.error(message)
                    st.session_state.company = None
                else:
                    st.rerun()
        with col2:
            if st.button("💾 저장"):
                save_game(company, competitors)
                st.success("저장 완료!")
    #── 탭2: 직원  ──────────────────────────
    with tab2:
        st.subheader("직원 목록")
        for e in company.employees:
            st.write(
                f"{e.name} | {e.role} | "
                f"능력: {e.skill} | 사기: {e.morale}"
            )

    # ── 탭3: 상품 ──────────────────────────
    with tab3:
        st.subheader("상품 목록")
        for p in company.products:
            st.write(
                f"{p.name} | 품질: {p.quality} | "
                f"출시: {p.is_launched}"
            )
    # ── 탭4: 로그 ──────────────────────────
    with tab4:
        st.subheader("이번 분기 로그")
        for item in st.session_state.log:
            st.write(item)
    # ── 자금 변화 그래프 ───────────────────
    st.subheader("📊 자금 변화")
    st.line_chart(company.cash_history)