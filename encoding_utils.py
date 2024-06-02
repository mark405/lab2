def name_hash(name):
    return sum(ord(char) for char in name.lower())