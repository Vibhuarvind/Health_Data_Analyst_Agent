import time
import traceback
from src.core.planner import QueryPlanner
from src.core.executor import QueryExecutor
from src.core.reasoning import ReasoningEngine

class HealthDataPipeline:
    """
    Orchestrates the end-to-end flow:
    NL Query -> Plan -> Execute -> Reason -> Response
    """
    
    def __init__(self):
        self.planner = QueryPlanner()
        self.executor = QueryExecutor()
        self.reasoning = ReasoningEngine()
        
    def run(self, user_query: str, verbose: bool = False) -> dict:
        """
        Runs the full pipeline for a single query.
        """
        result = {
            "question": user_query,
            "status": "pending",
            "timings_ms": {},
            "py_code": None,
            "py_success": False,
            "result": None,
            "final_response": None,
            "error": None
        }
        
        t_total_start = time.perf_counter()
        
        try:
            # 1. Planning
            t_start = time.perf_counter()
            plan = self.planner.generate_plan(user_query)
            result["timings_ms"]["planning"] = (time.perf_counter() - t_start) * 1000
            result["py_code"] = plan.get("query_code")
            
            if plan.get("error"):
                raise ValueError(f"Planning failed: {plan['error']}")
                
            # 2. Execution
            t_start = time.perf_counter()
            py_exec = self.executor.execute(result["py_code"])
            result["timings_ms"]["execution"] = (time.perf_counter() - t_start) * 1000
            result["py_success"] = py_exec.get("success", False)
            result["result"] = py_exec.get("result")
            
            if not result["py_success"]:
                raise ValueError(f"Execution failed: {py_exec.get('error')}")
                
            # 3. Reasoning
            t_start = time.perf_counter()
            reasoning_out = self.reasoning.analyze_result(user_query, py_exec, result["py_code"])
            result["timings_ms"]["reasoning"] = (time.perf_counter() - t_start) * 1000
            result["final_response"] = reasoning_out.get("response")
            
            result["status"] = "success"
            
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            if verbose:
                print(f"Pipeline error: {e}")
                traceback.print_exc()
                
        result["timings_ms"]["total"] = (time.perf_counter() - t_total_start) * 1000
        return result

if __name__ == "__main__":
    # Quick test
    pipeline = HealthDataPipeline()
    res = pipeline.run("What is the average BMI of patients with chronic kidney disease?")
    print(res["final_response"])
