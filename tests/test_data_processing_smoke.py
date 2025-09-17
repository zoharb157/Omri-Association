from data_processing import calculate_monthly_budget
from tests.fixtures.sample_data import sample_donations_df, sample_expenses_df


def test_calculate_monthly_budget_handles_basic_data():
    expenses = sample_expenses_df()
    donations = sample_donations_df()

    result = calculate_monthly_budget(expenses, donations)

    assert result["total_donations"] > 0
    assert result["total_expenses"] > 0
    assert result["balance"] == result["total_donations"] - result["total_expenses"]
    assert "monthly_donations" in result
    assert "monthly_expenses" in result
