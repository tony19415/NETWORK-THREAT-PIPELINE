import pandas as pd
import hashlib
import logging
from sqlalchemy import create_engine
import os

# Configure enterprise-grade logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def hash_ip_address(ip: str, salt: str) -> str:
    """
    Hashes an IP address with a salt for GDPR pseudonymization.
    Returns None if the IP is null or empty.
    """
    if not ip or pd.isna(ip) or str(ip).strip() == "":
        return None
    return hashlib.sha256((str(ip) + salt).encode('utf-8')).hexdigest()

def extract_and_clean(file_path: str, row_limit: int = 100000) -> pd.DataFrame:
    """
    Reads raw CSV data and standardizes column names.
    """
    logging.info(f"Extracting data from {file_path}")
    df = pd.read_csv(file_path, nrows=row_limit, low_memory=False)

    # CIC-IDS datasets have terrible column formatting, standardize them
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

def apply_gdpr_masking(df: pd.DataFrame, salt: str) -> pd.DataFrame:
    """
    Identifies PII columns and applies the SHA-256 hash.
    """
    logging.info("Applying GDPR masking to network IP addresses...")

    if 'src_ip' in df.columns and 'dst_ip' in df.columns:
        df['src_ip_hashed'] = df['src_ip'].apply(lambda x: hash_ip_address(x, salt))
        df['dst_ip_hashed'] = df['dst_ip'].apply(lambda x: hash_ip_address(x, salt))

        # Drop original unhashed columns so they never enter the database
        df = df.drop(columns=['src_ip', 'dst_ip'])
    else:
        logging.warning(f"IP columns not found. Found columns: {list(df.columns[:5])}. Bypassing masking.")

    return df

def load_to_postgres(df: pd.DataFrame, db_uri: str, table_name: str):
    """
    Loads the transformed dataframe into the raw layer of the data warehouse.
    """

    logging.info(f"Loading {len(df)} rows to database table: public.{table_name}")

    if "postgresql://" in db_uri and "psycopg2" not in db_uri:
        db_uri = db_uri.replace("postgresql://", "postgresql+psycopg2://")
    
    engine = create_engine(db_uri)

    with engine.begin() as connection:
        df.to_sql(table_name, con=connection, schema='public', if_exists='replace', index=False)
    
    logging.info("Data ingestion completed successfully.")

if __name__ == "__main__":
    RAW_FILE_PATH = "data/raw/Friday-WorkingHours.csv"
    GDPR_SALT = "darktrace_secure_salt_2026"

    DB_URI = "postgresql+psycopg2://darktrace_admin:securepassword123@postgres-dw:5432/threat_intelligence"

    try:
        raw_df = extract_and_clean(RAW_FILE_PATH)
        secure_df = apply_gdpr_masking(raw_df, GDPR_SALT)
        load_to_postgres(secure_df, DB_URI, "raw_network_logs")
    except Exception as e:
        logging.error(f"Pipeline execution failed: {e}")
        raise
