import pandas as pd
import numpy as np

def clean_ecommerce_data(file_path):
    print("Loading raw dataset...")
    # Load the raw data
    df = pd.DataFrame(pd.read_csv(file_path))
    
    print("Starting data cleaning pipeline...")
    
    # 1. Handle Missing Values in Demographics
    # For gender, missing data is a category of its own. We map nulls to 'Unknown' 
    # to avoid dropping valuable transaction history for those users.
    if 'gender' in df.columns:
        df['gender'] = df['gender'].fillna('Unknown')
        # Standardize text formatting (e.g., 'male', 'M' -> 'Male')
        df['gender'] = df['gender'].str.title().replace({'M': 'Male', 'F': 'Female'})
    
    # 2. Standardize Categorical Business Logic
    # Ensure churn_status is highly readable for the BI tool (Power BI)
    if 'churn_status' in df.columns:
        # Assuming raw data came in as 1/0 or boolean
        df['churn_status'] = df['churn_status'].replace({
            1: 'Churned', 
            0: 'Active',
            True: 'Churned',
            False: 'Active'
        })
        
    # 3. Handle Outliers and Invalid Data
    # Age cannot be negative or unrealistically high. 
    # Cap age at a reasonable limit and drop negative values if they exist.
    if 'age' in df.columns:
        df = df[(df['age'] > 0) & (df['age'] < 100)]
        
    # 4. Fill Nulls in Operational Metrics
    # If a user has no support tickets, it means 0 tickets, not a missing record.
    if 'num_support_tickets' in df.columns:
        df['num_support_tickets'] = df['num_support_tickets'].fillna(0)
        
    # 5. Data Type Formatting
    # Ensure currency and numerical columns are the correct type for MySQL ingestion
    if 'total_spend_inr' in df.columns:
        df['total_spend_inr'] = df['total_spend_inr'].round(2)
        
    if 'tenure_months' in df.columns:
        df['tenure_months'] = df['tenure_months'].astype(int)

    # 6. Drop Duplicates
    # Ensure no duplicate customer_ids accidentally inflate our revenue metrics
    if 'customer_id' in df.columns:
        initial_rows = len(df)
        df = df.drop_duplicates(subset=['customer_id'])
        print(f"Dropped {initial_rows - len(df)} duplicate records.")

    print("Data cleaning complete.")
    return df

if __name__ == "__main__":
    # Define input and output paths
    INPUT_FILE = "data/raw_ecommerce_data.csv"
    OUTPUT_FILE = "data/cleaned_ecommerce_data.csv"
    
    # Execute the cleaning function
    try:
        cleaned_data = clean_ecommerce_data(INPUT_FILE)
        
        # Export the clean data ready for MySQL and Power BI
        cleaned_data.to_csv(OUTPUT_FILE, index=False)
        print(f"Successfully saved cleaned dataset to {OUTPUT_FILE}")
        
    except FileNotFoundError:
        print(f"Error: Could not find the file at {INPUT_FILE}. Please check the path.")