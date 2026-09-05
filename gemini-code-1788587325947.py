import streamlit as st
import re

st.set_page_config(page_title="서·논술형 자동 채점 시스템", layout="wide")

st.title("📝 2회고사 대비 서·논술형 답안 자동 채점 시스템")
st.caption("설명 방법 및 매체 복합양식성 활용 문항 채점 도구")

# ------------------------------------------------------------------------------
# Helper Functions (채점 유틸리티 함수)
# ------------------------------------------------------------------------------

def check_keywords(text, required_groups):
    """
    required_groups: [[키워드1, 키워드2], [키워드3]] -> 그룹 내 하나 이상 포함 필수
    """
    for group in required_groups:
        if not any(kw in text for kw in group):
            return False
    return True

def detect_explanation_methods(text):
    """
    문장 내 용어 명시 또는 표현적 특성을 분석하여 사용된 설명 방법을 감지
    """
    methods = []
    # 1. 명시적 표기 검지
    if "(정의)" in text or "정의" in text: methods.append("정의")
    if "(예시)" in text or "예시" in text: methods.append("예시")
    if "(인과)" in text or "인과" in text: methods.append("인과")
    if "(비교)" in text or "(대조)" in text or "(비교와 대조)" in text or "비교" in text or "대조" in text: methods.append("비교와 대조")
    if "(분류)" in text or "(구분)" in text or "(분류와 구분)" in text or "분류" in text: methods.append("분류와 구분")

    # 2. 표현 특성 기반 감지 (용어 미표기 시 구제)
    if "~란" in text or "뜻한다" in text or "의미한다" in text or "말한다" in text:
        if "정의" not in methods: methods.append("정의")
    if "예를 들어" in text or "예로" in text or "대표적으로" in text:
        if "예시" not in methods: methods.append("예시")
    if "때문에" in text or "인해" in text or "원인은" in text or "결과적으로" in text:
        if "인과" not in methods: methods.append("인과")
    if "반면" in text or "달리" in text or "공통점" in text or "차이점" in text or "아닌" in text:
        if "비교와 대조" not in methods: methods.append("비교와 대조")
    if "나뉜다" in text or "구분된다" in text or "분류된다" in text:
        if "분류와 구분" not in methods: methods.append("분류와 구분")

    return list(set(methods))

# ------------------------------------------------------------------------------
# Tab Configuration
# ------------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["[실전 1] 사회적 촉진/억제", "[실전 2] 정전기의 특징", "[실전 3] AI 그림과 예술"])

