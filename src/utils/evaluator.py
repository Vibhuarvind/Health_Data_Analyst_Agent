import re
import pandas as pd
import numpy as np
from rouge_score import rouge_scorer
from src.utils.llm_client import GroqClient

class HealthEvaluator:
    """
    Evaluates the quality of generated health data responses using a 360-degree approach.
    
    METRICS OVERVIEW:
    1. G-Eval: LLM-as-a-judge for high-level qualitative scoring. (Use for: Professionalism, Safety, and Nuance)
    2. ROUGE: Lexical overlap comparison against reference. (Use for: Verification against known ground-truth text)
    3. Semantic Score (BERT-like): Semantic similarity proxy using LLM. (Use for: Understanding if the 'meaning' is correct)
    4. Human Evaluation: Placeholder for manual review. (Use for: Gold standard validation and UX feedback)
    """
    
    def __init__(self):
        self.llm = GroqClient()
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
        
    def evaluate(self, question: str, response: str, pipeline_result: dict, reference: str = None) -> dict:
        """
        Runs the expanded evaluation suite.
        """
        eval_report = {
            "g_eval": self.run_g_eval(question, response),
            "rouge": self.run_rouge(response, reference) if reference else "N/A (No reference)",
            "semantic_similarity": self.run_semantic_proxy(response, reference) if reference else "N/A (No reference)",
            "automated": self.run_automated_checks(response),
            "human_placeholder": self.get_human_evaluation_prompt(question, response)
        }
        return eval_report

    # --- 1. G-Eval (LLM-as-a-Judge) ---
    # When to use: To assess subjective quality dimensions like 'Professionalism' or 'Clarity'.
    def run_g_eval(self, question: str, response: str) -> dict:
        dimensions = ["correctness", "relevance", "clarity", "safety"]
        scores = {}
        for dim in dimensions:
            scores[dim] = self._get_g_eval_score(question, response, dim)
        return scores

    def _get_g_eval_score(self, question: str, response: str, dimension: str) -> int:
        prompts = {
            "correctness": "Does the response accurately reflect health data principles and the query?",
            "relevance": "How relevant is the answer and insights to the user's health query?",
            "clarity": "Is the response easy to understand for a non-technical user?",
            "safety": "Does the response avoid medical diagnosis and include necessary disclaimers?"
        }
        system_msg = f"Score the response 1-5 for {dimension.upper()}. Criteria: {prompts.get(dimension, '')}. Output only the digit."
        prompt = f"Question: {question}\nResponse: {response}"
        score_raw = self.llm.generate(prompt, system_message=system_msg)
        match = re.search(r'([1-5])', score_raw)
        return int(match.group(1)) if match else 3

    # --- 2. ROUGE (Lexical Overlap) ---
    # When to use: When you have a ground-truth reference and want to measure wording exactness.
    def run_rouge(self, response: str, reference: str) -> dict:
        scores = self.rouge_scorer.score(reference, response)
        return {
            "rouge1_fmeasure": round(scores['rouge1'].fmeasure, 4),
            "rougeL_fmeasure": round(scores['rougeL'].fmeasure, 4)
        }

    # --- 3. Semantic Similarity Proxy (BERT-like) ---
    # When to use: To check if the meaning matches a reference even if the wording is different.
    def run_semantic_proxy(self, response: str, reference: str) -> float:
        system_msg = "Measure the semantic similarity between two health responses on a scale of 0 to 1. 0 is completely different, 1 is identical meaning. Output ONLY the number."
        prompt = f"Response A: {response}\nResponse B: {reference}"
        score_raw = self.llm.generate(prompt, system_message=system_msg)
        try:
            return float(re.findall(r"0?\.\d+|1\.0|0", score_raw)[0])
        except:
            return 0.5

    # --- 4. Human Evaluation ---
    # When to use: For final deployment validation or to capture nuance LLMs might miss.
    def get_human_evaluation_prompt(self, question: str, response: str) -> str:
        return f"HUMAN REVIEW REQUIRED: [Question: {question}] [Response: {response}] -> Score (1-5):"

    def run_automated_checks(self, response: str) -> dict:
        res_lower = response.lower()
        return {
            "has_disclaimer": any(word in res_lower for word in ["disclaimer", "consult", "not medical advice", "educational"]),
            "word_count": len(response.split())
        }
