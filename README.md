Yes. Now that you have provided the **actual agent files**, I can match the README to your implementation instead of guessing.

Your `agents/` folder is implementing a **specialized multi-agent workflow** with:

* `router.py` → decides which agent should handle the request
* `learning_agent.py` → teaches DSA concepts
* `practice_agent.py` → provides practice problems
* `hint_agent.py` → gives guided hints
* `solution_agent.py` → provides complete solutions
* `code_review_agent.py` → reviews student code using RAG
* `critic_agent.py` → verifies the generated answer and controls the reasoning/retry loop

Below is the **updated README section/content specifically based on the code you provided**, using the **What → Why → How** format.

# 🧠 DSA Coach Agent

An AI-powered **Data Structures and Algorithms learning, practice, code-review, and assessment assistant** built using Python, Streamlit, Gemini, PostgreSQL, pgvector, RAG, and a specialized multi-agent architecture.

The system is designed to work as an **AI DSA tutor and evaluator** rather than a simple question-answering chatbot.

It uses specialized agents for different student requirements and combines them with:

* Retrieval-Augmented Generation (RAG)
* Intent-based agent routing
* Code review
* Automated evaluation
* Critic-based verification
* Reasoning/retry loop
* Conversation persistence
* Vector search
* Interactive Streamlit UI

---

# 📌 Table of Contents