# ==============================================================================
# SET 1 채점 로직 및 UI
# ==============================================================================
with tab1:
    st.header("[실전 적용-1] 사회적 촉진과 사회적 억제")
    
    with st.expander("📌 모범 답안 및 평가 기준 보기"):
        st.markdown("""
        **[서·논술형 1]** (1) 쉬운 과제 / (2) 차분하게 혼자 집중함 / (3) 사회적 억제  
        **[서·논술형 2]**  
        - *옵션 A (예시+인과):* (1) 쉬운 과제를 할 때는 커피숍처럼 타인과 함께하는 환경이 좋다. (예시) (2) 반면 어려운 과제는 타인이 있으면 방해가 되므로 혼자 집중해야 한다. (인과)  
        - *옵션 B (정의+대조):* (1) 사회적 촉진이란 쉬운 과제 시 효율이 올라가는 현상이다. (정의) (2) 쉬운 과제는 모임이 유리한 반면 어려운 과제는 혼자만의 공간이 유리하다. (비교와 대조)  
        **[서·논술형 3]**  
        - *시각:* 개인 방/독서실에서 한 학생이 책에 몰입하는 모습을 클로즈업 연출. (효과: 외부 자극 차단 및 몰입 강조)  
        - *청각:* 시계 초침 소리만 들리는 정적 음향. (효과: 외부 자극을 줄여 깊은 집중 유도)
        """)

    st.subheader("1. [서·논술형 1] 표 채우기")
    q1_1 = st.text_input("1세트 (1) 답안", key="s1_q1_1")
    q1_2 = st.text_input("1세트 (2) 답안", key="s1_q1_2")
    q1_3 = st.text_input("1세트 (3) 답안", key="s1_q1_3")

    st.subheader("2. [서·논술형 2] 설명문 작성")
    q2_1 = st.text_input("1세트 (1) 문장 작성", key="s1_q2_1")
    q2_2 = st.text_input("1세트 (2) 문장 작성", key="s1_q2_2")

    st.subheader("3. [서·논술형 3] 영상 기획안")
    q3_v = st.text_area("1세트 시각 요소(Ⓐ) 및 효과", key="s1_q3_v")
    q3_a = st.text_area("1세트 청각 요소(Ⓑ) 및 효과", key="s1_q3_a")

    if st.button("1세트 답안 채점하기"):
        st.divider()
        st.markdown("### 📊 채점 결과")
        
        # Q1 채점
        score_q1 = 0
        q1_1_pass = check_keywords(q1_1, [["쉬운", "친숙한", "노력이 적은", "간단한"]])
        q1_2_pass = check_keywords(q1_2, [["혼자", "독서실", "개인"] , ["집중", "연습", "차분"]])
        q1_3_pass = ("사회적 억제" in q1_3.strip())

        if q1_1_pass and q1_2_pass and q1_3_pass:
            st.success("[문항 1] 정답 (만점)")
        else:
            st.error(f"[문항 1] 부분 점수 또는 오답 | (1): {'통과' if q1_1_pass else '미통과'}, (2): {'통과' if q1_2_pass else '미통과'}, (3): {'통과' if q1_3_pass else '미통과'}")

        # Q2 채점
        m1 = detect_explanation_methods(q2_1)
        m2 = detect_explanation_methods(q2_2)
        
        # 오개념 검증: 쉬운 과제에 '혼자', 어려운 과제에 '모임'을 결합하면 오답
        concept_error = ("쉬운" in q2_1 and "혼자" in q2_1) or ("어려운" in q2_2 and "함께" in q2_2)
        
        if concept_error:
            st.error("[문항 2] 오답: 과제 난이도에 따른 학습 환경 오개념이 발견되었습니다.")
        elif len(m1) > 0 and len(m2) > 0 and set(m1) != set(m2):
            st.success(f"[문항 2] 조건 충족 (통과) | (1) 감지된 방법: {', '.join(m1)} / (2) 감지된 방법: {', '.join(m2)}")
        else:
            st.warning(f"[문항 2] 감점/미통과 | 두 문장에 서로 다른 설명 방법이 명확히 적용되어야 합니다. (감지 (1): {m1}, (2): {m2})")

        # Q3 채점
        v_pass = check_keywords(q3_v, [["혼자", "개인", "독서실", "클로즈업"], ["차단", "집중", "몰입"]])
        a_pass = check_keywords(q3_a, [["고요", "정적", "초침", "소음 최소"], ["자극", "불안", "집중", "몰입"]])
        
        if v_pass and a_pass:
            st.success("[문항 3] 조건 충족 (통과): 어려운 과제에 필요한 시/청각 연출과 몰입 효과 결론이 타당함.")
        else:
            st.error(f"[문항 3] 미통과 | 시각 연출 및 효과: {'통과' if v_pass else '미통과'}, 청각 연출 및 효과: {'통과' if a_pass else '미통과'}")

