def main():
    from dotenv import load_dotenv
    load_dotenv()

    # Step_1 : Setup UI with streamlit (model provider, model, system prompt, web search query)
    import requests
    import streamlit as st
    from streamlit_lottie import st_lottie

    # ---------- Page Configuration ----------
    st.set_page_config(
        page_title="LangGraph AI Chatbot",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # ----------------- CUSTOM CSS ------------------
    st.markdown(
        """
        <style>
            body {
                background-color: #111827;
                color: #d1d5db;
                font-family: 'Segoe UI', sans-serif;
            }
            .sidebar-content {
                background-color: #1f2937;
                padding: 20px;
            }
            .chat-message {
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 10px;
                font-size: 16px;
            }
            .user-message {
                background-color: #374151;
            }
            .bot-message {
                background-color: #4b5563;
            }
            .avatar {
                width: 30px;
                height: 30px;
                border-radius: 50%;
                margin-right: 10px;
            }
            button[kind="primary"] {
                background-color: #10b981;
                color: white;
                border-radius: 10px;
                border: none;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ---------- Lottie Animation ----------
    def load_lottie_url(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_ai = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_kkflmtur.json")
    st_lottie(lottie_ai, height=200)


    # ---------- Avatar Config ----------
    USER_AVATAR = "https://cdn-icons-png.flaticon.com/512/9131/9131529.png"
    AGENT_AVATAR = "https://cdn-icons-png.flaticon.com/512/4712/4712100.png"


    # ---------- Title and Prompt ----------
    st.title("AI Chatbot")
    st.caption("Ask your AI agent anything — powered by Groq and LangGraph!")

    # ---------- Initialize Session State ----------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ---------- Inputs ----------
    MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "llama3-70b-8192"]
    system_prompt = st.text_area("Define your AI Agent : ", height=68, placeholder="Type your system prompt here...")
    select_model  = st.selectbox("Select Model  (Groq Only) : ", MODEL_NAMES_GROQ)
    allow_web_search = st.checkbox("Allow Web Search")
    user_query = st.text_area("Enter you query :", height=150, placeholder="Ask Anything!")

    API_URL = "https://ai-agent-backend-uzhn.onrender.com/chat"

    # ---------- Chat History Display ----------
    for entry in st.session_state.chat_history:
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(entry["user"])
        with st.chat_message("assistant", avatar=AGENT_AVATAR):
            st.markdown(entry["agent"])

    # ---------- Submit Button ----------
    if st.button("Ask Agent!"):
        if user_query.strip():
            # Step_2 : Connect with backend via URL
        
            payload = {
                "model_name" : select_model,
                "system_prompt" : system_prompt,
                "messages" : [user_query],
                "allow_search" : allow_web_search
            }
            with st.spinner("Thinking... 💭"):
                try:
                    response = requests.post(API_URL, json=payload)

                    if response.status_code == 200:
                        try:
                            response_data = response.json()
                        except ValueError:
                            st.error("⚠️ Unable to parse the server response.")
                            response_data = {"response": response.text}

                        if isinstance(response_data, dict) and "error" in response_data:
                                st.error(response_data["error"])
                        else:
                            final_response = (
                                response_data if isinstance(response_data, str)
                                else response_data .get("response", str(response_data))
                            )

                        # Display new message
                        with st.chat_message("user", avatar=USER_AVATAR):
                            st.markdown(user_query)
                        with st.chat_message("assistant", avatar=AGENT_AVATAR):
                            st.markdown(final_response)

                        # Feedback section
                        feedback = st.radio("Was this helpful?", ["👍 Yes", "👎 No"], horizontal=True)
                        # Export option
                        st.download_button(
                            label = "📄 Download Response",
                            data = final_response,
                            file_name = "agent_response.txt",
                            mime = "text/plain"
                    )
                    else:
                        st.error(f"🚫 Server error: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Backend connection error: {e}")


# End of main
if __name__ == "__main__":
    main()
