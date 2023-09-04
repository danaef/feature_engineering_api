import featuretools as ft
import pandas as pd
import json


def preprocess_customer_data(customer_loans):
    customer_data = []
    loan_data = []
    loan_counter = dict()

    for customer in customer_loans:
        customer_id = customer["customer_ID"]
        annual_income = customer["loans"][0]["annual_income"]
        customer_data.append({'customer_ID': customer_id, "annual_income": annual_income})

        if customer_id not in loan_counter:
            loan_counter[customer_id] = 0

        for loan in customer['loans']:
            loan_counter[customer_id] += 1
            loan_id = customer_id + str(loan_counter[customer_id])
            loan_data.append({
                'loan_ID': loan_id,
                'customer_ID': customer_id,
                'loan_date': pd.to_datetime(loan['loan_date'], format='%d/%m/%Y'),
                'amount': int(loan['amount']),
                'fee': int(loan['fee']),
                'loan_status': True if loan['loan_status'] == '1' else False,
                'long_term': (loan['term'] == 'long'),
                'short_term': (loan['term'] == 'short'),
            })

    return pd.DataFrame(customer_data), pd.DataFrame(loan_data)


def create_entity_set_and_features(customer_df, loan_df):
    dataframes = {
        'customers': (customer_df, 'customer_ID'),
        'loans': (loan_df, 'loan_ID')
    }

    relationships = [
        ("customers", 'customer_ID', "loans", 'customer_ID')
    ]

    my_es = ft.EntitySet(id="my_es", dataframes=dataframes, relationships=relationships)

    feature_mat_customers, feature_defs_customers = ft.dfs(entityset=my_es,
                                                           target_dataframe_name='customers',
                                                           agg_primitives=['count', 'mean', 'min', 'max',
                                                                           'percent_true', 'num_true'],
                                                           trans_primitives=[],
                                                           verbose=True)

    feature_mat_loans, feature_defs_loans = ft.dfs(entityset=my_es,
                                                   target_dataframe_name='loans',
                                                   trans_primitives=['day', 'month', 'year'],
                                                   agg_primitives=[],
                                                   verbose=True)
    feature_mat_loans.reset_index(drop=False, inplace=True)
    feature_mat_customers.reset_index(drop=False, inplace=True)
    return feature_mat_customers, feature_mat_loans


def extra_feature_engineering(df):
    df_grouped = df.groupby("customer_ID").apply(lambda x: pd.Series({
        "fee_to_loan_ratio": (x["fee"].sum() / x["amount"].sum()) if x["amount"].sum() > 0 else 0,
        "loan_to_annual_income": (x["amount"].sum() / x['customers.annual_income'].sum()
                                  ) if x['customers.annual_income'].sum() > 0 else 0
    })).reset_index()

    df_grouped["total_debt"] = df_grouped.apply(lambda x: (
            df[(df["customer_ID"] == x["customer_ID"]) & df["loan_status"]]["amount"].sum() +
            df[(df["customer_ID"] == x["customer_ID"]) & df["loan_status"]]["fee"].sum()
    ) if x["customer_ID"] in df[df["loan_status"]]["customer_ID"].values else 0, axis=1)

    df_grouped["total_paid"] = df_grouped.apply(lambda x: (
            df[(df["customer_ID"] == x["customer_ID"]) & ~df["loan_status"]]["amount"].sum() +
            df[(df["customer_ID"] == x["customer_ID"]) & ~df["loan_status"]]["fee"].sum()
    ) if x["customer_ID"] in df[~df["loan_status"]]["customer_ID"].values else 0, axis=1)

    merged_df = df.join(df_grouped.set_index('customer_ID'), on='customer_ID', how='left')
    merged_df.reset_index(drop=False, inplace=True)
    return merged_df


def feature_engineering_final(json_data):
    customer_df, loan_df = preprocess_customer_data(json_data)
    feature_mat_customers, feature_mat_loans = create_entity_set_and_features(customer_df, loan_df)
    feature_mat_loans = extra_feature_engineering(feature_mat_loans)

    # Convert DataFrames to JSON format
    feature_mat_customers_json = feature_mat_customers.to_json(orient="records")
    feature_mat_loans_json = feature_mat_loans.to_json(orient="records")

    combined_features = {
        "customers_features": json.loads(feature_mat_customers_json),
        "loans_features": json.loads(feature_mat_loans_json)
    }

    return combined_features
