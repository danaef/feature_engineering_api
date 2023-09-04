import pytest
from fastapi.testclient import TestClient
from app.app import app
import json


@pytest.fixture
def client():
    return TestClient(app)


input_json_file = "data/cvas_data.json"


def test_feature_engineering_customers(client: TestClient): #
    response = client.post("/feature-engineering/customers")  #performs the action being tests
    assert response.status_code == 200  #testing that request was successful
    response_data = response.json()
    first_customer_features = response_data[0]   #getting ready to test first customer's features
    expected_first_customer_features = {   #manually computed values to compare with the returned
        "customer_ID": 1090,
        "annual_income": 41333,
        "COUNT(loans)": 1,
        "MAX(loans.amount)": 2426,
        "MAX(loans.fee)": 199,
        "MEAN(loans.amount)": 2426,
        "MEAN(loans.fee)": 199,
        "MIN(loans.amount)": 2426,
        "MIN(loans.fee)": 199,
        "NUM_TRUE(loans.loan_status)": 0,
        "NUM_TRUE(loans.long_term)": 1,
        "NUM_TRUE(loans.short_term)": 0,
        "PERCENT_TRUE(loans.loan_status)": 0,
        "PERCENT_TRUE(loans.long_term)": 1,
        "PERCENT_TRUE(loans.short_term)": 0
    }

    assert first_customer_features == expected_first_customer_features #testing if dicts are the same


def test_feature_engineering_loans(client: TestClient):
    response = client.post("/feature-engineering/loans")  #performs request tha is being tested
    assert response.status_code == 200   #tests if request was successful
    response_data = response.json()
    first_loan_features = response_data[0]   #retrieves first customer's data
    expected_first_loan_features = {  #manual computation of feature engineered data
        "loan_ID": 10901,
        "customer_ID": 1090,
        "amount": 2426,
        "fee": 199,
        "loan_status": False,
        "long_term": True,
        "short_term": False,
        "DAY(loan_date)": 15,
        "MONTH(loan_date)": 11,
        "YEAR(loan_date)": 2021,
        "customers.annual_income": 41333,
        "fee_to_loan_ratio": 0.0820280297,
        "loan_to_annual_income": 0.0586940217,
        "total_debt": 0,
        "total_paid": 2625
        }

    assert first_loan_features == expected_first_loan_features  #comparison 


def test_get_customer_data(client):             #tests if retrieved data for customer 1512 are correct
    customer_data = [{'customer_ID': '1512',
                      'loan_date': '29/03/2021',
                      'amount': '2114',
                      'fee': '75',
                      'loan_status': '1',
                      'term': 'short',
                      'annual_income': '67215'},
                     {'customer_ID': '1512',
                      'loan_date': '24/10/2019',
                      'amount': '210',
                      'fee': '78',
                      'loan_status': '0',
                      'term': 'long',
                      'annual_income': '67215'}]

    response = client.get("/get_customer/1512")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == customer_data


def test_health_check(client): #tests if request for health check is successful
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "UP"}
