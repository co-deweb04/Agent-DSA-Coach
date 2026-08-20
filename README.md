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

* 1. Project Overview
* 2. What is DSA Coach Agent?
* 3. Why was it developed?
* 4. How does it work?
* 5. Agent Implementation
* 6. Agent-Based Architecture
* 7. Agents Folder
* 8. Router Agent
* 9. Learning Agent
* 10. Practice Agent
* 11. Hint Agent
* 12. Solution Agent
* 13. Code Review Agent
* 14. Critic Agent
* 15. Reasoning and Verification Loop
* 16. Graph and Agent Orchestration
* 17. Shared State
* 18. Conversation Management
* 19. Data Organization
* 20. LeetCode Dataset
* 21. Student Uploads
* 22. Rubric Generator and Evaluation
* 23. Retrieval-Augmented Generation
* 24. Student Code Review Workflow
* 25. Streamlit UI
* 26. Database
* 27. Containerization
* 28. Dockerfile
* 29. .dockerignore
* 30. docker-compose.yml
* 31. Complete Project Structure
* 32. Technology Stack
* 33. Installation
* 34. Configuration
* 35. Running the Application
* 36. Overall System Architecture
* 37. Future Improvements
* 38. Conclusion

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

The system combines an LLM with RAG and multiple specialized agents to provide different types of assistance depending on the student's request.

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
Shared State
   │
   ▼
Graph / Orchestrator
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
        ┌─────┴─────┐
        │           │
       PASS        RETRY
        │           │
        ▼           ▼
   Final Answer  Regenerate
```

This provides a controlled multi-agent workflow.

---

# 2. What is DSA Coach Agent?

## What?

DSA Coach Agent is an AI tutor that helps students understand DSA concepts and improve their problem-solving skills.

The system uses Gemini as the language model and RAG to provide relevant project-specific knowledge.

The specialized agent layer determines **what kind of help the student needs** and selects the appropriate agent.

It combines:

AI + RAG + Specialized Agents + Database + UI

to create an interactive learning environment.

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

A single LLM prompt cannot easily enforce different behaviors for all these situations. An AI agent can dynamically decide what type of assistance is appropriate.

Instead of providing the answer immediately, the system can behave like a tutor:

```text
Learning Agent
→ Explain the concept.

Practice Agent
→ Give a problem without solving it.

Hint Agent
→ Give guidance without revealing the solution.

Solution Agent
→ Provide the complete solution.

Code Review Agent
→ Analyze the student's actual code.

Critic Agent
→ Verify the generated response.
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
Graph
   │
   ▼
Router
   │
   ▼
Specialized Agent
   │
   ▼
RAG Retrieval
   │
   ▼
Gemini
   │
   ▼
Draft Response
   │
   ▼
Critic
   │
   ├── PASS
   │
   └── RETRY
        │
        ▼
     Regenerate
        │
        ▼
      Critic
        │
        ▼
   Final Response
