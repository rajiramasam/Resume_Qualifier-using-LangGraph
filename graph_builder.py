from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from langchain.schema import HumanMessage
from llm_setup import llm  # Use Gemini or OpenAI here
from typing import TypedDict,Optional

class GraphState(TypedDict): #sharedstate
    resume:Optional[str]
    qualified:Optional[bool]
    message:Optional[str] 
def check_qualification(state):
    resume = state["resume"]
    prompt = f"""Based on this resume, is the candidate qualified for a Software development job?
Answer only YES or NO.\n\n{resume}"""
    response = llm.invoke([HumanMessage(content=prompt)])
    qualified = "YES" in response.content.upper()
    return {"resume": resume, "qualified": qualified}

def write_positive(state):
    resume = state["resume"]
    prompt = f"""Write a positive reply for this qualified candidate:\n{resume}"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"message": response.content}

def write_rejection(state):
    resume = state["resume"]
    prompt = f"Politely reject this candidate:\n{resume}"
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"message": response.content}

def route_decision(state):
    return "positive feedback" if state["qualified"] else "rejection message"

def build_graph():
    builder = StateGraph(GraphState)
    builder.add_node("check qualification", RunnableLambda(check_qualification))
    builder.add_node("positive feedback", RunnableLambda(write_positive))
    builder.add_node("rejection message", RunnableLambda(write_rejection))
    builder.set_entry_point("check qualification")
    builder.add_conditional_edges("check qualification", route_decision)
    return builder.compile()
