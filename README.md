# What is Langgraph?

LangGraph is a framework for building **stateful, multi-step AI workflows using a graph-based architecture**, where each node represents a task (like calling an LLM or a tool) and edges define how the system transitions between steps, enabling loops, branching, and persistent memory across the workflow.

# Difference between Langchain and Langgraph

> **LangChain = building blocks**
> 
> 
> **LangGraph = workflow engine using those blocks**
> 

---

## Core Difference

### LangChain

- A **framework to build LLM-powered apps**
- You connect:
    - LLMs (OpenAI, Claude, etc.)
    - Tools (APIs, DBs, search)
    - Memory
- Works mostly in a **linear / chain-based flow**

Example:

```
User → Prompt → LLM → Tool → LLM → Output
```

---

### LangGraph

- Built **on top of LangChain**
- Designed for **stateful, multi-step, agent workflows**
- Uses a **graph structure**
    - Nodes = tasks
    - Edges = decisions / transitions
- Supports **loops, branching, retries, memory across steps**

Example:

```
Start → Plan → Execute → Check → (loop if needed) → Final Answer
```

---

## Key Differences Side-by-Side

| Feature | LangChain | LangGraph |
| --- | --- | --- |
| Architecture | Linear chains | Graph (nodes + edges) |
| Complexity | Simple to moderate | Moderate to complex |
| State management | Limited | Strong (persistent state) |
| Loops / retries | Hard | Native support |
| Agents | Basic agents | Advanced agent workflows |
| Control | Less control | Fine-grained control |

---

# When to Use What

### Use LangChain if:

- You are building:
    - Simple chatbot
    - RAG (retrieval-based QA)
    - One-shot or few-step pipelines
- You want **quick development**

---

### Use LangGraph if:

- You need:
    - Multi-step reasoning agents
    - Planning + execution loops
    - Error handling / retries
    - Complex workflows (like AutoGPT-style systems)

---

## Real-World Analogy

- **LangChain** → Like writing a **script**
- **LangGraph** → Like designing a **flowchart with decisions and loops**

---

## Simple Example

### LangChain

```
chain=prompt|llm
```

### LangGraph

```
graph:
plan→execute→verify
↑↓
└──retry──┘
```

# Implementation

In this demo, we’re going to see two versions of an AI workflow built using LangGraph with Google Gemini.

First, we’ll look at a simple single-agent setup, where one LLM handles the entire request from input to output in a single step.

Then, we’ll move to a more advanced multi-agent workflow, where the same task is broken down into stages like planning, execution, and review, with each step handled by a specialized agent.

This will help us understand how we can evolve from a basic LLM call to a more structured and scalable workflow using LangGraph.

# Version 1:

## Step 1: Setup Environment

### 1. Create project folder

```
mkdir langgraph-project
cd langgraph-project
```

### 2. Create virtual environment

```
python3-m venv venv
source venv/bin/activate# Linux/Mac
```

### 3. Install LangGraph and gemini

```
pip install-U langgraph
```

```python
pip install langchain-google-genai
```

## Step 2: Add API Key

You need an LLM (Gemini or others).

```python
export GEMINI_API_KEY=AIzaSyAB-RN6IJVwzWA4hxu2tRcQGJcGzqVNY9Q
export GOOGLE_API_KEY=AIzaSyAB-RN6IJVwzWA4hxu2tRcQGJcGzqVNY9Q
```

## Step 3: Understand Core Concept

LangGraph works like this:

- **State** → data passed between steps
- **Node** → function (task)
- **Edge** → flow (what runs next)

---

## Step 4: Build Your First LangGraph App

Create file:

```
touch app.py
```

### Code:

Here, we are using LangGraph, but only with a single node. Even though it is structured as a graph, it behaves like a simple LLM call where input goes in and output comes out without intermediate processing.

`app.py`

```python
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
```

---

