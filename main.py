import os

import pandas as pd
from util.app_engine import search_max_documents
from util.logger import logger
from util.s3 import store_output_in_s3
from util.env import ENGINE_NAME, SOURCES

CSV_URL = "data/synoniemen.csv"


def _search_filters():
    if len(SOURCES) == 0:
        return {}

    return {"doc_source": SOURCES.split(",")}


def _fetch_organisation_array_from_excel() -> list[str]:
    organisations = pd.read_csv(CSV_URL, sep=";")

    # Remove whitespaces
    organisations.columns.str.strip()

    organisations = organisations.apply(
        lambda x: list(
            filter(
                pd.notna,
                [x["Organisatie"], x["Synoniem 1"], x["Synoniem 2"], x["Synoniem 3"]],
            )
        ),
        axis=1,
    )

    return organisations


def _find_hits_for_organisation(search_terms: list[str]) -> list[dict]:
    main_term = search_terms[0]
    results = [
        {"organisation": main_term, **result} for result in _search(search_terms)
    ]

    return results


def safe_key_or_none(key: str, dictionary: dict) -> str:
    if key in dictionary.keys():
        return dictionary[key]

    return None


def _search(search_terms: list[str]) -> list[dict]:
    results = []
    for search_term in search_terms:
        term_results = search_max_documents(
            {
                "query": f"""\"{search_term}\"""",
                "engine_name": ENGINE_NAME,
                "filters": _search_filters(),
            }
        )

        term_results_fmt = [
            {
                "score": result["score"],
                "uid": result["id"],
                "title": result["title"],
                "source": result["doc_source"],
                "doc_url": result["url"],
                "is_vo": False,
                "kind": safe_key_or_none("meta_bulk_key", result),
                "ministries": safe_key_or_none("meta_ministries", result),
                "publish_date": result["date"][0:10],
            }
            for result in term_results["documents"]
        ]

        results.extend(term_results_fmt)

    # Since we have multiple terms, we need to remove duplicates
    # The reason for the double reverse is that we want to keep the score of the first term
    # v['uid'] overrides the last value (and thus the score)
    results.reverse()

    unique_results = list({v["uid"]: v for v in results}.values())
    unique_results.reverse()

    return unique_results


def main() -> None:
    organisations = _fetch_organisation_array_from_excel()
    logger.info(f"Fetched {len(organisations)} organisations from Excel")

    results = []
    for i, organisation in enumerate(organisations):
        new_results = _find_hits_for_organisation(organisation)
        results.extend(new_results)

        if i % 10 == 0 and i > 0:
            logger.info(f"{i} organisations completed")

    df = pd.DataFrame.from_dict(results)
    df["j_en_v"] = df["ministries"].apply(
        lambda x: "Justitie en Veiligheid" in (x or [])
    )
    df["ministries"] = df["ministries"].apply(lambda x: ";;".join(x) if x else None)
    local_file_path = "output/tmp.xlsx"
    df.to_excel(local_file_path, index=False)

    target_file_path = store_output_in_s3(file_path=local_file_path)

    # Remove tmp file
    os.remove(local_file_path)

    logger.info(
        f"Total {len(results)} hits found and stored in S3 at {target_file_path}"
    )


if __name__ == "__main__":
    main()
