# 🧠 Altir AI Codegen Directed flow

This project is being used as a sandbox to:

- Learn which AI workflows are most useful internally
- Understand LangGraph-based orchestration
- Explore internal vs external AI tooling needs
- Learn how to create directed flow.

Head over to "agent" branch to learn how we can create agentic flow.

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
```

### 4. Run the tool

```bash
python main.py
```

### 5. Flowchart

Understand the flowchart of the tool in the `flowchart.png` file.