> [!TIP]
>
>This code implements a basic workflow using LangGraph with Google Gemini:
>
>```python
>User → chatbot → Output
>```
>
>There is only one agent (chatbot) handling the entire task.
>
>---
>
># 1. Imports
>
>```
>from langgraph.graph import StateGraph,START,END
>```
>
>Imports core LangGraph components:
>
>- `StateGraph`: The workflow engine used to define and run the graph
>- `START`: Entry point of the workflow
>- `END`: Exit point of the workflow
>
>---
>
>```
>fromtypingimportTypedDict
>```
>
>Used to define a structured state object. This ensures the data passed between nodes has a defined schema.
>
>---
>
>```
>fromlangchain_google_genaiimportChatGoogleGenerativeAI
>```
>
>Imports the integration for interacting with the Gemini LLM.
>
>---
>
># 2. State Definition
>
>```
>classState(TypedDict):
>input:str
>output:str
>```
>
>Defines the structure of the data flowing through the graph.
>
>Fields:
>
>- `input`: The user’s query
>- `output`: The model’s response
>
>Unlike the multi-agent version, there are no intermediate fields such as plan or execution.
>
>---
>
># 3. LLM Initialization
>
>```
>llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
>```
>
>Initializes the Gemini model.
>
>- This object is used to send prompts to the LLM
>- `llm.invoke()` is the method that triggers inference
>
>---
>
># 4. Single Agent (Node)
>
>```
>def chatbot(state:State):
>```
>
>Defines the only node in the graph. It takes the current state as input.
>
>---
>
>```
>response=llm.invoke(state["input"])
>```
>
>Sends the user input directly to the LLM.
>
>- No preprocessing
>- No decomposition
>- No intermediate reasoning
>
>---
>
>```
>return {"output":response.content}
>```
>
>Returns a dictionary that updates the state with the output field.
>
>Flow at this stage:
>
>input → LLM → output
>
>---
>
># 5. Build Graph
>
>```
>graph=StateGraph(State)
>```
>
>Creates a new graph using the defined state structure.
>
>---
>
>```
>graph.add_node("chatbot",chatbot)
>```
>
>Adds a single node named "chatbot" and maps it to the chatbot function.
>
>---
>
>```
>graph.add_edge(START,"chatbot")
>```
>
>Defines that execution begins at the chatbot node.
>
>---
>
>```
>graph.add_edge("chatbot",END)
>```
>
>Defines that after chatbot execution, the workflow terminates.
>
>Final graph structure:
>
>START → chatbot → END
>
>---
>
>```
>app=graph.compile()
>```
>
>Compiles the graph into an executable application.
>
>---
>
># 6. Run
>
>```
>result=app.invoke({"input":"Explain Kubernetes simply"})
>```
>
>Executes the workflow.
>
>Initial state:
>
>```
>{"input":"..."}
>```
>
>After execution:
>
>```
>{"input":"...","output":"..."}
>```
>
>---
>
>```
>print(result["output"])
>```
>
>Prints the final result to the terminal.
>
>---
>
># Internal Execution Flow
>
>1. Input enters the graph
>2. It is passed to the chatbot node
>3. The Gemini model generates a response
>4. The response is stored in the state
>5. The final state is returned
>
>---
>
># Key Difference from Multi-Agent Version
>
>| Feature | Single-Agent Code | Multi-Agent Code |
>| --- | --- | --- |
>| Agents | 1 | 3 (planner, executor, reviewer) |
>| Steps | Single-step | Multi-step |
>| State | Simple | Rich (plan, execution, final) |
>| Reasoning | Direct | Structured |
>| Output Quality | Basic | Refined |
>
>---
>
># Summary
>
>This is a single-agent workflow where one LLM processes the entire request in a single step without decomposition or intermediate reasoning.
>
>---


## Step 5: Run It

```
python3 app.py
```

You’ll get:

