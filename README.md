# 🧠 Altir AI Codegen Agent

---

Agent Workflow

<img width="1594" height="692" alt="Screenshot 2025-07-31 at 11 02 00 PM" src="https://github.com/user-attachments/assets/d3e71dcf-c0f7-409a-8543-ae7f8d414b9f" />

Tools available to agent:

<img width="1935" height="683" alt="Screenshot 2025-07-24 at 8 22 48 PM" src="https://github.com/user-attachments/assets/3e6fc9d2-2eff-4afb-8063-58ebeee0fa83" />



This project is being used as a sandbox to:

- Learn which AI workflows are most useful internally
- Understand LangGraph-based orchestration
- Explore internal vs external AI tooling needs
- Learn how to create agent which plans, replans and executes.
- How can we manage and maintain short term and long term memory
- How to utilize RAG

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/altir/altir-ai-codegen.git
cd altir-ai-codegen
```

### 2. Install dependencies

```bash
pip install -r requirements.txt

Or (if using uv)

uv sync
```

### 3. Set up environment variables in .env file at root of the project

```bash
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_PROJECT=altir-ai-codegen
GROQ_API_KEY=your_groq_api_key
```

### 4. Run the tool

```bash
python main.py
```

### 5. Flowchart

Understand the flowchart of the tool in the `flowchart.png` file.
