import json
import re
import os
from groq import Groq
from rubric import JUDGE_PROMPT, PASS_THRESHOLD

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def programmatic_checks(prompt, output):
    results = {}
    word_count = len(output.split())
    results["length_ok"] = 20 <= word_count <= 300
    refusal_phrases = ["as an ai", "i cannot", "i'm not able", "i don't have access"]
    results["no_refusal"] = not any(p in output.lower() for p in refusal_phrases)
    filler_openers = ["certainly!", "great question", "of course!", "absolutely!"]
    results["no_filler"] = not any(output.lower().startswith(p) for p in filler_openers)
    asks_bullets = any(w in prompt.lower() for w in ["bullet", "list", "points"])
    has_bullets = "•" in output or "- " in output or "* " in output
    results["format_match"] = (not asks_bullets) or has_bullets
    results["has_substance"] = word_count >= 10
    results["all_passed"] = all(results.values())
    return results

def judge(prompt, output):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # best free model on Groq
        messages=[{
            "role": "user",
            "content": JUDGE_PROMPT.format(prompt=prompt, output=output)
        }],
        max_tokens=300,
        temperature=0
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)

def evaluate(sample):
    prompt = sample["prompt"]
    output = sample["output"]
    checks = programmatic_checks(prompt, output)

    if not checks["all_passed"]:
        return {
            "id": sample["id"],
            "rule_checks": checks,
            "llm_score": None,
            "total": 0,
            "passed": False
        }

    scores = judge(prompt, output)
    passed = scores["total"] >= PASS_THRESHOLD

    return {
        "id": sample["id"],
        "rule_checks": checks,
        "llm_score": scores,
        "total": scores["total"],
        "passed": passed
    }