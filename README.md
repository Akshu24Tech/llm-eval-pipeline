# llm-eval-pipeline

![CI](https://github.com/Akshu24Tech/llm-eval-pipeline/actions/workflows/eval.yml/badge.svg)

A lightweight, automated evaluation pipeline for LLM outputs — built from scratch through hands-on annotation and rubric design.

Runs on every push via GitHub Actions. No eval framework dependency. Just Python, a rubric, and a Groq-powered judge.

---

## What it does

Every time code is pushed to `main`, the pipeline:

1. Runs **programmatic checks** — length, format, refusal detection (instant, no API calls)
2. Runs an **LLM judge** powered by Groq (`llama-3.3-70b-versatile`) scoring each output across 3 dimensions
3. Generates a **JSON report** with per-sample scores and a pass/fail verdict
4. **Fails the pipeline** if average quality drops below threshold — blocking bad changes from merging

---

## Eval dimensions

Each output is scored 0–2 across three dimensions (max total: 6):

| Dimension | What it measures |
|---|---|
| **Hallucination** | Is every claim specific and verifiable? |
| **Off-task** | Does the output directly answer what was asked? |
| **Format** | Does the structure match what was requested? |

A total score below **4.0/6** fails the pipeline.

---

## Repo structure

```
llm-eval-pipeline/
├── eval/
│   ├── eval.py          # programmatic checks + LLM judge
│   ├── rubric.py        # dimension definitions + judge prompt
│   └── report.py        # runs all samples, generates report, exits with status
├── samples/
│   └── test_cases.json  # 20 annotated test cases with human scores
├── .github/
│   └── workflows/
│       └── eval.yml     # GitHub Actions CI/CD trigger
├── requirements.txt
└── README.md
```

---

## Quickstart

```bash
git clone https://github.com/Akshu24Tech/llm-eval-pipeline.git
cd llm-eval-pipeline
pip install -r requirements.txt

export GROQ_API_KEY=your_key_here
python eval/report.py
```

---

## How the pipeline was built

This wasn't downloaded or copied from a template. It was built bottom-up through a structured 2-week sprint:

- **50 outputs manually annotated** — reading real Perplexity AI responses and writing a verdict on every one
- **Rubric designed from scratch** — 3 dimensions with PASS, FAIL, and BORDERLINE examples each
- **LLM judge validated** — achieved ~80% agreement with human scores before shipping
- **BERTScore studied and broken** — tested negation traps, fluent nonsense, and restructured-but-correct outputs to understand metric failure modes
- **CI/CD wired last** — the automation came after the intuition, not before

The full annotation database and rubric are logged in Notion.

---

## Extending it

**Add a new dimension** — define it in `rubric.py` and add it to the judge prompt.

**Change the model** — swap `llama-3.3-70b-versatile` in `eval.py` for any Groq-supported model.

**Lower/raise the threshold** — change `PASS_THRESHOLD` in `rubric.py`.

**Add more test cases** — append to `samples/test_cases.json` following the existing schema.

---

## Stack

- **Judge model:** Groq — `llama-3.3-70b-versatile`
- **CI/CD:** GitHub Actions
- **Language:** Python 3.11

---

## Background

Built as a portfolio project to develop hands-on intuition for text data quality and LLM evaluation design. Covers manual annotation, rubric design, LLM-as-judge, programmatic checks, metric analysis (BERTScore), and CI/CD integration.
