import pandas as pd


def piecewise_income_taxes(income, params):
    """Piecewise linear income taxes.

    This is a stupid tax schedule where earning more can be strongly punished.

    As such it has two types of parameters: cutoffs and tax rates. We decide to
    hardcode the cutoffs and to specify the tax rates as user provided params to show
    that both are viable options.

    Args:
        income (pd.Series)
        params (pd.Series)

    Returns
        pd.Series: Piecewise linear income tax.

    """
    taxes = pd.Series(data=0, index=income.index)
    taxes = taxes.where(income <= 10_000, income * params.tax_10_to_55)
    taxes = taxes.where(income <= 20_000, income * params.tax_above_55)
    return taxes


def unemployment_benefits(income, params):
    benefits = pd.Series(data=0, index=income.index)
    benefits = benefits.where(income != 0, params.unemp_benefit)
    return benefits


def aggregated_benefits(child_benefits, unemployment_benefits, params):
    return child_benefits + unemployment_benefits


def unrelated_function(income, params):
    return 0


def unrelated_function_2(unrelated_function, params):
    return 1


def un_unrelated_function(params):
    return 0
