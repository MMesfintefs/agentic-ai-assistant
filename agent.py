from langchain_community.agent_toolkits import create_react_agent
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

    # Proper creation method in langchain_community>=0.2.x
    agent = create_react_agent(llm=llm, tools=tools)
    result = agent.invoke(prompt)
    return result
