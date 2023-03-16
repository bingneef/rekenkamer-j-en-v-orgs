import os

from elastic_enterprise_search import AppSearch

ENGINE_BASE_URL = os.environ['ENGINE_BASE_URL']
ENGINE_AUTH = os.environ['ENGINE_AUTH']


def get_app_search():
    return AppSearch(
        ENGINE_BASE_URL,
        http_auth=ENGINE_AUTH,
    )


def search_max_documents(kwargs):
    results = {'documents': []}

    current_page = 1
    while True:
        print(f"Searching page {current_page}, currently at {(len(results['documents']))} documents")
        search_args = {
            **kwargs,
            'limit': 1000,
            'current_page': current_page
        }
        page_results = search(
            **search_args
        )
        if 'meta' not in results.keys():
            results['meta'] = page_results['meta']

        results['documents'].extend(page_results['documents'])

        all_documents_loaded = len(results['documents']) >= results['meta']['total_documents']
        no_more_new_documents = len(page_results['documents']) == 0

        if all_documents_loaded or no_more_new_documents:
            return results

        current_page += 1


def search(
    query,
    engine_name='source-main',
    limit=10,
    current_page=1,
    filters={},
    result_fields=None
):
    if result_fields is None:
        result_fields = [
            "id",
            "title",
            "url",
            "doc_source",
            "doc_sub_source",
            "date"
        ]

    result_fields_mapped = {}
    for result_field in result_fields:
        result_fields_mapped[result_field] = {'raw': {}}

    data = get_app_search().search(
        engine_name=engine_name,
        query=query,
        page_size=limit,
        current_page=current_page,
        filters=filters,
        search_fields={
            "title": {
                "weight": 10
            },
            "body": {
                "weight": 1
            },
            "url": {
                "weight": 2
            }
        },
        result_fields=result_fields_mapped
    )

    results = []
    for result in data['results']:
        row = {
            'score': result['_meta']['score'] or 0
        }

        for result_field in result_fields:
            try:
                row[result_field] = result[result_field]['raw']
            except KeyError:
                row[result_field] = None

        results.append(row)

    print(f"Found {data['meta']['page']['total_results']} result(s) for {query}")

    return {
        'meta': {
            'total_documents': data['meta']['page']['total_results']
        },
        'documents': results
    }
