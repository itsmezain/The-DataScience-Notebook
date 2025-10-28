import nlpcloud


def ner(text, entity_to_search):
    client = nlpcloud.Client(
        "en_core_web_lg", "a4b863cef52368fd3440f4556fc38a72dfbb1f88", gpu=False
    )
    response = client.entities(
        text,
        searched_entity=entity_to_search,
    )
    return response