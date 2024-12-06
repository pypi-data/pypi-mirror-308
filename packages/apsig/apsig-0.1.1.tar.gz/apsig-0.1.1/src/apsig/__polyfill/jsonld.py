import json

def load_json_ld(json_ld_str):
    """JSON-LD文字列を辞書型にロードする"""
    return json.loads(json_ld_str)

def apply_context(data, context):
    """コンテキストを適用して、プレフィックスを解決する"""
    if '@context' in data:
        context.update(data['@context'])
    expanded_data = {}
    for key, value in data.items():
        if key == '@context':
            continue
        expanded_key = expand_key(key, context)
        expanded_data[expanded_key] = value
    return expanded_data

def expand_key(key, context):
    if key in context:
        return context[key]
    return key

def expand(data):
    context = {}
    if '@context' in data:
        context = data['@context']
    return apply_context(data, context)

def normalize(data):
    return json.dumps(data, indent=2)