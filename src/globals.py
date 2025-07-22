import requests

def google_form(results):
    return [f"Title: {x['title']}\n\nSnippet: {x['snippet']}" for x in results]


def vectordb_form(results):
    return [f"Relevance: {x['score']}\nDocument: {x['payload']['text']}" for x in results]

OUTPUT_FORMAT_MAPPING = {
    'google.com': google_form, 
    'localhost:4000': vectordb_form, 
}

REQUESTS_MAPPING = {
    'localhost:4000': requests.post, 
}

EVAL_METRICS = {
    'example.json': ['bleu']
}
