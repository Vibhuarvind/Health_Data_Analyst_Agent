import streamlit as st
import pandas as pd
import time
import plotly.express as px
from src.core.planner import QueryPlanner
from src.core.executor import QueryExecutor
from src.core.reasoning import ReasoningEngine

# Page Config
st.set_page_config(
    page_title="GenAI Health Analyst",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished UI
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .stTextInput > div > div > input {
        caret-color: #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---
with st.sidebar:
    st.title("🏥 Health Analyst")
    st.markdown("---")
    st.markdown("### 🛠️ Capabilities")
    st.markdown("- **Natural Language Queries**")
    st.markdown("- **On-the-Fly Joining**")
    st.markdown("- **Auto-Visualization**")
    
    st.markdown("---")
    st.markdown("### 📝 Example Queries")
    
    examples = [
        "Select an example...",
        "What is the average BMI of patients with chronic kidney disease?",
        "Show me the relationship between smoking and blood pressure.",
        "Which patients have high stress and low physical activity?",
        "Find female patients under 40 with abnormal BP."
    ]
    
    selected_example = st.selectbox("Quick Start:", examples)
    
    st.markdown("---")
    st.caption("v1.0.0 | Powered by Llama 3 via Groq")

# --- Main Content ---
st.markdown('<div class="main-header">GenAI Health Data Analyst</div>', unsafe_allow_html=True)

# Ethical Disclaimer
st.info("⚠️ **Disclaimer:** This tool uses hypothetical data for educational purposes. Generated insights are not medical advice.", icon="ℹ️")

# Chat Interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Query Input logic
prompt = st.chat_input("Ask a question about the health data...")

# Handle Sidebar Selection (Simulates input)
if selected_example != "Select an example...":
    prompt = selected_example
    # Reset selection to avoid loop
    # st.sidebar.selectbox index reset is hard in streamlit without rerun, handle gracefully

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process Query
    with st.chat_message("assistant"):
        with st.spinner("Analyzing data..."):
            start_time = time.time()
            
            # Initialize components (cached)
            @st.cache_resource
            def get_components():
                return QueryPlanner(), QueryExecutor(), ReasoningEngine()
            
            planner, executor, reasoning = get_components()
            
            # 1. Plan
            plan_result = planner.generate_plan(prompt)
            
            if plan_result['error']:
                st.error(f"❌ Planning Error: {plan_result['error']}")
                st.stop()
                
            code = plan_result['query_code']
            
            # 2. Execute
            exec_result = executor.execute(code)
            
            if not exec_result['success']:
                st.error(f"❌ Execution Error: {exec_result['error']}")
                with st.expander("See Traceback"):
                    st.code(exec_result['traceback'])
                st.stop()
                
            result_data = exec_result['result']
            
            # 3. Reason
            insight = reasoning.analyze_result(prompt, exec_result, code)
            
            # 4. Evaluate (Real-time G-Eval)
            from src.utils.evaluator import HealthEvaluator
            evaluator = HealthEvaluator()
            eval_results = evaluator.evaluate(prompt, insight['response'], exec_result)
            
            total_time = time.time() - start_time
            result_response = insight['response']
            
            # --- Display Results ---
            
            # Tabs for organized view
            tab1, tab2, tab3, tab4 = st.tabs(["💡 Insight", "📊 Data & Viz", "🛠️ Logic", "⏱️ Evaluation"])
            
            with tab1:
                st.markdown(result_response)
                
            with tab2:
                # Result Display
                if isinstance(result_data, (pd.DataFrame, pd.Series)):
                    st.dataframe(result_data)
                    
                    # Auto-Visualization Logic
                    st.markdown("### 📈 Auto-Visualization")
                    try:
                        if isinstance(result_data, pd.DataFrame):
                            # Ensure numeric columns
                            num_cols = result_data.select_dtypes(include=['number']).columns.tolist()
                            
                            if len(num_cols) >= 2:
                                fig = px.scatter(result_data, x=num_cols[0], y=num_cols[1], 
                                               title=f"{num_cols[0]} vs {num_cols[1]}")
                                st.plotly_chart(fig, use_container_width=True)
                                
                            elif len(num_cols) == 1 and len(result_data.columns) == 2:
                                cat_col = [c for c in result_data.columns if c not in num_cols][0]
                                fig = px.bar(result_data, x=cat_col, y=num_cols[0], 
                                           title=f"{num_cols[0]} by {cat_col}")
                                st.plotly_chart(fig, use_container_width=True)
                                
                            elif len(num_cols) == 1:
                                fig = px.histogram(result_data, x=num_cols[0], 
                                                 title=f"Distribution of {num_cols[0]}")
                                st.plotly_chart(fig, use_container_width=True)
                        elif isinstance(result_data, pd.Series):
                             st.bar_chart(result_data)
                    except Exception as e:
                        st.caption("Visualization not applicable.")

                else:
                    st.write(result_data)

            with tab3:
                st.markdown("### Generated Code")
                st.code(code, language="python")
                
                st.markdown("### Execution Plan")
                st.json({
                    "plan_explanation": plan_result['explanation'],
                    "datasets_loaded": ["Health Metrics (df1)", "Activity (df2)"],
                    "join_strategy": "On-the-fly (in-memory)"
                })

            with tab4:
                st.markdown("### 📊 LLM Evaluation (G-Eval)")
                st.caption("AI-as-a-judge assessment of the generated response.")
                
                g_eval = eval_results.get("g_eval", {})
                cols = st.columns(4)
                
                # Metric display helper
                def get_score_color(score):
                    if score >= 4: return "normal"
                    if score >= 3: return "off"
                    return "inverse"

                dimensions = ["Correctness", "Relevance", "Clarity", "Safety"]
                for i, dim in enumerate(dimensions):
                    score = g_eval.get(dim.lower(), 0)
                    cols[i].metric(dim, f"{score}/5")

                st.markdown("---")
                col_m1, col_m2 = st.columns(2)
                
                with col_m1:
                    st.markdown("#### ⏱️ Performance Metrics")
                    st.metric("Processing Time", f"{total_time:.2f}s")
                    if isinstance(result_data, pd.DataFrame):
                        st.metric("Rows Processed", len(result_data))
                
                with col_m2:
                    st.markdown("#### 🛡️ Automated Checks")
                    safe_status = "✅ Present" if eval_results["automated"]["has_disclaimer"] else "❌ Missing"
                    st.markdown(f"**Medical Disclaimer:** {safe_status}")
                    st.markdown(f"**Word Count:** {eval_results['automated']['word_count']}")
            
            # Save assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": result_response})
