import pandas as pd

dia_atual = pd.Timestamp.today().normalize()

def calculate_vals(df, ref, day, macro):
    """
    Calculates aggregated values of a specific metric for a given day,
    both for the total and filtered by a specific meal.

    Parameters:
    ----------
    df : pandas.DataFrame
        DataFrame containing diet data.
    ref : str
        Meal name ('Ref1, 'Ref2', 'Ref3', 'Ref4', 'Ref5').
    day : datetime/date
        Day to filter.
    macro : str
        Macro ('Calorias (kcal)', 'Proteínas (g)', 'Carboidratos (g)')

    Returns:
    -------
    tuple (vals_day, vals_ref_day)
        vals_day : float/int
            Total sum of the metric for the selected day.
        vals_ref_day : float/int
            Sum of the metric for the specified meal on the same day.
    """
    vals_day = df[df['Data'] == day][macro].sum()
    vals_ref_day = df[(df['Refeição'] == ref) & (df['Data'] == day)][macro].sum()

    return vals_day, vals_ref_day

