---
title: Nexus Health Analyst
emoji: 🏥
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
short_description: GenAI Health Data Analysis with LLM + Pandas
app_port: 8501
---

# 🏥 Nexus Health Analyst

**GenAI-Powered Health Data Analysis System**

A production-grade Natural Language to Data Insights pipeline using:
- 🧠 **LLM**: Llama 3.3 (70B) via Groq API for code generation & reasoning
- 🐼 **Pandas**: Dynamic data analysis & manipulation
- 🔒 **Security**: AST-based code validation & sandboxed execution
- 📊 **Datasets**: Patient records, vitals monitoring, lab results

## 🚀 Features

- **Natural Language Queries**: "Show me average blood pressure by age group"
- **Cross-Dataset Analysis**: Automatic joins between patient records, vitals, and labs
- **Smart Reasoning**: LLM-generated insights from query results
- **Production-Ready**: Type hints, comprehensive tests, FastAPI backend

## 🎯 Architecture

**Planner → Executor → Reasoner** pipeline:
1. **Planner**: Converts NL query → Pandas code (schema-aware prompting)
2. **Executor**: Safely runs code in sandboxed environment
3. **Reasoner**: Generates natural language insights from results

## 💡 Example Queries

```
"What is the average blood pressure by age group?"
"Show me patients with abnormal glucose levels"
"Compare heart rate trends across different patient groups"
"List patients who need attention based on vital signs"
```

## 🔧 Tech Stack

- **LLM**: Llama 3.3 70B (Groq)
- **Data**: Pandas, NumPy
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Security**: AST validation, sandboxed execution
- **Testing**: Pytest (20+ tests)
- **CI/CD**: GitHub Actions

## 📝 License

MIT License - See LICENSE file for details
