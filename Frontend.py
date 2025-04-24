from dotenv import load_dotenv
load_dotenv()

# Step_1 : Setup UI with streamlit (model provider, model, system prompt, web search query)
import streamlit as st
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title="LangGraph Agent UI", layout="centered")

# Define the function to load Lottie animations
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_ai = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_kkflmtur.json")
st_lottie(lottie_ai, height=200)

st.title("AI Chatbot Agents")
st.write("Create and Interact with the AI Agents!")

system_prompt = st.text_area("Define your AI Agents : ", height=68, placeholder="Type your system prompt here...")

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mistral-saba-24b"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

provider = st.radio("Select Provider : ", ("Groq", "OpenAI"))

if provider == "Groq":
    select_model = st.selectbox("Select Groq Model :", MODEL_NAMES_GROQ)
elif provider == "OpenAI":
    select_model = st.selectbox("Select OpenAI Model :", MODEL_NAMES_OPENAI)

allow_web_search = st.checkbox("Allow Web Search")

user_query = st.text_area("Enter you query :", height=150, placeholder="Ask Anything!")

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask Agnet!"):
    if user_query.strip():
        # Step_2 : Connect with backend via URL
    
        payload = {
            "model_name" : select_model,
            "model_provider" : provider,
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

                        st.subheader("🤖 Agent Response")
                        st.markdown(final_response)

                    # Feedback section
                    feedback = st.radio("Was this helpful?", ["👍 Yes", "👎 No"], horizontal=True)
                    # Export option
                    st.download_button(
                        label = "📄 Download Response",
                        data = response_data,
                        file_name = "agent_response.txt",
                        mime = "text/plain"
                )
                else:
                    st.error(f"🚫 Server error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Backend connection error: {e}")
