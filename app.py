from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Define State
class State(TypedDict):
    input: str
    output: str

# 2. Initialize Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# 3. Define node
def chatbot(state: State):
    response = llm.invoke(state["input"])
    return {"output": response.content}

# 4. Build graph
graph = StateGraph(State)

graph.add_node("chatbot", chatbot)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

# 5. Compile
app = graph.compile()

# 6. Run
result = app.invoke({"input": "Explain Kubernetes simply"})
print(result["output"])
