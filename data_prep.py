import pandas as pd
import json
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
from latlon import latlon

def prep_data(df, X_col, y_col, test_size=0.35):
    return train_test_split(df[[X_col]], df[[y_col]], test_size=test_size)

def predict_coords(coords_df, l, c):
    lr = LinearRegression()
    X_train, X_test, y_train, y_test = prep_data(coords_df.dropna(), l, c)
    lr.fit(X_train, y_train)
    for _ in range(5):
        print(lr.score(X_test, y_test))
    return lr

def prep_coords(coords_path, latlon=False):
    coords = pd.read_csv(coords_path).query("use=='x'")
    coords['id'] = coords.apply(
        lambda r: "_".join(
            [r['state'].lower(), r['city'].lower()]
        ).replace(" ", ""), 1
    )
    coords['name'] = coords.apply(
            lambda r: ", ".join(
                [r['city'].title(), r['state']]
            ), 1
        )
    coords = coords[['id', 'name', 'x', 'y']].dropna()
    if latlon:
        latlon2 = {}
        for k,v in latlon.items():
            k_ = "_".join([
                k.split(", ")[1].lower(),
                k.split(", ")[0].lower(),
            ]).replace(" ", "")
            latlon2[k_] = {
                "lat": v[0],
                "lon": v[1]
            }
        coords = pd.DataFrame(latlon2).T.join(
            coords[['x ', 'y', 'name']].set_index("name")
            )

    return coords

def prep_budget(budget_path):
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
    df_ = df.query("year==2023")[['id', 'name', 'budget type', 'budget']].set_index('id')
    df_.rename(columns={'budget type':'budget_type'}, inplace=True)
    all_budget_df = df_.query("budget_type=='p23'").rename(columns={'budget':'police'}).drop('budget_type', axis=1).join(
        df_.query("budget_type=='gf23'").rename(columns={'budget':'general_fund'}).drop(['budget_type', 'name'], axis=1),
        on='id'
    )
    return all_budget_df

def create_data(predict=True):
    if predict:
        all_coords = prep_coords('coordinate_df.csv', latlon=True)
        lr_x = predict_coords(all_coords, 'lon', 'x')
        lr_y = predict_coords(all_coords, 'lat', 'y')
        all_coords['x'] = np.concatenate(lr_x.predict(all_coords[['lon']]))
        all_coords['y'] = np.concatenate(lr_y.predict(all_coords[['lat']]))
    else:
        all_coords = prep_coords('coordinate_df.csv')
    all_budget_df = prep_budget('budget_data.csv')

    big_df = pd.merge(all_coords.reset_index(names="id"), all_budget_df, on='id').dropna()
    for c in ['police', 'general_fund']:
        big_df[c] = big_df[c].map(lambda p: p.replace("$", "").replace(",", ""))

    with open("city_locations.json", "w+") as f:
        json.dump(
            big_df.rename(
                columns={'x':'cx', 'y':'cy'}
            )[['id', 'name', 'cx', 'cy']].dropna().to_dict('records'), f)
        
    with open("budget_data.json", "w+") as f:
        json.dump(
            big_df.rename(
                columns={'police':'policeBudget', 'general_fund':'totalBudget'}
            ).set_index('id')[['name', 'policeBudget', 'totalBudget']].dropna().to_dict('index'), f
        )

coords = pd.read_csv('coordinate_df.csv').query("use=='x'")
coords['id'] = coords.apply(
    lambda r: "_".join(
        [r['state'].lower(), r['city'].lower()]
    ).replace(" ", ""), 1
)
coords['name'] = coords.apply(
        lambda r: ", ".join(
            [r['city'].title(), r['state']]
        ), 1
    )
coords = coords[['id', 'name', 'x', 'y']].dropna()
all_budget_df = prep_budget('budget_data.csv')
big_df = pd.merge(coords.reset_index(names="id"), all_budget_df, on='id').dropna()
for c in ['police', 'general_fund']:
    big_df[c] = big_df[c].map(lambda p: p.replace("$", "").replace(",", ""))

with open("city_locations.json", "w+") as f:
    json.dump(
        big_df.rename(
            columns={'x':'cx', 'y':'cy'}
        )[['id', 'name', 'cx', 'cy']].dropna().to_dict('records'), f)
    
with open("budget_data.json", "w+") as f:
    json.dump(
        big_df.rename(
            columns={'police':'policeBudget', 'general_fund':'totalBudget'}
        ).set_index('id')[['name', 'policeBudget', 'totalBudget']].dropna().to_dict('index'), f
    )

# create_data()