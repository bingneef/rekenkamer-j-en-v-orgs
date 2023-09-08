import os

import pymongo
from util.logger import logger
import time
from dotenv import load_dotenv

load_dotenv()


def run_query(query: dict, projection: dict) -> list[dict]:
    client = pymongo.MongoClient(os.environ["MONGO_CONNECTION_STRING"])  # type: ignore

    db_name = os.environ.get("MONGO_DB", "sources")
    if os.environ.get("ENV", "production") == "test":
        db_name = "test_sources"

    db_conn = client[db_name]

    # Fetch documents
    logger.info(f"--- Sending query {query} to MongoDB ---")
    results = db_conn["source_documents"].find(query, projection)

    # Convert documents to list
    start_time = time.time()
    documents = list(results)
    logger.info(
        "--- Converted {} document(s) in {:.2f} seconds ---".format(
            len(documents), time.time() - start_time
        )
    )

    # Close connection with MongoDB
    client.close()

    return documents


def search_max_documents(search_terms: list[str], operator: str) -> list[dict]:
    read_chars = "[ \\n.,;]"

    if operator == "AND":
        query_parts = [
            {"doc_content": {"$regex": f"{read_chars}({search_term}){read_chars}"}}
            for search_term in search_terms
        ]
        query = {"$and": query_parts}
    else:
        pattern = f"{read_chars}({'|'.join(search_terms)}){read_chars}"
        query = {"doc_content": {"$regex": pattern}}

    # Ensure source custom is not included!
    query["source"] = {"$not": {"$eq": "custom"}}

    documents = run_query(query, {"doc_content": 0})

    return documents