```
Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
Imagine you're running a giant online store. This store isn't just one big program; it's made up of many smaller pieces: one piece for showing products, another for handling payments, another for managing user accounts, etc.

Now, imagine these challenges:

1.  **Deployment:** How do you get all these pieces (which are code) onto the actual computers (servers) that run your store?
2.  **Scaling:** What if suddenly a million people visit your store? You need more "copies" of certain pieces to handle the load. What if traffic drops? You want to reduce copies to save money.
3.  **Self-Healing:** What if one of your payment processing pieces crashes? You need it restarted automatically, or replaced, so customers can still pay.
4.  **Updates:** How do you update one piece of your store without taking the whole store offline?
5.  **Resource Management:** How do you make sure each piece gets enough CPU, memory, and storage without wasting resources?

Doing all this manually for dozens or hundreds of application pieces across many servers is a nightmare.

---

**That's where Kubernetes comes in!**

Think of Kubernetes as a highly intelligent, automated **"city manager" or "orchestra conductor" for your software applications.**

Here's how it works simply:

1.  **Containers (The Standardized Boxes):** First, your applications are packaged into standardized units called **"containers"** (like Docker containers). You can think of these as **standardized shipping containers**. Each container holds a piece of your application and everything it needs to run (code, libraries, settings). This makes them portable and consistent.

2.  **Kubernetes' Job (The Manager):** Kubernetes' job is to take these shipping containers (your app parts) and **figure out where to place them** across all your available servers (the 'ships' or 'trucks' in our logistics network).

Here's what it *does* automatically:

*   **Automated Deployment:** You tell Kubernetes, "I need 3 copies of my product catalog container and 2 copies of my payment processing container." Kubernetes finds the best servers to run them on and launches them.
*   **Scaling:** If your online store suddenly gets busy (Black Friday!), Kubernetes can **automatically create more copies of your app's containers** and distribute them to handle the increased load. When traffic drops, it scales them back down.
*   **Self-Healing:** If a part of your application crashes or a server goes down, Kubernetes notices. It will **automatically replace the broken container** or move it to a healthy server, ensuring your store stays online.
*   **Load Balancing:** It ensures that incoming requests to your application are **evenly distributed** among all the healthy copies of your containers.
*   **Rolling Updates:** When you want to update your app to a new version, Kubernetes can do it **gradually, replacing old containers with new ones one by one**, ensuring your app stays online the whole time without downtime.
*   **Resource Management:** It intelligently allocates CPU, memory, and storage to your containers, making sure they have what they need without wasting resources.

**In short:**

Kubernetes automates the deployment, scaling, and management of containerized applications. It takes away a lot of the manual, repetitive, and error-prone work involved in running modern software, allowing developers to focus on writing great code, and ensuring applications are always available and performing well.

It's like having a super-smart, tireless logistics manager and city planner for all your software.
..............
```

The first file is a **basic workflow built using LangGraph**, where a single node (`chatbot`) directly takes user input, sends it to **Google Gemini**, and returns a response. This represents a **single-agent system**, where one LLM handles the entire task from start to finish without breaking it into steps.

In contrast, the multi-agent version expands this into a **structured workflow of multiple specialized agents**—such as a planner, executor, and reviewer—where each node has a specific responsibility. Instead of one LLM doing everything, the task is **decomposed, processed step-by-step, and refined**, with data flowing through a shared state across nodes. This demonstrates the real power of LangGraph: **orchestrating multiple intelligent agents with defined roles and controlled execution flow**, rather than just making a single LLM call.

# Version 2:

Create a new file

`main.py`

```python
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
        "input": "Explain how to deploy a Docker container on Kubernetes"
    })

    # print("\n=== FINAL OUTPUT ===\n")
    # print(result["final"])

    save_to_markdown(result["final"])

```

