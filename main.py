import os

import pandas as pd
from util.app_engine import search_max_documents
from util.s3 import store_output_in_s3
from util.env import ENGINE_NAME, SOURCES

CSV_URL = 'data/synoniemen.csv'


def _search_filters():
    if len(SOURCES) == 0:

    return {'source': SOURCES.split(',')}


def _fetch_organisation_array_from_excel() -> list[str]:
    organisations = pd.read_csv(CSV_URL, sep=';')

    # Remove whitespaces
    organisations.columns.str.strip()

    organisations = organisations.apply(
        lambda x: list(
            filter(pd.notna, [
                x['Organisatie'],
                x['Synoniem 1'],
                x['Synoniem 2'],
                x['Synoniem 3']
            ])
        ),
        axis=1)

    return organisations


def _find_hits_for_organisation(search_terms: list[str]) -> list[dict]:
    main_term = search_terms[0]
    results = list(
        map(
            lambda result: {
                'organisation': main_term,
                **result
            },
            _search(search_terms)
        )
    )

    return results


def _search(search_terms: list[str]) -> list[dict]:
    results = []
    for search_term in search_terms:
        term_results = search_max_documents({
            'query': f"""\"{search_term}\"""",
            'engine_name': ENGINE_NAME,
            'filters': _search_filters()
        })

        term_results_fmt = list(
            map(
                lambda result: {
                    'score': result['score'],
                    'uid': result['id'],
                    'title': result['title'],
                    'doc_url': result['url'],
                    'is_vo': False,
                    'ministries': [],
                    'publish_date': result['date'][0:10]
                },
                term_results['documents']
            )
        )
        results.extend(term_results_fmt)

    return results


def main() -> None:
    organisations = _fetch_organisation_array_from_excel()
    print(f"Fetched {len(organisations)} organisations from Excel")

    results = []
    for i, organisation in enumerate(organisations):
        new_results = _find_hits_for_organisation(organisation)
        results.extend(new_results)

        if i % 10 == 0 and i > 0:
            print(f"{i} organisations completed")

    df = pd.DataFrame.from_dict(results)
    local_file_path = 'output/tmp.xlsx'
    df.to_excel(
        local_file_path,
        index=False
    )

    store_output_in_s3(file_path=local_file_path)

    # Remove tmp file
    os.remove(local_file_path)

    print(f"Total {len(results)} hits found and stored in S3")


if __name__ == '__main__':
    main()
