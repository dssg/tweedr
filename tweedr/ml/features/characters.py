def capitalized(document):
    return [['CAPITALIZED'] if token[0].isupper() else [] for token in document]


def plural(document):
    return [['PLURAL'] if token.endswith('s') else [] for token in document]


def numeric(document):
    return [['NUMERIC'] if token.isdigit() else [] for token in document]


def includes_numeric(document):
    return [['INCLUDES_NUMERIC'] if any(char.isdigit() for char in token) else [] for token in document]
