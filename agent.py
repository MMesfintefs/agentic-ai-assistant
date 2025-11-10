from langchain.agents import initialize_agent
from langchain.tools import Tool
from langchain.chat_models import ChatOpenAI
from tools.email_tool import fetch_emails
from tools.calendar_tool import get_events
from tools.news_tool import get_headlines

def run_agent(prompt):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [
        Tool(name="Fetch Emails", func=fetch_emails, description="Fetch latest emails."),
        Tool(name="Calendar", func=get_events, description="List today’s events."),
        Tool(name="News", func=get_headlines, description="Get top news.")
    ]
    agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description")
    return agent.run(prompt)
