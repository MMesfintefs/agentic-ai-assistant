from langchain.agents import create_react_agent
from langchain.agents.react.base import DocstoreExplorer
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

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
    # Use the new LangChain 0.2.x agent factory
    agent = create_react_agent(llm, tools)
    return agent.invoke(prompt)
