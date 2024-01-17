import os
from typing import Optional

import pymongo
from util.logger import logger
import time
from dotenv import load_dotenv

load_dotenv()


def run_cursor_query(
    query: str, projection: Optional[dict] = None
) -> pymongo.cursor.Cursor:
    client = pymongo.MongoClient(os.environ["MONGO_CONNECTION_STRING"])  # type: ignore

    db_name = os.environ.get("MONGO_DB", "sources")
    if os.environ.get("ENV", "production") == "test":
        db_name = "test_sources"

    db_conn = client[db_name]

    # Fetch documents
    logger.info(f"--- Sending query {query} to MongoDB ---")
    results = db_conn["source_documents"].find(query, projection)

    return results


def search_all_documents(search_terms: list[str], operator: str) -> list[dict]:
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

    documents_cursor = run_cursor_query(query, {"doc_content": 0})

    return list(documents_cursor)


def source_cursor(source: str) -> list[dict]:
    if source != "":
        if "custom" in source:
            raise ValueError("Cannot search for custom sources!")

        query = {"source": {"$regex": source}}

    else:
        query = {"source": {"$not": {"$eq": "custom"}}}

    return run_cursor_query(
        query,
        {
            "downloaded": 0,
            "enriched": 0,
            "local_doc_url": 0,
            "read": 0,
            "stored": 0,
            "version_download": 0,
            "version_enrich": 0,
            "version_read": 0,
            "version_scrape": 0,
            "version_store": 0,
        },
    )
