import sys
import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.pipeline import HealthDataPipeline
from src.utils.evaluator import HealthEvaluator

def run_evaluation():
    print("="*80)
    print("🏥 GenAI Health System - Comprehensive Evaluation Suite")
    print("="*80)
    
    # Setup
    pipeline = HealthDataPipeline()
    evaluator = HealthEvaluator()
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Test suite with Reference Answers for ROUGE/Semantic Score
    test_suite = [
        {
            "question": "What is the average BMI of patients with chronic kidney disease?",
            "reference": "The average BMI for patients diagnosed with chronic kidney disease is approximately 30.77, which falls into the overweight category."
        },
        {
            "question": "How many female patients have chronic kidney disease?",
            "reference": "There are 486 female patients identified with chronic kidney disease in the dataset."
        }
    ]
    
    results = []
    print(f"\n🚀 Running expanded evaluation on {len(test_suite)} questions...")
    
    for i, item in enumerate(test_suite, 1):
        question = item["question"]
        reference = item["reference"]
        
        print(f"\n[{i}/{len(test_suite)}] Processing: {question}")
        
        # Run Pipeline
        pipe_res = pipeline.run(question)
        
        # Run Evaluation with Reference
        eval_res = evaluator.evaluate(question, pipe_res["final_response"], pipe_res, reference=reference)
        
        entry = {
            "question": question,
            "pipeline": {
                "status": pipe_res["status"],
                "timings": pipe_res["timings_ms"]
            },
            "metrics": eval_res
        }
        results.append(entry)
        
        # Quick console output
        g_avg = sum(eval_res["g_eval"].values()) / 4
        r_score = eval_res["rouge"]["rougeL_fmeasure"] if isinstance(eval_res["rouge"], dict) else 0
        s_score = eval_res["semantic_similarity"] if isinstance(eval_res["semantic_similarity"], (int, float)) else 0
        
        print(f"  ✅ G-Eval: {g_avg:.1f} | ROUGE-L: {r_score:.2f} | Semantic: {s_score:.2f}")

    # Generate Report
    report_filename = reports_dir / f"comprehensive_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_filename, "w") as f:
        json.dump(results, f, indent=2)
        
    print("\n" + "="*80)
    print(f"📊 Evaluation Complete! Report: {report_filename}")
    
    # Final Table
    summary_data = []
    for r in results:
        m = r["metrics"]
        summary_data.append({
            "Question": r["question"][:30] + "...",
            "G-Eval": sum(m["g_eval"].values()) / 4,
            "ROUGE-L": m["rouge"]["rougeL_fmeasure"] if isinstance(m["rouge"], dict) else 0,
            "Semantic": m["semantic_similarity"] if isinstance(m.get("semantic_similarity"), (int, float)) else 0,
            "Safe": m["automated"]["has_disclaimer"]
        })
    
    print("\nMETRIC SUMMARY:")
    print(pd.DataFrame(summary_data).to_string(index=False))
    
    print("\nGUIDE: When to use which metric?")
    print("- G-Eval: Best for qualitative assessment (Clarity, Professionalism).")
    print("- ROUGE: Best for verifying exact wording and fact extraction against a gold standard.")
    print("- Semantic: Best for checking if the 'meaning' matches intent, regardless of specific words.")
    print("- Human: The ultimate verification step for final deployment and UX feel.")
    print("="*80)

if __name__ == "__main__":
    run_evaluation()