# ==============================================================================
# SET 2 채점 로직 및 UI
# ==============================================================================
with tab2:
    st.header("[실전 적용-2] 겨울철 정전기의 특징")
    
    with st.expander("📌 모범 답안 및 평가 기준 보기"):
        st.markdown("""
        **[서·논술형 1]** (1) 높은 곳에 고여 있는 물 / (2) 전하가 이동하지 않고 머물러 있음 / (3) 위험하지 않음  
        **[서·논술형 2]**  
        - *옵션 A (정의+대조):* (1) 정전기란 전하가 정지 상태로 머물러 있는 전기를 말한다. (정의) (2) 실생활 전기가 흐르는 물이라면 정전기는 고여 있는 물과 같아 위험하지 않다. (비교와 대조)  
        - *옵션 B (분류+인과):* (1) 전하는 이동 여부에 따라 실생활 전기와 정전기로 나뉜다. (분류와 구분) (2) 정전기는 전하가 이동하지 않기 때문에 전압이 높아도 피해가 없다. (인과)  
        **[서·논술형 3]**  
        - *시각:* 높은 산 저수지에 잔잔하게 고여 있는 물을 정적으로 보여줌. (효과: 전하가 이동하지 않는 정지 상태 표현)  
        - *청각:* 소리가 없는 정적 음향. (효과: 전하 이동이 없어 위험하지 않음을 전달)
        """)

    st.subheader("1. [서·논술형 1] 표 채우기")
    q1_1 = st.text_input("2세트 (1) 답안", key="s2_q1_1")
    q1_2 = st.text_input("2세트 (2) 답안", key="s2_q1_2")
    q1_3 = st.text_input("2세트 (3) 답안", key="s2_q1_3")

    st.subheader("2. [서·논술형 2] 설명문 작성")
    q2_1 = st.text_input("2세트 (1) 문장 작성", key="s2_q2_1")
    q2_2 = st.text_input("2세트 (2) 문장 작성", key="s2_q2_2")

    st.subheader("3. [서·논술형 3] 영상 기획안")
    q3_v = st.text_area("2세트 시각 요소(Ⓐ) 및 효과", key="s2_q3_v")
    q3_a = st.text_area("2세트 청각 요소(Ⓑ) 및 효과", key="s2_q3_a")

    if st.button("2세트 답안 채점하기"):
        st.divider()
        st.markdown("### 📊 채점 결과")
        
        # Q1 채점
        q1_1_pass = check_keywords(q1_1, [["고여 있는 물"], ["높은"]])
        q1_2_pass = check_keywords(q1_2, [["이동하지", "머물러", "정지"]])
        q1_3_pass = check_keywords(q1_3, [["위험하지 않", "피해가 없", "안전"]])

        if q1_1_pass and q1_2_pass and q1_3_pass:
            st.success("[문항 1] 정답 (만점)")
        else:
            st.error(f"[문항 1] 미통과 | (1): {'통과' if q1_1_pass else '미통과'}, (2): {'통과' if q1_2_pass else '미통과'}, (3): {'통과' if q1_3_pass else '미통과'}")

        # Q2 채점
        m1 = detect_explanation_methods(q2_1)
        m2 = detect_explanation_methods(q2_2)
        
        # 오개념 검증: 정전기에 전하가 이동한다거나 위험하다고 서술한 경우
        concept_error = ("정전기" in q2_1 and "이동" in q2_1) or ("정전기" in q2_2 and "위험하다" in q2_2)
        
        if concept_error:
            st.error("[문항 2] 오답: 정전기의 전하 이동성 및 위험성에 대한 과학적 오개념이 발견되었습니다.")
        elif len(m1) > 0 and len(m2) > 0 and set(m1) != set(m2):
            st.success(f"[문항 2] 조건 충족 (통과) | (1) 감지: {', '.join(m1)} / (2) 감지: {', '.join(m2)}")
        else:
            st.warning(f"[문항 2] 감점/미통과 | 서로 다른 설명 방법을 활용하고 논리적으로 연결되어야 합니다.")

        # Q3 채점
        v_pass = check_keywords(q3_v, [["고여", "저수지", "정적"], ["이동하지", "멈추", "정지"]])
        a_pass = check_keywords(q3_a, [["고요", "정적", "소리 없는"], ["위험하지", "피해", "안전"]])
        
        if v_pass and a_pass:
            st.success("[문항 3] 조건 충족 (통과): 정전기의 특성(고여 있는 물/무위험성) 근거와 효과가 타당함.")
        else:
            st.error(f"[문항 3] 미통과 | 시각 연출 및 지문 근거 효과: {'통과' if v_pass else '미통과'}, 청각 연출 및 효과: {'통과' if a_pass else '미통과'}")

