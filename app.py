import streamlit as st
from openai import OpenAI

st.title("🤖 Миний Анхны Чатбот")

# Нууцлалаас API түлхүүрийг дуудаж байна
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Надаас ямар нэгэн зүйл асуугаарай..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        reply = response.choices[0].message.content
        st.markdown(reply)
        
    st.session_state.messages.append({"role": "assistant", "content": reply})