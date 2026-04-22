import streamlit as st
import requests

st.title("AI Chat Assitant !")

API_URL = "http://127.0.0.1:8000/api/chat"  #put "yourlocahost/api/chat"

user_input = st.chat_input("What's up ?")

# store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input:

    # add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # instantly render user message (fixes "delay feeling")
    with st.chat_message("user"):
        st.write(user_input)

    # assistant placeholder (so UI feels instant)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.write("Thinking...")

    #connection to backend
    try:
        response = requests.post(
            API_URL,
            json={"messages": st.session_state.messages[-10:]},  # slight optimization
            timeout=30
        )

        #handling response
        if response.status_code == 200:
            bot_reply = response.json()["response"]
        else:
            bot_reply = f"Error {response.status_code}: {response.text}"

    except Exception as e:
        bot_reply = f"Connection error: {str(e)}"

    # update assistant message in-place
    placeholder.write(bot_reply)

    # add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})