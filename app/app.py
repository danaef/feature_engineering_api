from feature_eng.feature_eng import feature_engineering_final
from fastapi import FastAPI, HTTPException
import json

app = FastAPI()

json_path = 'data/cvas_data.json'
with open(json_path, 'r') as json_file:
    json_data = json.load(json_file)['data']


@app.post("/feature-engineering/customers")  # creates an endpoint to perform feature engineer on the customer data
async def feature_engineering_customers():
    try:
        result = feature_engineering_final(json_data)["customers_features"]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/feature-engineering/loans")
async def feature_engineering_loans():  # creates an endpoint that performs feature engineer on the loan data
    try:
        result = feature_engineering_final(json_data)["loans_features"]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_customer/{customer_id}")
async def get_customer_data(customer_id):   # creates an endpoint that get the information about a specific customer
    for customer in json_data:
        if customer.get("customer_ID") == customer_id:
            return customer["loans"]


def feature_eng_loans():
    return feature_engineering_final(json_data)["loans_features"]


@app.get("/feature-engineering/get_loans")
async def get_feature_engineered_loans():   # gets the feature-engineered loan data
    try:
        result = feature_eng_loans()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/update_loan_status/{updated_status}")
async def update_loan(updated_status):  # changes the loan status of a specific loan
    loans_data = feature_eng_loans()
    for loan in loans_data:
        if loan.get("loan_ID") == 10901:
            loan["loan_status"] = updated_status
            return {"message": f"Loan {10901} status updated successfully to {updated_status}"}
    raise HTTPException(status_code=404, detail="Loan not found")


@app.delete("/customer/{customer_id}")
async def delete_customer(customer_id): # deletes a customer and their transactions
    for customer in json_data:
        if customer.get("customer_ID") == customer_id:
            json_data.remove(customer)
            return {"message": f"Customer with ID {customer_id} deleted"}

    raise HTTPException(status_code=404, detail=f"Customer with ID {customer_id} not found")


@app.get("/health")
async def health_check(): # checks if the api is running
    return {"status": "UP"}
