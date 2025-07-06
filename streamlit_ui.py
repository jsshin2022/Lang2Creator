
import streamlit as st
import requests

st.set_page_config(page_title="Lang2Creator Streamlit UI", layout="wide")
st.title("🎙️ Lang2Creator AI Assistant")

query = st.chat_input("무엇이 궁금하신가요? 예: Creator_001의 썸네일 보여줘")

if query:
    with st.chat_message("user"):
        st.markdown(query)

    try:
        payload = {"user": "jinsoo", "text": query}
        response = requests.post("http://localhost:8000/ask", json=payload)
        result = response.json()

        with st.chat_message("assistant"):
            if "error" in result:
                st.error(result["error"])
            elif "thumbnail" in result:
                st.image(result["thumbnail"], caption=result.get("title", "썸네일"))
                st.markdown(f"[🔗 영상 보러가기]({result['url']})")
            elif "views" in result:
                st.write(f"📊 {result['creator']}의 조회수")
                df = result["views"]
                st.line_chart({v["date"]: v["views"] for v in df})
            else:
                st.json(result)
    except Exception as e:
        st.error(f"요청 처리 중 오류 발생: {e}")