```
The workflow can also integrate:

Rubric Generator
        ↓
Evaluator
        ↓
Student Feedback

and:

Conversation
        ↓
PostgreSQL

for persistent learning history

---

# 5. Agent Implementation

The project contains multiple specialized agents under:

```text
agents/
├── __init__.py
├── router.py
├── learning_agent.py
├── practice_agent.py
├── hint_agent.py
├── solution_agent.py
├── code_review_agent.py
└── critic_agent.py
```

Each agent has a specific responsibility.

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

The project follows a specialized multi-agent architecture.

                    DSA Coach
                        │
                      Router
                        │
       ┌────────────────┼────────────────┐
       │                │                │
       ▼                ▼                ▼
    Learning         Practice          Hint
     Agent            Agent           Agent
       │                │                │
       └────────────────┼────────────────┘
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
       Solution Agent      Code Review Agent
              │                   │
              └─────────┬─────────┘
                        │
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

The architecture separates responsibilities and makes individual agents easier to modify and test.

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
## What?

The agent components are organized inside:

```text
agents/
```

The agents/ directory contains the specialized AI agents and routing logic:

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

Why?

Separating agents provides:

Modularity
Clear responsibilities
Easier debugging
Easier testing
Better prompt control
Easier future expansion

How?

Each agent receives the workflow state, performs its specialized task, and returns an updated state.

The Router determines which agent should execute.

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

The mapping includes:

```python
mode_mapping = {
    "learn": "learn",
    "learn dsa": "learn",
    "practice": "practice",
    "hint": "hint",
    "get hint": "hint",
    "solution": "solution",
    "view solution": "solution",
    "code_review": "code_review",
    "code review": "code_review",
}
```

If a valid mode is supplied, the router immediately returns the corresponding intent.

If there is no valid mode, the router performs automatic keyword-based intent detection.

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

The Learning Agent is explicitly instructed to behave as a teacher.

---

## How?

The agent retrieves:

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

This means the Learning Agent can retrieve educational knowledge and stories.

The retrieved context is then supplied to Gemini.

The Gemini prompt instructs the agent to:

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

The agent should challenge the student rather than immediately explaining the solution therefore avoids giving complete solutions.

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

* Give one suitable DSA problem
* Match the requested topic
* Mention difficulty
* Explain the problem
* Provide examples
* Provide constraints
* Avoid complete solutions
* Avoid revealing the algorithm.
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

A student may first attempt a problem, request a hint, and eventually need the complete explanation.

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

It acts as a **Critic Agent** that verifies the draft generated by another agent.

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

The maximum number of loops is controlled by:

```python
MAX_REASONING_LOOPS
```
This prevents unlimited retries.

---

# 15. Reasoning and Verification Loop

## What?

The Critic Agent forms the core of the project's **reasoning/verification loop**.

The system does not have to accept the first generated answer immediately.

It can evaluate the draft and decide whether another generation attempt is required.

---

## Why?

The verification loop improves reliability of LLM-generated responses.

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

# 16. Graph and Agent Orchestration
## What?

graph.py defines the workflow connecting the different agents.

It acts as the orchestration layer of the multi-agent system.

## Why?

A multi-agent application needs to control:

Which agent runs
In what order agents execute
What state is passed between agents
When the critic runs
When a retry happens
When the workflow ends

graph.py provides a centralized place for this workflow.

## How?

The conceptual workflow is:

                 User Request
                      │
                      ▼
                   Router
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
       Learning    Practice      Hint
        Agent       Agent        Agent
          │           │           │
          └───────────┼───────────┘
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
       Solution Agent    Code Review Agent
             │                 │
             └────────┬────────┘
                      │
                      ▼
                 Draft Response
                      │
                      ▼
                 Critic Agent
                      │
                ┌─────┴─────┐
                │           │
              PASS         RETRY
                │           │
                ▼           ▼
             Final       Regenerate

The graph therefore acts as the central control layer.

---

# 17. Shared State
## What?

state.py defines the shared state used by the agent workflow.

The state stores information required by different agents.

Typical values include:

question
mode
intent
topic
difficulty
user_id
student_code
draft_response
critique
needs_retry
loop_count

## Why?

Different agents need different information.

For example:

Router
→ question + mode


Learning Agent
→ question + topic + difficulty


Code Review Agent
→ question + student_code + topic


Critic Agent
→ question + draft_response + loop_count

A shared state structure makes communication easier.

## How?

The state moves through the workflow:

User
 ↓
State
 ↓
Router
 ↓
Agent
 ↓
Updated State
 ↓
Critic
 ↓
Updated State
 ↓
Final Response

This allows agents to remain independent while participating in one workflow.

---

# 18. Conversation Management
## What?

conversation.py manages persistent conversations and messages.

Typical operations include:

```python
create_conversation()
save_message()
get_messages()
get_conversations()
```

## Why?

Conversation persistence allows students to:

Continue previous discussions
Review previous questions
Revisit explanations
Continue solving problems
Maintain learning history

This makes DSA Coach more useful as a long-term learning assistant.

## How?

A conversation can be created:

```python
conversation_id = create_conversation(
    "Two Sum Discussion"
)
```
A message can be stored:

```python
save_message(
    conversation_id,
    "user",
    "Explain Two Sum"
)
```

Messages can later be retrieved:

```python
get_messages(conversation_id)
```

The flow is:

Student
   ↓
Question
   ↓
Agent Workflow
   ↓
Response
   ↓
conversation.py
   ↓
PostgreSQL

---

# 19. Data Organization
## What?

The data/ directory contains the knowledge sources used by the RAG pipeline.

data/
├── notes/
├── stories/
├── descriptions/
└── leetcode.json

## Why?

Keeping all knowledge resources under one directory makes the project:

Easier to maintain
Easier to ingest
Easier to expand
Better organized

Different types of knowledge can also be retrieved according to the agent's purpose.

## How?

The ingestion pipeline processes these resources.

The general flow is:

Data Files
   ↓
Document Processing
   ↓
Text Splitting
   ↓
Embeddings
   ↓
PostgreSQL + pgvector
   ↓
Semantic Retrieval
   ↓
Agents

---

# 20. LeetCode Dataset
## What?

data/leetcode.json contains structured DSA practice problems.

A record may contain information such as:

{
    "title": "Two Sum",
    "difficulty": "Easy",
    "topic": "Array",
    "description": "...",
    "examples": [],
    "constraints": []
}

The exact fields depend on the project's dataset.

## Why?

A structured problem dataset makes it easier to:

Retrieve coding problems
Filter by topic
Filter by difficulty
Generate practice questions
Generate solutions
Populate the RAG knowledge base

## How?

The ingestion pipeline can process the JSON file:

leetcode.json
      ↓
Document
      ↓
Chunking
      ↓
BGE Embedding
      ↓
pgvector
      ↓
Semantic Retrieval
      ↓
Practice / Solution Agent

The Practice Agent enables:

```python
include_leetcode=True
```

The Solution Agent also enables:

```python
include_leetcode=True
```
---

# 21. Student Uploads
## What?

The uploads/ directory stores files submitted by students.

uploads/
├── py/
└── ipynb/

## Why?

Students can submit DSA solutions in different formats.

The project supports:

Python source files
Jupyter Notebook files

Separating these formats makes file processing and organization easier.

## How?

The upload workflow is:

Student Upload
      ↓
File Type Detection
      ↓
┌─────┴─────┐
│           │
.py        .ipynb
│           │
▼           ▼
uploads/py  uploads/ipynb
│           │
└─────┬─────┘
      ↓
Student Code
      ↓
Code Review Agent
---

# 22. Rubric Generator and Evaluation

## What?

The project contains:

rubric_generator.py
evaluator.py

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

# 23. Retrieval-Augmented Generation

## What?

RAG (Retrieval-Augmented Generation) allows the agents to retrieve relevant information from the DSA knowledge base before generating their responses.Instead of relying only on the LLM's internal knowledge.

The project uses:

* PostgreSQL
* pgvector
* BGE (BAAI General Embedding) embeddings
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

The general workflow is:

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

# 24. Student Code Review Workflow

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
Gemini
        │
        ▼
Draft Review
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
        Evaluation
              │
              ▼
        Student Feedback
```

