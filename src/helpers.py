
from flask import current_app
import locale
from pandas import Series
import pandas as pd

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def normalize(s: Series) -> Series:
    return s.map(
        lambda v: (v - s.min())/(s.max()-s.min())
    )


def get_muni_data(state: str, city: str):
    local_data = current_app.config['BUDGET_DATA'].get('_'.join([state, city]), None)
    location = local_data['name']
    police_budget = locale.currency(float(local_data['policeBudget']), grouping=True)
    total_budget = locale.currency(float(local_data['totalBudget']), grouping=True)
    pct = int(float(local_data['policeBudget'])/float(local_data['totalBudget'])*100)
    return location, police_budget, total_budget, pct


def generate_plot_points(budget_data):
    budget_data_df = pd.DataFrame(budget_data).T
    budget_data_df['gf_norm'] = normalize(budget_data_df['totalBudget'].map(float))
    budget_data_df['p_norm'] = normalize(budget_data_df['policeBudget'].map(float))
    budget_data_df[['state', 'city']] = budget_data_df.index.str.split("_", expand=True).to_list()
    plot_points = budget_data_df[['gf_norm', 'p_norm', 'state', 'city']].to_dict('records')
    return plot_points