* [1. Project Overview](#1-project-overview)
* [2. What is DSA Coach Agent?](#2-what-is-dsa-coach-agent)
* [3. Why was it developed?](#3-why-was-it-developed)
* [4. How does it work?](#4-how-does-it-work)
* [5. ](#5-qualification-requirements)
* [6. Agent-Based Architecture](#6-agent-based-architecture)
* [7. Agents Folder](#7-agents-folder)
* [8. Router Agent](#8-router-agent)
* [9. Learning Agent](#9-learning-agent)
* [10. Practice Agent](#10-practice-agent)
* [11. Hint Agent](#11-hint-agent)
* [12. Solution Agent](#12-solution-agent)
* [13. Code Review Agent](#13-code-review-agent)
* [14. Critic Agent](#14-critic-agent)
* [15. Reasoning and Verification Loop](#15-reasoning-and-verification-loop)
* [16. Rubric Generator and Evaluation](#16-rubric-generator-and-evaluation)
* [17. Retrieval-Augmented Generation](#17-retrieval-augmented-generation)
* [18. Student Code Review Workflow](#18-student-code-review-workflow)
* [19. Streamlit UI](#19-streamlit-ui)
* [20. Database](#20-database)
* [21. Project Structure](#21-project-structure)
* [22. Technology Stack](#22-technology-stack)
* [23. Installation](#23-installation)
* [24. Configuration](#24-configuration)
* [25. Running the Application](#25-running-the-application)
* [26. Future Improvements](#26-future-improvements)

---

# 1. Project Overview

## What?

**DSA Coach Agent** is an AI-powered educational application that helps students learn, practice, solve, debug, and review Data Structures and Algorithms problems.

The system provides different capabilities depending on what the student asks for.

It supports:

* DSA concept learning
* Practice problem generation
* Hints
* Complete solutions
* Code review
* Debugging assistance
* Complexity analysis
* Context-aware answers
* Retrieval-Augmented Generation
* Automated answer verification
* Student conversation history

---

## Why?

A normal chatbot generally uses one prompt and one LLM response for every request.

That approach does not provide enough control for an educational system.

For example:

```text
"Explain Binary Search"
```

requires teaching.

Whereas:

```text
"Give me a Binary Search problem"
```

requires practice generation.

And:

```text
"Give me a hint"
```

should not reveal the complete solution.

Similarly:

```text
"Review my code"
```

requires code analysis rather than a normal explanation.

Therefore, DSA Coach uses **specialized agents**, where each agent has a clearly defined responsibility.

---

## How?

The application follows an agent-based workflow:

```text
                     Student
                        │
                        ▼
                  Streamlit UI
                        │
                        ▼
                   User Request
                        │
                        ▼
                  Router Agent
                        │
       ┌────────────────┼────────────────┐
       │                │                │
       ▼                ▼                ▼
   Learning          Practice          Hint
    Agent             Agent           Agent
       │                │                │
       ├────────────────┼────────────────┤
       │                │                │
       ▼                ▼                ▼
   Solution        Code Review       Other Flow
    Agent             Agent
       │                │
       └────────────┬───┘
                    ▼
                Draft Answer
                    │
                    ▼
               Critic Agent
                    │
             ┌──────┴──────┐
             │             │
            PASS          RETRY
             │             │
             ▼             ▼
        Final Answer   Regenerate
```

This provides a controlled multi-agent workflow.

---

# 2. What is DSA Coach Agent?

## What?

DSA Coach Agent is an AI tutor that helps students understand DSA concepts and improve their problem-solving skills.

The system uses Gemini as the language model and RAG to provide relevant project-specific knowledge.

The specialized agent layer determines **what kind of help the student needs** and selects the appropriate agent.

---

## Why?

Different learning activities require different response strategies.

For example:

| Student Requirement       | Agent             |
| ------------------------- | ----------------- |
| Learn a concept           | Learning Agent    |
| Get a coding problem      | Practice Agent    |
| Student is stuck          | Hint Agent        |
| Wants complete answer     | Solution Agent    |
| Wants code reviewed       | Code Review Agent |
| Verify generated response | Critic Agent      |

This separation improves control and makes the system easier to extend.

---

## How?

The user interacts through Streamlit.

The request is passed into the agent workflow.

The router identifies the intent and sends the request to the appropriate specialized agent.

The selected agent retrieves relevant information from RAG where required and generates a draft response using Gemini.

The draft can then pass through the critic/reasoning loop before the final answer is returned.

---

# 3. Why was it developed?

## What problem does it solve?

Students often struggle with:

* Understanding DSA concepts
* Choosing the correct algorithm
* Knowing how to start a problem
* Debugging code
* Understanding complexity
* Knowing whether their solution is efficient
* Understanding why their solution is incorrect

---

## Why an AI Agent?

An AI agent can dynamically decide what type of assistance is appropriate.

Instead of providing the answer immediately, the system can behave like a tutor:

```text
Learn → Practice → Hint → Attempt → Review → Improve
```

This makes the learning process more interactive.

---

# 4. How does it work?

The complete workflow is:

```text
Student
   │
   ▼
Streamlit
   │
   ▼
State
   │
   ▼
Router
   │
   ├── Learning Agent
   ├── Practice Agent
   ├── Hint Agent
   ├── Solution Agent
   └── Code Review Agent
              │
              ▼
             RAG
              │
              ▼
        Relevant Context
              │
              ▼
          Gemini LLM
              │
              ▼
         Draft Response
              │
              ▼
         Critic Agent
              │
       ┌──────┴──────┐
       │             │
      PASS          RETRY
       │             │
       ▼             ▼
   Final Answer    New Draft
```

---

# 5. Agent Implementation

The project contains multiple specialized agents under:

```text
agents/
```

The agents have separate responsibilities.

The architecture therefore follows an **agent-oriented design** instead of placing all functionality inside one LLM function.

---

## Agent-Based Workflow

The implementation contains:

```text
Router
   ↓
Specialized Agent
   ↓
RAG / LLM
   ↓
Draft
   ↓
Critic
   ↓
Final Response
```

This is particularly important for demonstrating the project's agentic nature.

---

## LangGraph / Agent Workflow

The agent functions operate on a shared `state` dictionary.

For example:

```python
def learning_agent(state):
    question = state.get("question", "")
```

and:

```python
def critic_agent(state):
    draft = state.get("draft_response", "")
```

This state-based design makes the agents suitable for orchestration through a graph-based workflow such as LangGraph.

---

# 6. Agent-Based Architecture

## What?

The `agents` package contains specialized components responsible for different DSA tasks.

---

## Why?

Separating responsibilities provides:

* Better modularity
* Easier debugging
* Easier testing
* Clear responsibilities
* Easier future expansion
* Better control over LLM behavior

---

## How?

Each agent receives a shared `state`.

For example:

```text
state
├── question
├── mode
├── topic
├── difficulty
├── user_id
├── student_code
├── draft_response
├── critique
├── needs_retry
└── loop_count
```

An agent reads the information it needs and returns an updated state.

---

# 7. Agents Folder

The agent components are organized inside:

```text
agents/
```

The folder contains specialized agents such as:

```text
agents/
│
├── __init__.py
├── router.py
├── learning_agent.py
├── practice_agent.py
├── hint_agent.py
├── solution_agent.py
├── code_review_agent.py
└── critic_agent.py
```

Additional agent components such as the rubric/evaluation workflow can also be integrated into this architecture.

---

# 8. Router Agent

## What?

The `router.py` file contains the request-routing logic.

Its main function is:

```python
route_intent(state)
```

The router determines which specialized agent should handle the request.

---

## Why?

Without a router, every request would have to be handled by the same agent.

The router allows the system to select the correct workflow automatically.

For example:

```text
"Teach me stacks"
        ↓
Learning Agent
```

while:

```text
"Give me a stack problem"
        ↓
Practice Agent
```

---

## How?

The router first checks the sidebar mode.

The sidebar mode has the highest priority.

For example:

```python
mode_mapping = {
    "learn": "learn",
    "practice": "practice",
    "hint": "hint",
    "solution": "solution",
    "code_review": "code_review",
}
```

If a valid mode is supplied, the router immediately returns the corresponding intent.

If there is no valid mode, the router performs automatic keyword-based detection.

For example:

```python
if any(word in question for word in [
    "review",
    "debug",
    "error",
    "wrong answer",
    "bug",
]):
    return {"intent": "code_review"}
```

Therefore, the router supports both:

1. Explicit user-selected modes
2. Automatic intent detection

---

# 9. Learning Agent

## What?

`learning_agent.py` implements the Learning Agent.

Its responsibility is to **teach DSA concepts**.

---

## Why?

A student learning a concept needs an explanation rather than a coding problem or a complete solution.

The Learning Agent is specifically instructed to behave as a teacher.

---

## How?

The agent extracts:

```python
question
topic
difficulty
user_id
```

from the state.

It then calls:

```python
retrieve_context(
    question=question,
    mode="learn",
    topic=topic,
    difficulty=difficulty,
    user_id=user_id,
    include_code=False,
    include_leetcode=False,
    include_stories=True,
)
```

This means the Learning Agent can retrieve educational material and stories.

The retrieved context is then supplied to Gemini.

The prompt instructs the model to:

* Explain intuition first
* Give examples
* Explain operations
* Include complexity
* Use analogies when useful
* Avoid unrelated problems
* Behave as a teacher

The generated response is returned as:

```python
{
    "draft_response": response.text
}
```

---

# 10. Practice Agent

## What?

`practice_agent.py` implements the Practice Agent.

Its responsibility is to provide the student with a DSA problem to solve.

---

## Why?

Practice requires a different behavior from learning.

The agent should challenge the student rather than immediately explaining the solution.

---

## How?

The Practice Agent retrieves problem-related context:

```python
retrieve_context(
    question=question,
    mode="practice",
    topic=topic,
    difficulty=difficulty,
    user_id=user_id,
    include_code=False,
    include_leetcode=True,
    include_stories=False,
)
```

It specifically enables LeetCode/problem retrieval.

The prompt instructs the agent to:

* Give one suitable problem
* Match the requested topic
* Mention difficulty
* Explain the problem
* Provide examples
* Provide constraints
* Avoid complete solutions
* Ask the student to attempt the problem

The expected structure is:

```text
## Problem

## Example

## Constraints

## Your Task
```

This ensures that the Practice Agent behaves differently from the Solution Agent.

---

# 11. Hint Agent

## What?

`hint_agent.py` provides hints to students who are stuck.

---

## Why?

Giving the complete solution immediately reduces the learning value of the practice process.

The Hint Agent therefore provides guidance without revealing the final answer.

---

## How?

The agent first checks whether student code is available.

If code exists, it is added to the retrieval query:

```python
retrieval_question = question

if student_code:
    retrieval_question += "\n\nStudent's code:\n" + student_code
```

The agent retrieves:

```python
include_code=bool(student_code)
include_leetcode=True
include_stories=False
```

The prompt specifically instructs Gemini to:

* Give a small hint
* Focus on the student's difficulty
* Avoid complete code
* Avoid directly revealing the algorithm
* Encourage the student to think about the next step

The response begins with:

```text
### Hint
```

This creates a guided-learning experience.

---

# 12. Solution Agent

## What?

`solution_agent.py` handles requests where the student explicitly wants the complete solution.

---

## Why?

A student may first attempt a problem, request a hint, and eventually ask for the full solution.

The Solution Agent is responsible for providing that complete explanation.

---

## How?

The agent retrieves relevant problem knowledge:

```python
retrieve_context(
    question=question,
    mode="solution",
    topic=topic,
    difficulty=difficulty,
    user_id=user_id,
    include_code=False,
    include_leetcode=True,
    include_stories=False,
)
```

The prompt requires:

1. Problem identification
2. Approach
3. Algorithm
4. Complete code
5. Code explanation
6. Time complexity
7. Space complexity
8. Edge cases

The response follows:

```text
## Approach

## Algorithm

## Code

## Explanation

## Complexity

## Edge Cases
```

Unlike the Practice and Hint Agents, this agent is explicitly allowed to provide the complete solution.

---

# 13. Code Review Agent

## What?

`code_review_agent.py` reviews the student's actual submitted code.

---

## Why?

Students need feedback on their own implementations, not just generic explanations.

The Code Review Agent can analyze:

* Correctness
* Implementation
* Bugs
* Complexity
* Optimization
* Code quality

---

## How?

The agent extracts:

```python
question
topic
difficulty
user_id
student_code
```

If no code is supplied, it returns:

```text
## Code Review

Please provide your code so I can review it.
```

If code exists, it creates a retrieval query containing both the student's question and code:

```python
retrieval_question = f"""
Student question:
{question}

Student code:
{student_code}
"""
```

It then calls:

```python
retrieve_context(
    question=retrieval_question,
    mode="code_review",
    topic=topic,
    difficulty=difficulty,
    user_id=user_id,
    include_code=True,
    include_leetcode=False,
    include_stories=False,
)
```

This is important because the Code Review Agent retrieves **student-code-related context** rather than unrelated educational material.

The retrieved context is then passed to Gemini along with the student's code.

---

# 14. Critic Agent

## What?

`critic_agent.py` implements the verification component of the system.

It acts as a **Critic Agent** that evaluates the draft generated by another agent.

---

## Why?

An LLM-generated response can contain:

* Incorrect technical information
* Incorrect complexity analysis
* Missing information
* Contradictions
* Unclear explanations

Instead of immediately returning the first generated answer, the system can ask another LLM call to critique it.

This provides an additional verification stage.

---

## How?

The Critic Agent receives:

```python
draft = state.get("draft_response", "")
question = state.get("question", "")
loop_count = state.get("loop_count", 0)
```

It then asks Gemini to check:

```text
1. Is the answer technically correct?
2. Does it answer the question?
3. Are time and space complexities correct?
4. Is the explanation clear?
5. Does it contain unsupported or contradictory information?
```

The critic must return:

```text
PASS
```

or:

```text
RETRY: <short reason>
```

The code checks:

```python
retry = critique.upper().startswith("RETRY")
```

Therefore:

```text
PASS
   ↓
Continue

RETRY
   ↓
Generate another draft
```

---

# 15. Reasoning and Verification Loop

## What?

The Critic Agent forms the core of the project's **reasoning/verification loop**.

The system does not have to accept the first generated answer immediately.

It can evaluate the draft and decide whether another generation attempt is required.

---

## Why?

The verification loop improves reliability.

For example:

```text
User:
Explain the complexity of this solution.
```

The first generated answer may incorrectly claim:

```text
Time Complexity: O(n²)
```

The Critic Agent can detect that the complexity is incorrect and return:

```text
RETRY: Time complexity is incorrect.
```

The workflow can then regenerate the response.

---

## How?

The loop works conceptually as:

```text
                User Request
                     │
                     ▼
                  Router
                     │
                     ▼
             Specialized Agent
                     │
                     ▼
              Draft Response
                     │
                     ▼
                Critic Agent
                     │
              ┌──────┴──────┐
              │             │
            PASS           RETRY
              │             │
              ▼             ▼
        Final Response   Generate Again
                            │
                            ▼
                         Critic
```

The loop count is stored in the state:

```python
loop_count = state.get("loop_count", 0)
```

The system also uses:

```python
MAX_REASONING_LOOPS
```

to prevent unlimited retries.

The implementation therefore has a safety boundary:

```python
if loop_count >= MAX_REASONING_LOOPS:
    retry = False
```

This prevents the system from continuously regenerating responses.

---

# 16. Rubric Generator and Evaluation

## What?

The rubric/evaluation component provides structured assessment of student solutions.

The Rubric Generator creates criteria against which a student's code can be evaluated.

The Evaluator then uses those criteria to assess the submission.

---

## Why?

An LLM should not simply be told:

```text
"Give this student a score."
```

A structured rubric provides a more consistent evaluation process.

Possible criteria include:

```text
Correctness
Time Complexity
Space Complexity
Code Quality
Edge Cases
Optimization
```

---

## How?

The assessment workflow can be represented as:

```text
Student Code
     │
     ▼
Problem Context
     │
     ▼
Rubric Generator
     │
     ▼
Evaluation Criteria
     │
     ▼
Evaluator
     │
     ▼
Critic / Verification
     │
     ▼
Student Feedback
```

This complements the Code Review Agent.

The Code Review Agent focuses on understanding and reviewing the student's code, while the rubric/evaluation layer provides a structured way to assess it.

---

# 17. Retrieval-Augmented Generation

## What?

RAG allows the agents to retrieve relevant information from the DSA knowledge base before generating their responses.

The project uses:

* PostgreSQL
* pgvector
* BGE embeddings
* Semantic search

---

## Why?

Without RAG, the agents depend primarily on the general knowledge of the LLM.

RAG allows the application to ground responses in project-specific content.

---

## How?

The agent sends a retrieval request:

```python
result = retrieve_context(...)
```

The returned context is extracted using:

```python
context = result.get("context", "")
```

That context is then included in the Gemini prompt.

For example:

```text
Question
   ↓
Agent
   ↓
retrieve_context()
   ↓
Relevant DSA Knowledge
   ↓
Gemini
   ↓
Draft Response
```

Different agents use different retrieval configurations.

### Learning Agent

```text
Stories: YES
LeetCode: NO
Student Code: NO
```

### Practice Agent

```text
Stories: NO
LeetCode: YES
Student Code: NO
```

### Hint Agent

```text
Stories: NO
LeetCode: YES
Student Code: optional
```

### Solution Agent

```text
Stories: NO
LeetCode: YES
Student Code: NO
```

### Code Review Agent

```text
Stories: NO
LeetCode: NO
Student Code: YES
```

This shows that the RAG layer is **agent-aware** rather than being used identically for every request.

---

# 18. Student Code Review Workflow

The complete code-review workflow is:

```text
Student Uploads Code
        │
        ▼
Code Review Request
        │
        ▼
Router
        │
        ▼
Code Review Agent
        │
        ▼
Retrieve Relevant Context
        │
        ▼
Analyze Student Code
        │
        ▼
Generate Draft Review
        │
        ▼
Rubric / Evaluator
        │
        ▼
Critic Agent
        │
        ├── PASS
        │
        └── RETRY
              │
              ▼
        Improved Review
              │
              ▼
        Final Feedback
```

This makes code review an agent-based assessment workflow rather than a single prompt.

---

# 19. Streamlit UI

## What?

The Streamlit application provides the user interface.

---

## Why?

Students need a simple interface for interacting with the different agents.

Instead of manually selecting Python functions, the student can choose a mode and submit a question.

---

## How?

The UI can expose modes such as:

```text
Learn DSA
Practice
Get Hint
View Solution
Code Review
```

The selected mode is placed into the state.

The router gives explicit sidebar mode priority.

Therefore:

```text
Sidebar Selection
        ↓
Router
        ↓
Correct Agent
```

This ensures predictable behavior.

---

# 20. Database

## What?

PostgreSQL is used for persistent storage.

pgvector is used for vector similarity search.

---

## Why?

The project requires persistent storage for:

* RAG chunks
* Embeddings
* Search history
* Conversations
* Student-related information

---

## How?

The RAG data is stored as vector embeddings.

The embedding model used by the project is:

```text
BAAI/bge-small-en-v1.5
```

with:

```text
Embedding Dimension = 384
```

The retrieval layer searches these vectors to identify relevant knowledge.

---

# 21. Project Structure

The project is organized approximately as:

```text
DSA-Coach-Agent/
│
├── agents/
│   ├── __init__.py
│   ├── router.py
│   ├── learning_agent.py
│   ├── practice_agent.py
│   ├── hint_agent.py
│   ├── solution_agent.py
│   ├── code_review_agent.py
│   └── critic_agent.py
│
├── app.py
├── coach.py
├── rag.py
├── ingest.py
├── database.py
├── config.py
├── evaluator.py
├── rubric_generator.py
├── create_tables.sql
├── requirements.txt
├── README.md
├── .gitignore
├── .env
├── data/
   └── notes/
   ├── stories/
   ├── leetcode.json
   └── descriptions/
```

---

# 22. Technology Stack

| Technology                 | Purpose                      |
| -------------------------- | ---------------------------- |
| Python                     | Main programming language    |
| Streamlit                  | Interactive UI               |
| Gemini                     | LLM generation and critique  |
| Agent Architecture         | Specialized task processing  |
| LangGraph-compatible State | Agent workflow orchestration |
| RAG                        | Context retrieval            |
| PostgreSQL                 | Persistent database          |
| pgvector                   | Vector similarity search     |
| BGE                        | Text embeddings              |
| LangChain                  | Document processing          |
| Git/GitHub                 | Version control              |
| Docker                     | Containerization             |

---

# 23. Installation

## What?

The project requires Python, PostgreSQL, pgvector, and the required Python packages.

---

## How?

Create a virtual environment:

```bash
python -m venv .myenv
```

Activate it on Windows:

```bash
.myenv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 24. Configuration

Create a `.env` file in the project root.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

The `.env` file should not be committed to GitHub.

Add:

```gitignore
.env
```

to `.gitignore`.

---

# 25. Running the Application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in the browser.

The student can then select:

```text
Learn DSA
Practice
Get Hint
View Solution
Code Review
```

and interact with the corresponding agent.

---

# 26. Future Improvements

The current architecture can be extended with:

* Full LangGraph state graph
* More specialized agents
* Advanced rubric evaluation
* Automated test execution
* Student performance tracking
* Adaptive difficulty
* Personalized learning paths
* More programming languages
* Instructor dashboard
* Authentication
* Docker Compose
* Cloud deployment
* Automated agent evaluation
* Better retry and verification strategies

---

# 🏁 Conclusion

DSA Coach Agent is designed as an **agent-based AI learning and assessment system**.

Its architecture separates different responsibilities into specialized agents:

```text
                 DSA Coach
                     │
                   Router
                     │
       ┌─────────────┼─────────────┐
       │             │             │
    Learning      Practice       Hint
     Agent         Agent         Agent
       │             │             │
       └─────────────┼─────────────┘
                     │
              Solution Agent
                     │
              Code Review Agent
                     │
                     ▼
              Draft Response
                     │
                     ▼
                Critic Agent
                     │
              ┌──────┴──────┐
              │             │
            PASS          RETRY
              │             │
              ▼             ▼
        Final Answer    Regenerate
```

The most important aspect of the architecture is that **different agents have different responsibilities and different RAG configurations**.

The system therefore demonstrates:

* Specialized agent implementation
* Intent-based routing
* State-based agent communication
* RAG integration
* Code-review capability
* Rubric-based evaluation
* Critic-based verification
* Reasoning/retry loop
* Persistent storage
* Interactive UI

This makes DSA Coach more than a basic LLM chatbot. It is an **agent-oriented DSA learning, practice, code-review, and assessment platform**.