This makes code review an agent-based assessment workflow rather than a single prompt.

The system can support both .py and .ipynb submissions.

---

# 25. Streamlit UI

## What?

The Streamlit application provides the interactive user interface for DSA Coach.

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

The flow is:

```text
Streamlit
    ↓
Selected Mode
    ↓
State
    ↓
Router
    ↓
Specialized Agent
```
This ensures predictable behavior.

---

# 26. Database

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

The RAG pipeline generates embeddings using:

```text
BAAI/bge-small-en-v1.5
```

with:

```text
Embedding Dimension = 384
```

The embeddings are stored in PostgreSQL using pgvector.

The retrieval process then performs semantic similarity search.

---

# 27. Containerization
## What?

The project supports containerized deployment using Docker.

The main containerization files are:

Dockerfile
.dockerignore
docker-compose.yml

## Why?

Containerization provides:

Reproducible environments
Easier deployment
Easier team collaboration
Consistent dependencies
Simplified service management

## How?

The application and database can run as separate services.

Docker Compose
      │
 ┌────┴────┐
 │         │
 ▼         ▼
App       DB
 │         │
 │      pgvector
 │         │
 └────┬────┘
      │
   Database

---

# 28. Dockerfile
## What?

The Dockerfile defines how to build the DSA Coach application image.

