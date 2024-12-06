import streamlit as st
from typing import TypedDict, List, Dict, Annotated
from langgraph.graph import StateGraph, END
from langchain.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseMessage

class AgentState(TypedDict):
    messages: List[BaseMessage]
    next_agent: str

def create_agent(name: str, system_message: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "{input}"),
    ])
    return prompt | ChatOllama(model="llama2:3b")

researcher = create_agent(
    "Researcher",
    "You are a research agent. Your job is to find relevant information and pass it to the writer."
)

writer = create_agent(
    "Writer",
    "You are a writer agent. Your job is to take the research provided and create a concise summary."
)

def route(state: AgentState) -> Dict:
    if state["next_agent"] == "Writer":
        return {"Writer": state}
    elif state["next_agent"] == "Researcher":
        return {"Researcher": state}
    else:
        return END

def run_langgraph_agents():
    st.header("LangGraph Agents")

    workflow = StateGraph(AgentState)

    workflow.add_node("Researcher", researcher)
    workflow.add_node("Writer", writer)

    workflow.set_entry_point("Researcher")

    workflow.add_edge("Researcher", route)
    workflow.add_edge("Writer", route)

    app = workflow.compile()

    topic = st.text_input("Enter a topic for the agents to research and summarize:")
    
    if st.button("Run Agents"):
        if topic:
            with st.spinner("Agents are working..."):
                result = app.invoke({
                    "messages": [],
                    "next_agent": "Researcher",
                    "input": f"Research the topic: {topic}"
                })
                st.subheader("Research and Summary:")
                for message in result['messages']:
                    st.write(f"{message.type}: {message.content}")
        else:
            st.warning("Please enter a topic for the agents to work on.")
