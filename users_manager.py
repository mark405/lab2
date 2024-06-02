from encoding_utils import name_hash


class UserManager:
    def __init__(self, tree):
        self.tree = tree

    def add_user(self, name):
        key = name_hash(name)
        self.tree.insert(key, name)
        print(f"User '{name}' added with key {key}.")

    def search_user(self, name):
        key = name_hash(name)
        result = self.tree.search(key)
        if result:
            print(f"User found: {result}")
        else:
            print(f"User '{name}' not found.")

    def delete_user(self, name):
        key = name_hash(name)
        self.tree.delete(key)
        print(f"User '{name}' deleted.")

    def search_greater_or_less(self, name, greater=True):
        key = name_hash(name)
        results = self.tree.search_range(key, greater)
        print(f"Users greater than '{name}': {results}")
