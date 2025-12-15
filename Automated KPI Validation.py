import pytest
from deepeval import assert_test
# 1. FIXED: Import LLMTestCaseParams from 'deepeval.test_case'
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import FaithfulnessMetric, GEval

# ---------------------------------------------------------
# 1. DEFINE YOUR METRICS
# ---------------------------------------------------------

# Faithfulness: Did the model hallucinate numbers not in the text?
faithfulness_metric = FaithfulnessMetric(
    threshold=0.7,
    model="gpt-4o",  # or any judge model you prefer
    include_reasoning=True
)

# Custom G-Eval: strictly checks if JSON structure and specific KPIs exist
kpi_correctness_metric = GEval(
    name="KPI Extraction Correctness",
    criteria="Determine if the actual output contains 'Maintenance Cost' and 'Fleet Size' matching the context.",
    # 2. FIXED: This now works because LLMTestCaseParams is imported correctly
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.CONTEXT],
    threshold=0.8
)

# ---------------------------------------------------------
# 2. DEFINE THE TEST DATA
# ---------------------------------------------------------

fleet_plan_text = """
The Q3 Fleet Operational Plan indicates a total fleet size of 150 vehicles. 
The projected quarterly maintenance budget is set at $45,000, 
averaging $300 per vehicle.
"""

model_output = """
{
  "fleet_size": 150,
  "maintenance_budget": "$45,000",
  "average_cost": "$300"
}
"""

# ---------------------------------------------------------
# 3. RUN THE TEST CASE
# ---------------------------------------------------------

def test_kpi_extraction():
    test_case = LLMTestCase(
        input="Extract the fleet size and budget from the text.",
        actual_output=model_output,
        retrieval_context=[fleet_plan_text]
    )

    assert_test(test_case, [faithfulness_metric, kpi_correctness_metric])
    print("✅ KPI Extraction Test Passed!")