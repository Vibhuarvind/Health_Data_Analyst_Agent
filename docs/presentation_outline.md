# Presentation Outline: GenAI Health Data Analyst

This document provides a structure for the final presentation of the project.

## 1. Introduction (1 min)
- **Goal**: Build a GenAI solution that queries complex health data without permanent integration.
- **Problem**: Health data is often siloed (demographics vs. activity logs). Consolidation is expensive and risky.
- **Solution**: A "Planner-Executor" system that joins data on-the-fly using LLM-generated logic.

## 2. Approach: Planner-Executor Pattern (3 mins)
- **Architecture**: NL Query -> Planner (Text-to-Code) -> Validator -> Executor -> Reasoner.
- **On-the-fly Joins**: Why we use temporary in-memory joins (Privacy & Performance).
- **Dual Query Capability**: Support for both Python (Pandas) and SQL queries.

## 3. Technical Highlights (3 mins)
- **Model**: Using Llama 3 (via Groq) for high speed and low latency.
- **Evaluation Framework**: 360-degree evaluation (G-Eval, ROUGE, Semantic Similarity).
- **UI**: Streamlit interface with auto-visualization capabilities.

## 4. Challenges & Solutions (2 mins)
- **Privacy**: Implemented a "Validator" to prevent code injection and system access.
- **Accuracy**: Used G-Eval to iteratively refine system prompts.
- **Safety**: Built-in disclaimers and instruction-tuned prompts to avoid medical diagnosis.

## 5. Ethical Considerations (1 min)
- **Data Privacy**: No data is sent to the LLM as unstructured text; only schemas and results.
- **Medical Safety**: Clear boundaries between "Data Insights" and "Clinical Advice".

## 6. Conclusion & Q&A
- Demo of the Streamlit application.
- Summary of delivery artifacts (Code, Evaluation Report, Data Audit).
