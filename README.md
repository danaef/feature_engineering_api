# FastAPI Feature Engineering API
This is a FastAPI-based API for performing feature engineering on financial data consisting of customer and loan information. The API allows you to automate feature engineering using FeatureTools, manually compute certain features, and interact with the data via various endpoints. Additionally, it can be deployed using Docker for easy access.

## Features
Automated Feature Engineering: You can perform automated feature engineering on both customer and loan data using the /feature-engineering/customers and /feature-engineering/loans endpoints, respectively. This leverages FeatureTools to create valuable features from your data.

Manual Feature Engineering: The API also includes manual feature engineering for additional insights. Features like fee to loan ratio, fee to annual income ratio, total debt, and total paid are computed.

Data Retrieval: You can retrieve feature-engineered data for both customers and loans using the /feature-engineering/get_customers and /feature-engineering/get_loans endpoints.

Data Modification: The API allows you to update the loan status of a specific loan using the /update_loan_status/{updated_status} endpoint. This feature is useful for marking loans as paid and adjusting total debt and total paid accordingly.

Customer Information: Retrieve information about a specific customer by their ID using the /get_customer/{customer_id} endpoint.

Customer Deletion: Delete a customer and their associated transactions using the /customer/{customer_id} endpoint.

Health Check: You can check if the API is running smoothly by accessing the /health endpoint.

Getting Started
Prerequisites
Python 3.7 or higher
Docker (optional)
Installation
Clone this repository to your local machine.

Install the required Python packages by running:

Copy code
pip install -r requirements.txt
Running the API
Without Docker
Run the API locally using the following command:

css
Copy code
uvicorn main:app --host 0.0.0.0 --port 8080
Access the API documentation at http://127.0.0.1:8080/docs to interact with the endpoints.

With Docker (Optional)
Build the Docker image from the project directory:

Copy code
docker build -t fastapi .
Run the Docker container:

arduino
Copy code
docker run -d -p 8080:8080 fastapi
Access the API documentation at http://127.0.0.1:8080/docs to interact with the endpoints.

Unit Testing
Unit tests for the API are available in the tests directory. You can run them using pytest:

Copy code
pytest tests
Future Enhancements
Here are some ideas for future enhancements:

Dynamic Operations: Add endpoints for creating new loans, adding new customers, and deleting specific loans or customers.

Active Loans: Create an endpoint to retrieve customers with at least one active loan and loans that are currently active.

Loan Status Changes: Implement functionality to change the status of a loan (e.g., from active to inactive) when a customer pays. Update the total debt and total paid accordingly.

Feel free to contribute to this project and expand its functionality further.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
FastAPI
FeatureTools
Docker
pytest
Thank you for using this FastAPI Feature Engineering API! If you have any questions or encounter issues, please open an issue in the GitHub repository.
