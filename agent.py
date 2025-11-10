from langchain.agents import AgentExecutor
from langchain.agents.tool_calling import create_tool_calling_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

from tools.email_tool import fetch_emails
from tools.calendar_tool import get_events
from tools.news_tool import get_headlines


def run_agent(prompt):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    tools = [
        Tool(name="Fetch Emails", func=fetch_emails, description="Fetch latest emails."),
        Tool(name="Calendar", func=get_events, description="List today's events."),
        Tool(name="News", func=get_headlines, description="Get top news."),
    ]

    agent = create_tool_calling_agent(llm=llm, tools=tools)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    result = agent_executor.invoke({"input": prompt})
    return result["output"]
