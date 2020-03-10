import pandas as pd

from dag_gettsim import tax_transfer
from dag_gettsim.benefits import benefits as child_benefits
from user_functions import (aggregated_benefits, piecewise_income_taxes,
                            unemployment_benefits)

if __name__ == "__main__":
    # ==================================================================================
    # Create data
    # ==================================================================================
    index = [
        "rich_person",
        "normal_person",
        "poor_person",
        "many_children",
        "unemployed",
    ]
    data = {
        "income": pd.Series([200_000, 50_000, 10_000, 60_000, 0], index=index),
        "wealth": pd.Series([1_000_000, 50_000, 0, 20_000, 0], index=index),
        "n_children": pd.Series([0, 2, 2, 5, 2], index=index),
    }

    # ==================================================================================
    # Baseline simulation
    # ==================================================================================
    baseline_result = tax_transfer(
        baseline_date="2019-01-01", data=data, targets=["disposable_income"],
    )

    df = pd.DataFrame(
        {
            "correct": pd.Series([260_000, 45_000, 12_000, 50_000, 4000], index=index),
            "calculated": baseline_result["disposable_income"],
        }
    )

    print("Baseline Results")
    print(df)

    # ==================================================================================
    # Replace income_tax by piecewise linear income tax (i.e. replace one function by
    # another one with the same interface)
    # ==================================================================================

    piecewise_result = tax_transfer(
        baseline_date="2019-01-01",
        data=data,
        functions={"income_taxes": piecewise_income_taxes},
        params={"tax_10_to_55": 0.2, "tax_above_55": 0.5},
        targets=["disposable_income"],
    )

    df = pd.DataFrame(
        {
            "correct": pd.Series([200_000, 45_000, 14_000, 32_000, 4000], index=index),
            "calculated": piecewise_result["disposable_income"],
        }
    )

    print("Piecewise Results")
    print(df)

    # ==================================================================================
    # Replace benefits by child_benefits and unemployment_benefits, i.e. replace one
    # function by two other functions but still re-use as much as possible of the
    # existing code)
    # ==================================================================================

    user_funcs = {
        "child_benefits": child_benefits,
        "unemployment_benefits": unemployment_benefits,
        "benefits": aggregated_benefits,
    }

    benefit_result = tax_transfer(
        baseline_date="2019-01-01",
        data=data,
        functions=user_funcs,
        params={"unemp_benefit": 8_000},
        targets=["disposable_income"],
    )

    df = pd.DataFrame(
        {
            "correct": pd.Series(
                [260_000, 45_000, 12_000, 50_000, 12_000], index=index
            ),
            "calculated": benefit_result["disposable_income"],
        }
    )

    print("Benefit Results")
    print(df)
