# Design Decisions & Technical Documentation

This document explicitly maps the project's technical implementation to the case study requirements.

## 1. Data Processing (Mandatory 2a)
- **Data Integration**: Implemented **on-the-fly in-memory joins** using Pandas in `executor.py`. This avoids permanent data consolidation as per the core project objective.
- **Feature Engineering**: Implemented in `src/data/loader.py` (added `BMI_Category` derived from continuous health metrics).

## 2. Model Methodology (Mandatory 2b & 2c)
- **Interim Logic**: The system follows a **Planner-Executor** pattern where the LLM first generates Python/SQL code. This ensures the model only processes the required subset of data.
- **Instruction-Tuning**: Handled via **expert system prompts** in `planner.py`. This ensures the OSS model (Llama 3) adheres to analytical constraints without the need for resource-intensive parameter fine-tuning for this POC.

## 3. Evaluation & Refinement (Mandatory 2d)
- **Framework**: A 360-degree suite in `src/utils/evaluator.py`.
- **Metrics**: G-Eval (LLM-as-a-judge), ROUGE (lexical), and Semantic Similarity (Meaning).
- **Refinement**: The `ReasoningEngine` provides the "refinement" layer, ensuring the final answer is insightful and contextually grounded in the execution result.

## 4. Safety & Ethical Factors (Note)
- **Guardrails**: `QueryValidator` blocks system-level commands and dangerous Python imports.
- **Privacy**: No raw medical data is uploaded to public LLM services; only metadata and temporary query results are processed.
- **Non-Clinical boundaries**: Disclaimers are integrated into both the `ReasoningEngine` response and the Streamlit UI.

## 5. Technology Choice
- **Llama 3 (via Groq)**: Chosen for high-performance reasoning and near-instant response times.
- **Streamlit**: Chosen for its fast development of a clean, interactive medical analyst dashboard.
