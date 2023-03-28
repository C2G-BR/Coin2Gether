import pandas as pd
import json
import itertools

def raw_to_json(df):
    intents = []
    for index, row in df.iterrows():
        intent = {}
        intent['tag'] = row['Tag']
        patterns = row['Patterns'].strip(' ').strip(';').strip(' ').split(';') #Striptease for geeks
        intent['patterns'] = [pattern.strip() for pattern in patterns]
        responses = row['Response'].strip(' ').strip(';').strip(' ').split(';') #Striptease for geeks
        intent['responses'] = [response.strip() for response in responses]
        intents.append(intent)
    return intents


def unzip_entities(intents, parent_tags):

    for parent_tag in parent_tags:
        parent_patterns = next(intent['patterns'] for intent in intents if intent['tag'] == parent_tag)
        parent_responses = next(intent['responses'] for intent in intents if intent['tag'] == parent_tag)
        entities = []
        for intent in intents:
            if intent['tag'].startswith(f'{parent_tag}_'):
                entities = intent['patterns']
                new_patterns = [parent_pattern.replace('__', entity) for parent_pattern, entity in itertools.product(parent_patterns, entities)]
                intent['patterns'] = new_patterns
                
                new_response = [parent_response.replace('__', response) for parent_response, response in itertools.product(parent_responses, intent['responses'])]
                intent['responses'] = new_response
                
        intents = list(filter(lambda intent: (intent['tag'] != parent_tag), intents))            

    return intents


def split_entities(intents, parent_tags):

    new_intents = unzip_entities(intents, parent_tags) #Seiteneffekte einfach hopps genommen

    splitted_data = {}

    for parent_tag in parent_tags:
        #Step 1:
        parent_patterns = next(intent['patterns'] for intent in intents if intent['tag'] == parent_tag)
        entities = []
        new_patterns = []
        for intent in intents:
            if intent['tag'].startswith(f'{parent_tag}_'):
                new_patterns += intent['patterns']
        for intent in intents:
            if intent['tag'] == parent_tag:
                intent['patterns'] = new_patterns

        intents = list(filter(lambda intent:  not (intent['tag'].startswith(f'{parent_tag}_')), intents))

        #Step 2:
        splitted_data[parent_tag] = list(filter(lambda intent: (intent['tag'].startswith(f'{parent_tag}_')), new_intents))

    # intents
    return intents, splitted_data


def tags_patterns_mix(unzipped_data):
    df = pd.DataFrame()
    tags_patterns = []
    for d in unzipped_data:
        tag = d['tag']
        for pattern in d['patterns']:
            tags_patterns.append((tag, pattern))

    return pd.DataFrame(tags_patterns, columns = ['tag', 'pattern'])

def get_responses(data):
    r = {}
    for d in data:
        tag = d['tag']
        responses = d['responses']
        r[tag] = responses
    return r


def remove_fallback(data, fallback = 'fallback'):
    for d in data:
        if d['tag'] == 'fallback':
            data.remove(d)
    return data