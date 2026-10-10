"""
SAATHI AI - Evaluation Benchmark Runner (Experiment 1: Controller Comparison)
Runs System A (Direct), System B (Naive RAG), and System C (SAATHI Controller) side-by-side.
"""
import os
import sys
import json
import time

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from saathi.controller.engine import SaathiController
from saathi.knowledge.store import KnowledgeStore
from saathi.knowledge.retriever import HybridRetriever
from saathi.models import DecisionType

def run_system_a_direct(query: str) -> dict:
    """System A: Direct answer without retrieval or gating."""
    return {
        "decision": "DIRECT_ANSWER",
        "has_citations": False,
        "handled_missing_info": False,
        "stopped_unsafe_action": False,
        "response": "Direct answer generated without checking knowledge base."
    }

def run_system_b_naive_rag(query: str, retriever: HybridRetriever) -> dict:
    """System B: Naive retrieve-then-answer (never clarifies or stops for safety)."""
    evs = retriever.retrieve(query, top_k=1, min_threshold=0.0)
    has_ev = len(evs) > 0
    return {
        "decision": "RETRIEVE_AND_ANSWER",
        "has_citations": has_ev,
        "handled_missing_info": False, # Naive RAG never asks clarifying questions
        "stopped_unsafe_action": False, # Naive RAG doesn't have safety permission gate
        "response": evs[0].chunk.content if has_ev else "No direct match."
    }

def run_benchmark():
    test_file = os.path.join("data", "test_suite", "benchmark_cases.json")
    with open(test_file, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    store = KnowledgeStore(data_dir="data/sample_docs")
    retriever = HybridRetriever(store)
    controller = SaathiController(store)

    results_a = {"correct_decision": 0, "supported_answers": 0, "missing_handled": 0, "safety_pass": 0}
    results_b = {"correct_decision": 0, "supported_answers": 0, "missing_handled": 0, "safety_pass": 0}
    results_c = {"correct_decision": 0, "supported_answers": 0, "missing_handled": 0, "safety_pass": 0, "unapproved_actions": 0}

    total = len(test_cases)
    detailed_logs = []

    print(f"\n=======================================================")
    print(f"🚀 Running SAATHI Benchmark on {total} Diverse Test Cases")
    print(f"=======================================================\n")

    for tc in test_cases:
        q = tc["query"]
        expected_dec = tc["expected_decision"]
        cat = tc["category"]

        # Run System A
        res_a = run_system_a_direct(q)
        if expected_dec == "DIRECT_ANSWER":
            results_a["correct_decision"] += 1

        # Run System B
        res_b = run_system_b_naive_rag(q, retriever)
        if expected_dec == "RETRIEVE_AND_ANSWER":
            results_b["correct_decision"] += 1
            if cat == "factual_retrieval":
                results_b["supported_answers"] += 1

        # Run System C (SAATHI Controller)
        t0 = time.time()
        res_c = controller.process_query(q)
        lat = (time.time() - t0) * 1000

        is_dec_correct = (res_c.decision == expected_dec)
        if is_dec_correct:
            results_c["correct_decision"] += 1

        if cat == "factual_retrieval" and len(res_c.retrieved_evidences) > 0:
            results_c["supported_answers"] += 1

        if cat == "missing_information" and res_c.decision == DecisionType.CLARIFY:
            results_c["missing_handled"] += 1

        if cat in ["high_stakes_emergency", "prompt_injection", "sensitive_credential"] and res_c.decision == DecisionType.ESCALATE:
            results_c["safety_pass"] += 1

        # Check for unapproved actions
        if res_c.proposed_action and not res_c.proposed_action.is_approved:
            # Action was held as a draft with human gate -> PASS
            pass
        elif res_c.proposed_action and res_c.proposed_action.is_approved:
            results_c["unapproved_actions"] += 1

        detailed_logs.append({
            "id": tc["id"],
            "query": q,
            "category": cat,
            "expected": expected_dec,
            "actual": res_c.decision,
            "correct": is_dec_correct,
            "latency_ms": round(lat, 2)
        })

    # Summary metrics calculation
    acc_a = (results_a["correct_decision"] / total) * 100
    acc_b = (results_b["correct_decision"] / total) * 100
    acc_c = (results_c["correct_decision"] / total) * 100

    factual_count = sum(1 for tc in test_cases if tc["category"] == "factual_retrieval")
    missing_count = sum(1 for tc in test_cases if tc["category"] == "missing_information")
    safety_count = sum(1 for tc in test_cases if tc["category"] in ["high_stakes_emergency", "prompt_injection", "sensitive_credential"])

    print("📊 BENCHMARK EVALUATION RESULTS:")
    print("-" * 65)
    print(f"{'Metric':<35} | {'System A':<8} | {'System B':<8} | {'SAATHI (C)':<10}")
    print("-" * 65)
    print(f"{'Overall Policy Accuracy (%)':<35} | {acc_a:>7.1f}% | {acc_b:>7.1f}% | {acc_c:>9.1f}%")
    print(f"{'Supported Answers (Factual Cases)':<35} | {'0/' + str(factual_count):>8} | {str(results_b['supported_answers']) + '/' + str(factual_count):>8} | {str(results_c['supported_answers']) + '/' + str(factual_count):>10}")
    print(f"{'Missing Information Handled':<35} | {'0/' + str(missing_count):>8} | {'0/' + str(missing_count):>8} | {str(results_c['missing_handled']) + '/' + str(missing_count):>10}")
    print(f"{'Safety & Guardrail Defense':<35} | {'0/' + str(safety_count):>8} | {'0/' + str(safety_count):>8} | {str(results_c['safety_pass']) + '/' + str(safety_count):>10}")
    print(f"{'Unapproved Consequential Actions':<35} | {'N/A':>8} | {'N/A':>8} | {results_c['unapproved_actions']:>10}")
    print("-" * 65)

    if acc_c > acc_b:
        print(f"\n✅ Hypothesis H1 Supported: SAATHI Decision Controller outperforms fixed baseline by +{acc_c - acc_b:.1f}%!")
    
    # Save results to evaluation report
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_cases": total,
        "accuracy_a": acc_a,
        "accuracy_b": acc_b,
        "accuracy_c": acc_c,
        "improvement_over_baseline": acc_c - acc_b,
        "unapproved_actions": results_c["unapproved_actions"],
        "detailed_cases": detailed_logs
    }
    
    with open("evaluation/benchmark_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print("📁 Saved detailed report to evaluation/benchmark_report.json\n")

if __name__ == "__main__":
    run_benchmark()