## Why?

The Dockerfile packages:

Python runtime
Project files
Dependencies
Application configuration

into a reproducible environment.

This avoids environment differences between machines.

## How?

The typical build process is:

Python Base Image
       ↓
Working Directory
       ↓
Copy requirements.txt
       ↓
Install Dependencies
       ↓
Copy Project Files
       ↓
Expose Port
       ↓
Start Streamlit

The image can be built using:

```bash
docker build -t dsa-coach .
```
---

# 29. .dockerignore
## What?

.dockerignore specifies files that should not be copied into the Docker build context.

## Why?

Excluding unnecessary files:

-Reduces build size
-Improves build speed
-Keeps the image clean
-Helps prevent sensitive configuration from being copied

## How?

Typical entries include:

.myenv
.venv
__pycache__
*.pyc
.env
.git
.gitignore
uploads

Docker will ignore these files when creating the build context.

---

# 30. docker-compose.yml
## What?

docker-compose.yml defines the services required by the project and how they communicate.

The main services are:

DSA Coach Application
PostgreSQL + pgvector

## Why?

Docker Compose simplifies:

-Service startup
-Networking
-Port management
-Environment configuration
-Database connectivity
-Multi-container deployment

It is particularly useful for the project's containerization requirement.

## How?

A typical setup can define:

```YAML
services:

  app:
    build: .
    ports:
      - "8501:8501"
    depends_on:
      - db


  db:
    image: pgvector/pgvector:pg16
    ports:
      - "5432:5432"
```

The exact database credentials and environment variables should match the project's configuration.

The services can be started using:

```bash
docker compose up --build
```
---

