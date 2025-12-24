import streamlit as st
from openai import OpenAI

# --- API KEY ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- 페이지 설정 ---
st.set_page_config(page_title="영어 문장 만들기")
st.title("📘 영어 문장 만들기")

# --- 입력 영역 ---
word = st.text_input(
    "문장 생성에 사용할 영단어",
    placeholder="vacation"
) or "vacation"

school_levels = ["중1", "중2", "중3", "고1", "고2", "고3"]
level = st.selectbox("대상 학교급 / 학년(어휘 수준)", school_levels)

words_per_sentence = st.text_input(
    "문장당 단어 수",
    placeholder="8"
) or "8"

# --- 문법 요소 목록 (selectbox) ---
grammar_options = [
    "현재시제",
    "과거시제",
    "미래시제 (will / be going to)",
    "현재진행형",
    "현재완료",

    "조동사 can / could",
    "조동사 may / might",
    "조동사 must / have to",
    "조동사 should",

    "의문문",
    "부정문",
    "명령문",

    "접속사 because",
    "접속사 when / while",
    "조건문 if",

    "관계대명사 who / which / that",

    "비교급",
    "최상급",
    "as ~ as",

    "to부정사 (목적)",
    "동명사 (~ing)",

    "수동태 (be + p.p.)",

    "가정법 과거 (If I were~)"
]

grammar = st.selectbox(
    "사용할 문법 요소 선택",
    grammar_options
)

# --- Lexile 매핑 ---
level_to_lexile_map = {
    "중1": "Lexile=600L~800L",
    "중2": "Lexile=700L~900L",
    "중3": "Lexile=800L~1000L",
    "고1": "Lexile=1000L~1150L",
    "고2": "Lexile=1100L~1200L",
    "고3": "Lexile=1200L~1300L",
}

# --- 실행 버튼 ---
if st.button("✏️ 문장 만들기"):
    lexile_level = level_to_lexile_map[level]

    prompt = (
        f"영단어 {word}를 반드시 사용하고, "
        f"{level} 수준({lexile_level})에 맞추어 "
        f"{grammar} 문법을 적용한 영어 문장 3개를 생성하시오. "
        f"각 문장은 정확히 {words_per_sentence}단어로 구성하시오."
    )

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": (
                    "문장 생성만 수행할 것. "
                    "각 문장은 번호를 붙일 것. "
                    "지정된 영단어는 **bold** 처리할 것. "
                    "다른 설명이나 해설은 하지 말 것."
                )
            },
            {"role": "user", "content": prompt},
        ]
    )

    st.subheader("✅ 생성된 문장")
    st.write(response.choices[0].message.content)
