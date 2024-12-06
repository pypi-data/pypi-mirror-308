import string

def clean(name):
    return name.lower().translate(str.maketrans('', '', string.punctuation)).strip()