# pylint: disable=missing-module-docstring
from pathlib import Path
from flask import jsonify, current_app, Response


def ping() -> Response:
    """Test route to verify that the server is online."""
    return jsonify({'message': 'pong'})


def list_indices() -> Response:
    """Route to list Elasticsearch indexes."""
    return current_app.elastic_query_conn.get_indices()  # type: ignore


def retrieve_document(index_id: str, document_id: str) -> Response:
    """Route to retrieve a document by its ID."""
    document = (current_app.elastic_query_conn  # type: ignore
                .get_document_by_id(index_id, document_id))
    return jsonify(document)


def list_wet_processes() -> Response:
    """Route to list wet processes."""
    wet_processes_index = f"{current_app.config['GENAPI_ES_INDEX_PREFIX']}-wet_processes"
    result = (current_app.elastic_query_conn  # type: ignore
              .get_field_values(wet_processes_index, "proc_id"))
    return jsonify(list(result))


def list_bi_processes() -> Response:
    """Route to list bi processes."""
    bi_processes_index = f"{current_app.config['GENAPI_ES_INDEX_PREFIX']}-bi_processes"
    result = (current_app.elastic_query_conn  # type: ignore
              .get_field_values(bi_processes_index, "name"))
    return jsonify(list(result))


def list_analyses() -> Response:
    """Route to list analyses."""
    analyses_index = f"{current_app.config['GENAPI_ES_INDEX_PREFIX']}-analyses"
    result = current_app.elastic_query_conn.get_field_values(analyses_index, "path")  # type: ignore
    filenames = [Path(path).name for path in result]
    return jsonify(filenames)


def list_analyses_wet_processes(proc_id: str) -> Response:
    """Route to list analyses one of specific wet process"""
    analyses_index = f"{current_app.config['GENAPI_ES_INDEX_PREFIX']}-analyses"

    search_query = {
        "query": {
            "term": {
                "metadata.wet_process.keyword": proc_id,
            }
        }
    }
    result = []
    response = (current_app.elastic_query_conn  # type: ignore
                .client.search(index=analyses_index, body=search_query))
    for hit in response['hits']['hits']:
        result.append(hit['_source']['path'])

    return jsonify(result)


def list_analyses_bi_processes(proc_id: str) -> Response:
    """Route to list analyses one of specific bi process"""
    analyses_index = f"{current_app.config['GENAPI_ES_INDEX_PREFIX']}-analyses"

    search_query = {
        "query": {
            "term": {
                "metadata.bi_process.keyword": proc_id,
            }
        }
    }
    result = []
    response = (current_app.elastic_query_conn  # type: ignore
                .client.search(index=analyses_index, body=search_query))
    for hit in response['hits']['hits']:
        result.append(hit['_source']['path'])

    return jsonify(result)
