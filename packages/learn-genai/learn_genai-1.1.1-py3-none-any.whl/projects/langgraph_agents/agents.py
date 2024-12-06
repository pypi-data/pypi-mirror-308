from langgraph.graph import Graph, END
<<<<<<< HEAD
from langchain_community.chat_models import ChatOllama
=======
from langchain.chat_models import ChatOllama
>>>>>>> 0ffe8c014fd8dd028d766a214e6e7213eea2a3ff
from langchain.schema import HumanMessage, AIMessage
from typing import TypedDict, Annotated, Sequence

class AgentState(TypedDict):
    messages: Annotated[Sequence[str], "The messages in the conversation"]
    next: Annotated[str, "The next agent to use"]

def create_researcher(llm):
    def researcher(state):
        messages = state['messages']
        result = llm.invoke(messages + [HumanMessage(content="Act as a researcher and provide relevant information for the given topic.")])
        return {
            "messages": messages + [AIMessage(content=f"Researcher: {result.content}")],
            "next": "writer"
        }
    return researcher

def create_writer(llm):
    def writer(state):
        messages = state['messages']
        result = llm.invoke(messages + [HumanMessage(content="Act as a writer and create a concise summary based on the researcher's information.")])
        return {
            "messages": messages + [AIMessage(content=f"Writer: {result.content}")],
            "next": END
        }
    return writer

def create_agent_chain(llm):
    workflow = Graph()

    workflow.add_node("researcher", create_researcher(llm))
    workflow.add_node("writer", create_writer(llm))

    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "writer")

    return workflow.compile()

# Example usage
if __name__ == "__main__":
    llm = ChatOllama(model="llama2:3b")
    chain = create_agent_chain(llm)
    
    result = chain.invoke({
        "messages": [HumanMessage(content="Explain the importance of renewable energy.")],
        "next": "researcher"
    })
    
    for message in result['messages']:
        print(message.content)
