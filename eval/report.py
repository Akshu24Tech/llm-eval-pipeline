import json
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from eval import evaluate

def run(test_cases_path="samples/test_cases.json"):
    with open(test_cases_path) as f:
        samples = json.load(f)

    results = []
    for sample in samples:
        print(f"Evaluating sample {sample['id']}...")
        result = evaluate(sample)
        results.append(result)

    scored = [r for r in results if r["llm_score"] is not None]
    avg_score = sum(r["total"] for r in scored) / len(scored) if scored else 0
    pass_rate = sum(1 for r in results if r["passed"]) / len(results) * 100

    report = {
        "total_samples": len(results),
        "avg_score": round(avg_score, 2),
        "pass_rate": round(pass_rate, 1),
        "results": results
    }

    with open("eval_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n{'='*40}")
    print(f"Avg score : {avg_score:.2f}/6")
    print(f"Pass rate : {pass_rate:.1f}%")
    print(f"{'='*40}")

    # Fail the pipeline if quality drops
    if avg_score < 4.0:
        print(f"\n❌ FAILED — avg score {avg_score:.2f} below threshold 4.0")
        sys.exit(1)
    else:
        print(f"\n✅ PASSED")
        sys.exit(0)

if __name__ == "__main__":
    run()