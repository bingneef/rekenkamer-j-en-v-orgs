import os

import pandas as pd
from util.mongo import search_max_documents
from util.logger import logger
from util.s3 import store_output_in_s3


CSV_ORGS_URL = "data/organisations.csv"
CSV_THEMES_URL = "data/themes.csv"


def _fetch_themes_array_from_excel() -> list[str]:
    themes = pd.read_csv(CSV_THEMES_URL, sep=";", keep_default_na=False)

    # Remove whitespaces
    themes.columns.str.strip()

    themes = themes.apply(
        lambda x: {
            "theme": x["Thema"],
            "subtheme": x["Subthema"],
            "keywords": x["Keywords"].split(","),
        },
        axis=1,
    )

    return themes


def _fetch_organisation_array_from_excel() -> list[str]:
    organisations = pd.read_csv(CSV_ORGS_URL, sep=";")

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
        {"organisation": main_term, **result}
        for result in _search(search_terms, operator="OR")
    ]

    return results


def _find_hits_for_themes(search_terms: dict) -> list[dict]:
    theme = search_terms["theme"]
    subtheme = search_terms["subtheme"]
    keywords = search_terms["keywords"]

    results = [
        {"theme": theme, "subtheme": subtheme, **result}
        for result in _search(keywords, operator="AND")
    ]

    return results


def safe_key_or_none(key: str, dictionary: dict) -> str:
    if key in dictionary.keys():
        return dictionary[key]

    return None


def is_vo(uid: str, source: str):
    if source != "rekenkamer":
        return False

    # The uid for rekenkamer reports is like 2023:05:17:{id}
    dateless_uid = uid.split(":")[-1]

    indicators = [
        "resultaten-verantwoordingsonderzoek-",
        "staat-van-de-rijksverantwoording-",
        "rijk-verantwoord-",
    ]

    for indicator in indicators:
        if dateless_uid.find(indicator) == 0:
            return True

    return False


def _dossier_element_from_meta(meta: dict, element: str) -> str:
    if not meta or "dossier" not in meta.keys():
        return "-"

    dossiers = meta["dossier"]
    elements = [str(dossier[element]) for dossier in dossiers]
    return ";;".join(elements)


def fmt_raw_document(document: dict) -> dict:
    return {
        "uid": document["remote_uid"],
        "title": document["title"],
        "source": document["source"],
        "doc_url": document["doc_url"],
        "is_vo": is_vo(document["remote_uid"], document["source"]),
        "kind": safe_key_or_none("bulk_key", document["meta"]),
        "publish_date": document["date"][0:10],
        "meta.file_dossier_numbers": _dossier_element_from_meta(
            document["meta"], "nummer"
        ),
        "meta.file_dossier_titles": _dossier_element_from_meta(
            document["meta"], "title"
        ),
    }


def _search(search_terms: str | list[str], operator: str) -> list[dict]:
    if type(search_terms) == str:
        search_terms = [search_terms]

    raw_documents = search_max_documents(search_terms, operator)
    return [fmt_raw_document(document) for document in raw_documents]


def main(kind: str = "orgs") -> None:
    if kind not in ["orgs", "themes"]:
        raise ValueError("kind must be either orgs or themes")

    if kind == "themes":
        search_array = _fetch_themes_array_from_excel()
        search_func = _find_hits_for_themes
    else:
        search_array = _fetch_organisation_array_from_excel()
        search_func = _find_hits_for_organisation

    logger.info(f"Fetched {len(search_array)} {kind} to search from Excel")

    results = []
    for i, organisation in enumerate(search_array):
        new_results = search_func(organisation)
        results.extend(new_results)

        if i % 10 == 0 and i > 0:
            logger.info(f"{i} {kind} completed")

    df = pd.DataFrame.from_dict(results)

    local_file_path = "output/tmp.xlsx"
    df.to_excel(local_file_path, index=False)

    target_file_path = store_output_in_s3(file_path=local_file_path, kind=kind)

    # Remove tmp file
    os.remove(local_file_path)

    logger.info(
        f"Total {len(results)} hits found and stored in S3 at {target_file_path}"
    )


if __name__ == "__main__":
    kind = os.environ.get("KIND", "orgs")
    main(kind=kind)
