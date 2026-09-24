# Automated KPI Validation with DeepEval

Checks that numbers an LLM pulls out of a business document are actually in the document, before they end up on a dashboard.

## The problem

Teams increasingly use LLMs to read reports and fill KPI tables: fleet size, budgets, cost per unit. The risk is quiet: a model can return a well-formed JSON with a number that isn't in the source. A normal schema check won't catch it, because the output looks valid.

## What this does

`Automated KPI Validation.py` is a pytest test that treats the extraction like any other data pipeline step and asserts on quality:

| check | metric | threshold | catches |
|---|---|---|---|
| Faithfulness | DeepEval `FaithfulnessMetric` | 0.7 | numbers or claims not supported by the source text (hallucinated KPIs) |
| KPI correctness | DeepEval `GEval` with a custom rubric | 0.8 | missing KPIs, or values that don't match the source |

The example is a fleet operations plan:

```
Source:  "The Q3 Fleet Operational Plan indicates a total fleet size of 150 vehicles.
          The projected quarterly maintenance budget is set at $45,000,
          averaging $300 per vehicle."

Model output:  {"fleet_size": 150, "maintenance_budget": "$45,000", "average_cost": "$300"}
```

The test is meant to pass only when every extracted value is grounded in the source. Change `model_output` to a wrong number (for example `"fleet_size": 175`) and the faithfulness check should fail it, which is how you want a pipeline gate to behave.

## Run it

```bash
pip install deepeval pytest
export OPENAI_API_KEY=...        # DeepEval uses an LLM as the judge (gpt-4o here)
deepeval test run "Automated KPI Validation.py"
# or: pytest "Automated KPI Validation.py"
```

## How it fits a real pipeline

1. LLM extracts KPIs from documents into JSON.
2. This test suite runs on each extraction (or a sample) in CI.
3. Only extractions that pass faithfulness and correctness are loaded into the reporting tables. Failures go to a review queue.

## Notes

- The judge model is configurable in the metric definitions.
- The same pattern works for any document type: swap in your own source text, expected KPIs and rubric.

Related: [DQ Rules Agent](https://github.com/Bhagyesh1207/dq-rules-agent) generates validation rules for tabular data from a profile.

Author: [Bhagyesh Patel](https://itsbhagyesh.vercel.app)
