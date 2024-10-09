import pandas as pd
import json

budget_path = "budget_data.csv"
year = 2024

df = pd.read_csv(budget_path)
df['id'] = df.apply(
    lambda r: "_".join(
        [r['state'].lower(), r['city'].lower()]
    ).replace(" ", ""), 1
)
df['name'] = df.apply(
    lambda r: ", ".join(
        [r['city'].title(), r['state']]
    ), 1
)
df['budget_type'] = df.apply(
    lambda r: r['expense'].lower()[0] + str(r['year'])[-2:], 1
)

budget_df = df.query("year==@year & expense!='Education'")[['id', 'name', 'expense', 'year', 'budget']].set_index(['id', 'name']).pivot(
    columns='expense', values=['budget']
)
budget_df.columns = ['general_fund', 'police']
budget_df.reset_index(inplace=True)

budget_df['police'] = budget_df['police'].fillna('1')
budget_df['general_fund'] = budget_df['general_fund'].fillna('5')

coords = pd.read_csv('coordinate_df.csv').query("use=='x'")
coords['id'] = coords.apply(
    lambda r: "_".join(
        [r['state'].lower(), r['city'].lower()]
    ).replace(" ", ""), 1
)

big_df = pd.merge(coords, budget_df, on='id')
for c in ['police', 'general_fund']:
    big_df[c] = big_df[c].map(lambda p: p.replace("$", "").replace(",", ""))

city_locations_df = big_df.rename(
            columns={'x':'cx', 'y':'cy'}
        )[['id', 'name', 'cx', 'cy']].dropna()

budget_data_df = big_df.rename(
            columns={'police':'policeBudget', 'general_fund':'totalBudget'}
        ).set_index('id')[['name', 'policeBudget', 'totalBudget']]

with open("src/city_locations.json", "w+") as f:
    json.dump(
        city_locations_df.dropna().to_dict('records'), f)
    
with open("src/budget_data.json", "w+") as f:
    json.dump(
        budget_data_df.dropna().to_dict('index'), f
    )

print("SUCCESS! GO UPLOAD THEM TO S3.")