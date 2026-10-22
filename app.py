import streamlit as st
from google import genai

st.title("🤖 Google Gemini Free Chatbot")

# Streamlit secrets-ээс Gemini API түлхүүрийг уншиж клиент үүсгэх
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Чатны түүхийг хадгалах санах ой
if "messages" not in st.session_state:
    st.session_state.messages = []

# Өмнөх мессежүүдийг дэлгэцэнд гаргах
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Хэрэглэгч юм бичихэд ажиллах хэсэг
if prompt := st.chat_input("Юуны тухай ярилцах вэ?"):
    # Хэрэглэгчийн мессежийг хадгалж харуулах
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Өмнөх түүхийг Gemini-д тохирох хэлбэрт оруулах
            formatted_history = [
                {"role": m["role"], "parts": [m["content"]]} 
                for m in st.session_state.messages[:-1]
            ]
            
            # Чат сесс эхлүүлж хариу авах (gemini-2.5-flash эсвэл gemini-1.5-flash)
            chat = client.chats.create(model="gemini-1.5-flash", history=formatted_history)
            response = chat.send_message(prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "content": response.text})
            
        except Exception as e:
            st.error(st.error(f"Алдаа гарлаа: {e}"))
        
