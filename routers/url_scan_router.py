from fastapi import APIRouter, Depends, HTTPException
from google.cloud import bigquery
from google.oauth2 import service_account
import logging
import datetime

# Import for token auth
from auth.admin_auth import verify_token
from auth.google_auth import CREDENTIALS, MODEL_NAMES

# Import for data models
from models.url_scan_models import AutoAiScan, ModelFeatures
from shared.utils import calculate_url_features

# Set up logging
logging.basicConfig(level=logging.INFO)

router = APIRouter()

# Initialize BigQuery client
bigquery_client = bigquery.Client(credentials=CREDENTIALS)

@router.post('/automatic_ai_scan')
async def scan_url(request: AutoAiScan, token_data: dict = Depends(verify_token)):
    """
    Scans the provided URL using multiple AI models in BigQuery to check if it's a scam.
    Returns predictions from each model.
    """
    
    # Calculate features based on the input URL
    features = calculate_url_features(request.url)

    results = {}
    try:
        # Iterate over each model table and request a prediction
        for model_name, table_id in MODEL_NAMES.items():
            logging.info(f"Processing model: {model_name} with table: {table_id}")
            
            try:
                # Construct the SQL query for prediction
                query = f"""
                SELECT
                    *
                FROM
                    ML.PREDICT(MODEL `{table_id}`, 
                               (SELECT 
                                    {features["IsDomainIP"]} AS IsDomainIP,
                                    {features["NoOfAmpersandInURL"]} AS NoOfAmpersandInURL,
                                    {features["TLDLegitimateProb"]} AS TLDLegitimateProb,
                                    {features["TLDLength"]} AS TLDLength,
                                    {features["LargestLineLength"]} AS LargestLineLength,
                                    {features["Robots"]} AS Robots,
                                    {features["NoOfURLRedirect"]} AS NoOfURLRedirect,
                                    {features["NoOfPopup"]} AS NoOfPopup,
                                    {features["HasExternalFormSubmit"]} AS HasExternalFormSubmit,
                                    {features["HasHiddenFields"]} AS HasHiddenFields,
                                    {features["HasPasswordField"]} AS HasPasswordField,
                                    {features["Bank"]} AS Bank,
                                    {features["Pay"]} AS Pay,
                                    {features["Crypto"]} AS Crypto,
                                    {features["NoOfiFrame"]} AS NoOfiFrame,
                                    {features["NoOfEmptyRef"]} AS NoOfEmptyRef
                               ))
                """

                # Execute the query
                query_job = bigquery_client.query(query)
                prediction = query_job.result()  # Wait for the query to complete

                # Store the prediction results
                for row in prediction:
                    model_result = row.get("predicted_label", "No prediction available")
                    results[model_name] = model_result

            except Exception as model_error:
                logging.error(f"Error processing model {model_name}: {model_error}")
                results[model_name] = "Prediction failed"

    except Exception as e:
        logging.error(f"General error during URL scanning: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while scanning the URL: {str(e)}")

    return results

@router.post('/manual_ai_scan')
async def scan_with_features(features: ModelFeatures, token_data: dict = Depends(verify_token)):
    """
    Accepts all features directly in the request body and uses them to make predictions 
    with each model in BigQuery.
    """
    
    results = {}
    try:
        # Iterate over each model table and request a prediction
        for model_name, table_id in MODEL_NAMES.items():
            logging.info(f"Processing model: {model_name} with table: {table_id}")
            
            try:
                # Construct the SQL query for prediction using provided features
                query = f"""
                SELECT
                    *
                FROM
                    ML.PREDICT(MODEL `{table_id}`, 
                               (SELECT 
                                    {features.IsDomainIP} AS IsDomainIP,
                                    {features.NoOfAmpersandInURL} AS NoOfAmpersandInURL,
                                    {features.TLDLegitimateProb} AS TLDLegitimateProb,
                                    {features.TLDLength} AS TLDLength,
                                    {features.LargestLineLength} AS LargestLineLength,
                                    {features.Robots} AS Robots,
                                    {features.NoOfURLRedirect} AS NoOfURLRedirect,
                                    {features.NoOfPopup} AS NoOfPopup,
                                    {features.HasExternalFormSubmit} AS HasExternalFormSubmit,
                                    {features.HasHiddenFields} AS HasHiddenFields,
                                    {features.HasPasswordField} AS HasPasswordField,
                                    {features.Bank} AS Bank,
                                    {features.Pay} AS Pay,
                                    {features.Crypto} AS Crypto,
                                    {features.NoOfiFrame} AS NoOfiFrame,
                                    {features.NoOfEmptyRef} AS NoOfEmptyRef
                               ))
                """

                # Execute the query
                query_job = bigquery_client.query(query)
                prediction = query_job.result()  # Wait for the query to complete

                # Store the prediction results
                for row in prediction:
                    model_result = row.get("predicted_label", "No prediction available")
                    results[model_name] = model_result

            except Exception as model_error:
                logging.error(f"Error processing model {model_name}: {model_error}")
                results[model_name] = "Prediction failed"

    except Exception as e:
        logging.error(f"General error during URL scanning: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while scanning the URL: {str(e)}")

    return results

@router.get('/news_date')
async def scan_url():
    """
    return the news timestamp
    """

    return 1734238800
