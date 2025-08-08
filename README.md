# 🧠 Altir AI Codegen

> An intelligent coding assistant tailored for Altir's codebase, tech stack, and internal workflows.

---

This project is being used as a sandbox to:

- Learn which AI workflows are most useful internally
- Understand LangGraph-based orchestration
- Explore internal vs external AI tooling needs
- How to create agent which plans, replans and executes.
- This is still in progress

Future scope: 

## 🚀 Overview

**Altir AI Codegen** is a developer productivity tool built to accelerate day-to-day engineering at Altir.  
Unlike generic coding tools like Cursor or Copilot, this assistant is designed to integrate deeply with **Altir’s internal architecture**, **coding conventions**, and **business logic**.

It understands how _we_ build software — from folder structure to API design — and helps automate repetitive, high-context tasks in a context-aware way.

---

### ⚠️ Important Notes

- This tool is **in progress** and still in **exploration phase**.
- It is **not a replacement** for existing tools like **Cursor** or **Windsurf** used at Altir.
- Currently, it **only works with OpenAI models** (GPT-3.5 / GPT-4).
- It's intended to explore the possibility of lightweight, internally-shaped automation assistants tailored to our workflows.

---

## 💡 How It's Different from Cursor

While tools like Cursor are extremely powerful and production-ready, `altir-ai-codegen` explores areas where a **company-specific assistant** could provide deeper value.

| Feature                    | Cursor / Copilot       | `altir-ai-codegen`           |
| -------------------------- | ---------------------- | ---------------------------- |
| Access to internal code    | ❌ No                  | ✅ Fully aware of our repos  |
| Follows our conventions    | ❌ Generic suggestions | ✅ Altir-specific patterns   |
| Internal API knowledge     | ❌                     | ✅ Understands our backend   |
| Private/Self-hosted option | ❌                     | ✅ Enterprise-friendly       |
| Integrated workflows       | ❌                     | ✅ Tied to our dev processes |

This tool is focused on exploring **Altir-specific automation**, and may eventually be integrated with existing systems or work alongside tools like Cursor — not replace them.

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
```

### 4. Run the tool

```bash
python main.py
```

### 5. Flowchart

Understand the flowchart of the tool in the `flowchart.png` file.