> [!INFO]
>
>This whole script builds a **multi-agent workflow using LangGraph** with **Google Gemini**:
>
>```
>User → Planner → Executor → Reviewer → Markdown File
>```
>
>Each step:
>
>- reads **state**
>- modifies it
>- passes it forward
>
>---
>
>## 1. Imports
>
>```
>importdatetime
>```
>
>→ Imports Python’s built-in module to work with **date & time**
>
>Used later to:
>
>- timestamp files
>- create unique filenames
>
>---
>
>```
>fromlanggraph.graphimportStateGraph,START,END
>```
>
>→ From LangGraph:
>
>- `StateGraph` → main workflow engine
>- `START` → entry point of graph
>- `END` → exit point
>
>Think:
>
>```
>START → your nodes → END
>```
>
>---
>
>```
>fromtypingimportTypedDict
>```
>
>→ Used to define a **structured state (data schema)**
>
>Instead of random dictionaries, you define:
>
>- what fields exist
>- their types
>
>---
>
>```
>fromlangchain_google_genaiimportChatGoogleGenerativeAI
>```
>
>→  This connects your code to **Gemini LLM**
>
>---
>
>## 2. State Definition
>
>```
>classState(TypedDict):
>input:str
>plan:str
>execution:str
>final:str
>```
>
>→ This is **VERY IMPORTANT**
>
>It defines the **data flowing between agents**
>
>### What each field means:
>
>| Field | Purpose |
>| --- | --- |
>| `input` | User query |
>| `plan` | Output from planner |
>| `execution` | Output from executor |
>| `final` | Final polished output |
>
>---
>
>→ Think of this as a **shared memory object**
>
>Each agent:
>
>- reads from it
>- writes to it
>
>---
>
>## 3. LLM Initialization
>
>```
>llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
>```
>
>👉 Creates a connection to Gemini
>
>- `gemini-2.5-flash` → fast + efficient model
>- `llm.invoke()` → sends prompt to model
>
>---
>
>## 4. Agents (Nodes)
>
>Each function = **one node in graph**
>
>---
>
>### Planner
>
>```
>defplanner(state:State):
>```
>
>→ Takes current state as input
>
>---
>
>```
>prompt=f"""
>...
>{state['input']}
>"""
>```
>
>→ Builds prompt using:
>
>- user input from state
>
>---
>
>```
>response=llm.invoke(prompt)
>```
>
>→ Sends prompt to Gemini
>
>---
>
>```
>return {"plan":response.content}
>```
>
>→ Updates state:
>
>- adds `plan`
>
>---
>
>**Result:**
>
>```
>input → planner → plan created
>```
>
>---
>
>### Executor
>
>```
>defexecutor(state:State):
>```
>
>→ Receives updated state
>
>---
>
>```
>{state['plan']}
>```
>
>→ Uses planner output
>
>---
>
>```
>return {"execution":response.content}
>```
>
>→ Adds execution result to state
>
>---
>
>Result:
>
>```
>plan → executor → execution
>```
>
>---
>
>### Reviewer
>
>```
>defreviewer(state:State):
>```
>
>→ Final agent
>
>---
>
>```
>{state['execution']}
>```
>
>→ Uses execution output
>
>---
>
>```
>return {"final":response.content}
>```
>
>→ Produces final polished markdown
>
>---
>
>Result:
>
>```
>execution → reviewer → final output
>```
>
>---
>
>## 5. Save to Markdown
>
>```
>defsave_to_markdown(content:str):
>```
>
>→ Function to store final result
>
>---
>
>```
>filename=f"output_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md"
>```
>
>→ Creates **unique filename**
>
>Example:
>
>```
>output_2026-04-06_05-45-10.md
>```
>
>---
>
>```
>withopen(filename,"w")asf:
>```
>
>→ Opens file in **write mode**
>
>---
>
>```
>f.write("# AI Generated Report\n\n")
>```
>
>→ Adds Markdown heading
>
>---
>
>```
>f.write(f"**Generated on:**{datetime.datetime.now()}\n\n")
>```
>
>→ Adds timestamp
>
>---
>
>```
>f.write(content)
>```
>
>→ Writes final LLM output
>
>---
>
>```
>print(f"\n Output saved to{filename}")
>```
>
>→ Confirms file creation
>
>---
>
>## 6. Build Graph
>
>```
>graph=StateGraph(State)
>```
>
>→ Creates workflow with defined state
>
>---
>
>```
>graph.add_node("planner",planner)
>```
>
>→ Adds node:
>
>- name = "planner"
>- function = planner()
>
>Same for executor & reviewer
>
>---
>
>```
>graph.add_edge(START,"planner")
>```
>
>→ Defines flow start
>
>---
>
>```
>graph.add_edge("planner","executor")
>graph.add_edge("executor","reviewer")
>```
>
>→ Defines sequence
>
>---
>
>```
>graph.add_edge("reviewer",END)
>```
>
>→ Ends workflow
>
>---
>
>### Final Flow:
>
>```
>START → planner → executor → reviewer → END
>```
>
>---
>
>```
>app=graph.compile()
>```
>
>→ Converts graph into executable app
>
>---
>
>## 7. Run the Workflow
>
>```
>if__name__=="__main__":
>```
>
>→ Ensures code runs only when script is executed directly
>
>---
>
>```
>result=app.invoke({
>"input":"Explain how to deploy a Docker container on Kubernetes"
>})
>```
>
>→ Starts execution
>
>- initial state = `{input: ...}`
>- rest fields get filled step-by-step
>
>---
>
>### Internally:
>
>```
>input
> ↓
>planner → adds plan
> ↓
>executor → adds execution
> ↓
>reviewer → adds final
>```
>
>---
>
>```
>save_to_markdown(result["final"])
>```
>
>→ Saves final output to file
>
>---
>
># Summary
>
>### What this code demonstrates:
>
>- Multi-agent system
>- State passing between agents
>- Sequential workflow
>- Role-based LLM usage
>- File output


Run:

```python
python3 main.py
```

Expected Output:

```python
 Output saved to output_2026-04-06_07-27-13.md
```

Run `ls`  to verify

```python
ls
app.py  main.py  output_2026-04-06_07-27-13.md
```

Lets change the topic and see.

Change the input in the run section

```python
# =========================
# 6. Run
# =========================
if __name__ == "__main__":
    result = app.invoke({
        "input": "Explain the Indian Politics"
    })
```

Verify:

```python
 Output saved to output_2026-04-06_07-42-37.md
```

```python
ls
app.py  main.py  output_2026-04-06_07-27-13.md  output_2026-04-06_07-42-37.md
```