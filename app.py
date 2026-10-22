import streamlit as st
import google.generativeai as genai

st.title("🤖 Google Gemini Free Chatbot")

# Streamlit secrets-ээс Gemini API түлхүүрийг унших
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Үнэгүй бөгөөд хурдан Gemini загварыг сонгох
model = genai.GenerativeModel("gemini-1.5-flash")

# Чатны түүхийг хадгалах санах ой
if "messages" not in st.session_state:
    st.session_state.messages = []

# Өмнөх мессежүүдийг дэлгэцэнд гаргах
for message in st.session_state.messages:
    # Gemini-ийн 'model' ролыг Streamlit дээр 'assistant' болгож харуулах
    role = "assistant" if message["role"] == "model" else message["role"]
    with st.chat_message(role):
        st.markdown(message["content"])

# Хэрэглэгч юм бичихэд ажиллах хэсэг
if prompt := st.chat_input("Юуны тухай ярилцах вэ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Gemini чат түүхийг бэлтгэх
        chat_history = [
            {
                "role": "user" if m["role"] == "user" else "model",
                "parts": [m["content"]]
            }
            for m in st.session_state.messages[:-1]
        ]
        
        # Хиймэл оюунаас хариу авах
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(prompt)
        
        st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "content": response.text})
