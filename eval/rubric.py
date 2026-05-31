DIMENSIONS = ["hallucination", "off_task", "format"]

JUDGE_PROMPT = """
You are a strict text quality evaluator.
Score the following AI output across 3 dimensions.
Return ONLY valid JSON, no extra text.

HALLUCINATION (0-2)
0 = false or unverifiable claim stated as fact
1 = vague but not clearly wrong
2 = specific and verifiable

OFF_TASK (0-2)
0 = ignores the question entirely
1 = partially answers but drifts
2 = directly and fully answers

FORMAT (0-2)
0 = ignores requested format or structure
1 = partially follows format
2 = fully follows requested structure

User prompt: {prompt}
AI output: {output}

Return ONLY this JSON:
{{
  "hallucination": 0,
  "off_task": 0,
  "format": 0,
  "total": 0,
  "reason": "biggest issue in one sentence"
}}
"""

PASS_THRESHOLD = 4.0