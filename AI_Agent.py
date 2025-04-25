from dotenv import load_dotenv
load_dotenv()

# Step_1 : Setup API Keys for Groq, OpenAI and Tavily
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY  = os.environ.get("TAVILY_API_KEY")

# Step_2 : Setup LLM & Tools
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

# Step_3 : Setup AI Agent with Search tool functionality

from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

system_prompt = "Act as an AI chatbot who is smart and friendly"

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt):
    try:
        llm = ChatGroq(model = llm_id, api_key=GROQ_API_KEY)
        tools = [TavilySearchResults(max_results=2, api_key=TAVILY_API_KEY)] if allow_search else []
        
        agent = create_react_agent(
            model = llm,
            tools = tools,
            state_modifier = system_prompt
        )

        state = {"messages" : query}
        response = agent.invoke(state)
        messages = response.get("messages")
        ai_messages = [message.content for message in messages if isinstance(message,AIMessage)]
        return (ai_messages[-1]) if ai_messages else "❌ No AI response received."
    
    except Exception as e:
        print("❌ Error in agent.invoke:", e)
        return {"error": str(e)}