# ==============================================================================
# SET 3 채점 로직 및 UI
# ==============================================================================
with tab3:
    st.header("[실전 적용-3] 인공 지능이 그린 그림을 바라보는 시각")
    
    with st.expander("📌 모범 답안 및 평가 기준 보기"):
        st.markdown("""
        **[서·논술형 1]**  
        - (1) 완벽하게 피겨 스케이팅을 해내는 로봇  
        - (2) 감정도 느끼지 못하고 독자적 철학이나 이야기가 없으므로 예술이 아니다.  
        - (3) 미술계 변화 및 예술 범주 확장이라는 상징적 가치가 있음  
        **[서·논술형 2]**  
        - *옵션 A (인과+대조):* (1) AI는 감정이나 독자적 철학이 없으므로 예술로 보기 어렵다. (인과) (2) 그러나 예술의 범주를 확장한다는 점에서 상징적 가치가 있다. (비교와 대조)  
        - *옵션 B (예시+정의):* (1) 예를 들어 에드몽 드 벨라미는 고가에 판매되었으나 감정은 없다. (예시) (2) 진정한 예술이란 작가의 감정과 삶의 경험이 담긴 것을 의미한다. (정의)  
        **[서·논술형 3]**  
        - *시각:* 인간 선수가 땀흘리며 열정적 연기를 펼치고 관객이 열광하는 연출. (효과: 감정과 삶의 경험, 열정이 담긴 가치 강조)  
        - *청각:* 선수의 숨소리와 서정적 음악, 뜨거운 박수 소리. (효과: 감상자에게 남다른 감동과 마음의 울림 전달)
        """)

    st.subheader("1. [서·논술형 1] 표 채우기")
    q1_1 = st.text_input("3세트 (1) 답안", key="s3_q1_1")
    q1_2 = st.text_area("3세트 (2) 답안 (근거 포함)", key="s3_q1_2")
    q1_3 = st.text_area("3세트 (3) 답안", key="s3_q1_3")

    st.subheader("2. [서·논술형 2] 설명문 작성")
    q2_1 = st.text_input("3세트 (1) 문장 작성", key="s3_q2_1")
    q2_2 = st.text_input("3세트 (2) 문장 작성", key="s3_q2_2")

    st.subheader("3. [서·논술형 3] 영상 기획안")
    q3_v = st.text_area("3세트 시각 요소(Ⓐ) 및 효과", key="s3_q3_v")
    q3_a = st.text_area("3세트 청각 요소(Ⓑ) 및 효과", key="s3_q3_a")

    if st.button("3세트 답안 채점하기"):
        st.divider()
        st.markdown("### 📊 채점 결과")
        
        # Q1 채점
        q1_1_pass = check_keywords(q1_1, [["로봇", "피겨"]])
        q1_2_pass = check_keywords(q1_2, [["감정", "철학", "이야기", "경험"], ["아니다", "어렵다", "없다"]])
        q1_3_pass = check_keywords(q1_3, [["변화", "확장", "상징"]])

        if q1_1_pass and q1_2_pass and q1_3_pass:
            st.success("[문항 1] 정답 (만점)")
        else:
            st.error(f"[문항 1] 미통과 | (1): {'통과' if q1_1_pass else '미통과'}, (2)(근거포함): {'통과' if q1_2_pass else '미통과'}, (3): {'통과' if q1_3_pass else '미통과'}")

        # Q2 채점
        m1 = detect_explanation_methods(q2_1)
        m2 = detect_explanation_methods(q2_2)
        
        if len(m1) > 0 and len(m2) > 0 and set(m1) != set(m2):
            st.success(f"[문항 2] 조건 충족 (통과) | (1) 감지: {', '.join(m1)} / (2) 감지: {', '.join(m2)}")
        else:
            st.warning(f"[문항 2] 감점/미통과 | 서로 다른 설명 방법 사용 및 문장 간 자연스러운 논리 전환이 필요합니다.")

        # Q3 채점
        v_pass = check_keywords(q3_v, [["인간", "선수", "열정", "땀"], ["감정", "철학", "경험", "가치"]])
        a_pass = check_keywords(q3_a, [["숨소리", "박수", "환호", "서정적"], ["감동", "울림"]])
        
        if v_pass and a_pass:
            st.success("[문항 3] 조건 충족 (통과): 인간 예술의 본질적 가치와 감동/울림이라는 결론 방향이 타당함.")
        else:
            st.error(f"[문항 3] 미통과 | 시각 연출 및 근거 효과: {'통과' if v_pass else '미통과'}, 청각 연출 및 효과: {'통과' if a_pass else '미통과'}")