# 31.📁 Project Structure

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
├── data/
│   ├── notes/
│   │   └── DSA knowledge files
│   │
│   ├── stories/
│   │   └── DSA story-based explanations
│   │
│   ├── descriptions/
│   │   └── DSA problem descriptions
│   │
│   └── leetcode.json
│
├── uploads/
│   ├── py/
│   │   └── Student Python files
│   │
│   └── ipynb/
│       └── Student Jupyter Notebook files
│
├── app.py
├── coach.py
├── graph.py
├── state.py
├── conversation.py
├── rag.py
├── ingest.py
├── database.py
├── config.py
├── evaluator.py
├── rubric_generator.py
│
├── create_tables.sql
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
├── README.md
└── .gitignore
```
---

# 32. Technology Stack

| Technology         | Purpose                         |
| ------------------ | ------------------------------- |
| Python             | Main programming language       |
| Streamlit          | Interactive user interface      |
| Gemini             | LLM generation and verification |
| Specialized Agents | Task-specific AI processing     |
| Graph Workflow     | Agent orchestration             |
| Shared State       | Agent communication             |
| RAG                | Context retrieval               |
| PostgreSQL         | Persistent database             |
| pgvector           | Vector similarity search        |
| BGE                | Text embeddings                 |
| LangChain          | Document processing             |
| Git/GitHub         | Version control                 |
| Docker             | Containerization                |
| Docker Compose     | Multi-service orchestration     |


---

# 33. Installation

## What?

The project requires Python, PostgreSQL, pgvector, and the required Python packages.

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

# 34. Configuration

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

# 35. Running the Application

Activate the virtual environment:

```bash
.myenv\Scripts\activate
```

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

Docker Execution

Build and start the application:

```bash
docker compose up --build
```

This starts the configured application and database services.

---

# 36. Overall System Architecture

The complete DSA Coach Agent architecture is:

                         ┌─────────────────────┐
                         │       Student       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Streamlit UI     │
                         │       app.py        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      state.py       │
                         │    Shared State     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      graph.py       │
                         │ Agent Orchestration │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     router.py       │
                         │   Intent Routing    │
                         └──────────┬──────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼                         ▼                         ▼
   Learning Agent            Practice Agent             Hint Agent
          │                         │                         │
          └─────────────────────────┼─────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
             Solution Agent                 Code Review Agent
                                                    │
                                                    ▼
                                              Student Code
                                                    │
                                           ┌────────┴────────┐
                                           │                 │
                                          .py              .ipynb
                                           │                 │
                                           └────────┬────────┘
                                                    │
                                                    ▼
                                                   RAG
                                                    │
                    ┌───────────────────────────────┼──────────────────────┐
                    │                               │                      │
                    ▼                               ▼                      ▼
                  Notes                          Stories             Descriptions
                    │                               │                      │
                    └───────────────────────────────┼──────────────────────┘
                                                    │
                                                    ▼
                                             leetcode.json
                                                    │
                                                    ▼
                                             BGE Embeddings
                                                    │
                                                    ▼
                                          PostgreSQL + pgvector
                                                    │
                                                    ▼
                                                  Gemini
                                                    │
                                                    ▼
                                             Draft Response
                                                    │
                                                    ▼
                                              Critic Agent
                                                    │
                                           ┌────────┴────────┐
                                           │                 │
                                         PASS              RETRY
                                           │                 │
                                           ▼                 ▼
                                      Final Answer      Regenerate
                                                             │
                                                             └──► Critic

                                                    │
                                                    ▼
                                             Rubric Generator
                                                    │
                                                    ▼
                                                Evaluator
                                                    │
                                                    ▼
                                             Student Feedback
                                                    │
                                                    ▼
                                           conversation.py
                                                    │
                                                    ▼
                                               PostgreSQL
# 37. Future Improvements

The current architecture can be extended with:

* More specialized agents
* More advanced graph workflows
* Adaptive learning paths
* Personalized difficulty
* Student performance tracking
* Automated test execution
* More programming languages
* Instructor dashboard
* Authentication
* Advanced rubric scoring
* Automated agent evaluation
* Better notebook processing
* Cloud deployment
* CI/CD pipelines
* Docker-based production deployment
* More sophisticated reasoning strategies

---

# 38. Conclusion

DSA Coach Agent is designed as an **agent-based AI learning and assessment platform** rather than a basic LLM chatbot.

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
It combines these agents with:

```text
RAG
+
PostgreSQL
+
pgvector
+
Conversation Persistence
+
Rubric Evaluation
+
Streamlit
+
Docker
```
The complete learning workflow can therefore be represented as:

```text
                     Student
                        │
                        ▼
                       UI
                        │
                        ▼
                      State
                        │
                        ▼
                      Graph
                        │
                        ▼
                     Router
                        │
                        ▼
               Specialized Agent
                        │
                        ▼
                      RAG
                        │
                        ▼
                     Gemini
                        │
                        ▼
                Draft Response
                        │
                        ▼
                    Critic
                        │
                 ┌──────┴──────┐
                 │             │
               PASS          RETRY
                 │             │
                 ▼             ▼
              Final        Regenerate
                               │
                               └──► Critic
                        │
                        ▼
                Rubric / Evaluator
                        │
                        ▼
                Student Feedback
                        │
                        ▼
                 Conversation DB
```

The most important aspect of the architecture is that **different agents have different responsibilities and different RAG configurations**.

The system demonstrates:

* Specialized multi-agent implementation
* Intent-based routing
* Shared agent state
* Graph-based orchestration
* RAG-based contextual generation
* Student code analysis
* Guided learning
* Practice generation
* Solution generation
* Critic-based verification
* Reasoning and retry loops
* Rubric-based evaluation
* Conversation persistence
* PostgreSQL and pgvector
* Student .py and .ipynb uploads
* Streamlit UI
* Docker containerization

DSA Coach Agent functions as a complete **AI-powered DSA learning, practice, code-review, reasoning, and assessment platform.**
