import datetime
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI


# =========================
# 1. State Definition
# =========================
class State(TypedDict):
    input: str
    plan: str
    execution: str
    final: str


# =========================
# 2. Gemini LLM
# =========================
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


# =========================
# 3. Agents (Nodes)
# =========================

# Planner Agent
def planner(state: State):
    prompt = f"""
    You are a planner agent.
    Break the following task into clear steps.

    Task:
    {state['input']}
    """
    response = llm.invoke(prompt)
    return {"plan": response.content}


# Executor Agent
def executor(state: State):
    prompt = f"""
    You are an executor agent.
    Execute the following plan step by step.

    Plan:
    {state['plan']}
    """
    response = llm.invoke(prompt)
    return {"execution": response.content}


# Reviewer Agent (Markdown formatter)
def reviewer(state: State):
    prompt = f"""
    You are a reviewer agent.

    Convert the following into a well-structured markdown document.

    Content:
    {state['execution']}

    Include:
    - Headings
    - Bullet points
    - Code blocks if needed
    """
    response = llm.invoke(prompt)
    return {"final": response.content}


# =========================
# 4. Save to Markdown
# =========================
def save_to_markdown(content: str):
    filename = f"output_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md"
    
    with open(filename, "w") as f:
        f.write("# AI Generated Report\n\n")
        f.write(f"**Generated on:** {datetime.datetime.now()}\n\n")
        f.write("---\n\n")
        f.write(content)

    print(f"\n Output saved to {filename}")


# =========================
# 5. Build Graph
# =========================
graph = StateGraph(State)

graph.add_node("planner", planner)
graph.add_node("executor", executor)
graph.add_node("reviewer", reviewer)

graph.add_edge(START, "planner")
graph.add_edge("planner", "executor")
graph.add_edge("executor", "reviewer")
graph.add_edge("reviewer", END)

app = graph.compile()


# =========================
# 6. Run
# =========================
if __name__ == "__main__":
    result = app.invoke({
        "input": "Explain the Indian Politics"
    })

    # print("\n=== FINAL OUTPUT ===\n")
    # print(result["final"])

    save_to_markdown(result["final"])

