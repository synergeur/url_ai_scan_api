
from fastapi import APIRouter
from google.cloud import aiplatform
from google.oauth2 import service_account

import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Parse the GOOGLE_CONNECTION environment variable as JSON
google_connection_info = json.loads(os.getenv("GOOGLE_CONNECTION"))

# Create Google Cloud credentials from the parsed JSON
CREDENTIALS = service_account.Credentials.from_service_account_info(google_connection_info)
# Initialize AI Platform with credentials
aiplatform.init(credentials=CREDENTIALS)

MODEL_NAMES = {
    "decision_tree_model": "projet-integration-au-2024.sacha_phishing_url_website.decision_tree_model",
    #"dnn_classifier_model": "projet-integration-au-2024.sacha_phishing_url_website.dnn_classifier_model",
    "logistic_regression_model": "projet-integration-au-2024.sacha_phishing_url_website.logistic_regression_model",
    "random_forest_model": "projet-integration-au-2024.sacha_phishing_url_website.random_forest_model",
    "xgboost_model": "projet-integration-au-2024.sacha_phishing_url_website.xgboost_model"
}
