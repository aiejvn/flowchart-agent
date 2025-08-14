import requests, random ,re

def google_form(results):
    return [f"Title: {x['title']}\n\nSnippet: {x['snippet']}" for x in results]


def vectordb_form(results):
    # print(results[0])
    return [f"Relevance: {x['score']}\nDocument: {re.sub(r'[\s]{2,}', ' ', x['payload']['text'])}" for x in results]

def db_retrieval(node, input, headers):
    if 'query' in node.metadata:
        data = input.get(node.metadata['query'], None)
        if data:
            data = data.value
        data = {'query': data}
        # print(data)
        response = requests.post(url=''.join(['http://', node.url, node.endpoint]), data=data, headers=headers)

        
        res = response.json()
        # print(res)
        text = []
        output_strat = node.metadata['output_strat']
        if output_strat == 'concat':
            text = res
        elif output_strat.startswith('top'): # top k, where k is < 10
            text.extend(res[:int(output_strat[-1])])
        elif output_strat == 'random': # random k, where k is < 10
            text.append(random.sample(res, k=int(output_strat[-1])))

        return text, res
    else:
        return []

OUTPUT_FORMAT_MAPPING = {
    'google.com': google_form, 
    'localhost:4000': vectordb_form, 
}

REQUESTS_MAPPING = {
    'localhost:4000': db_retrieval,
}

EVAL_METRICS = {
    'example.json': ['bleu']
}

PROVIDER_MAPPING = {
    'gpt-4o-mini': 'openai',
    'gpt-4o': 'openai',
    'o3': 'openai',
    'o3-deep-research': 'openai',
    "claude-3-5-sonnet-latest": 'anthropic',

}
