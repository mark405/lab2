class BPlusTree:
    def __init__(self, order=4):
        if order < 2 or order > 4:
            raise ValueError("Order must be between 2 and 4")
        self.root = self.BPlusTreeNode(order)
        self.order = order

    def insert(self, key, value):
        self.root.insert(key, value)
        if len(self.root.keys) >= self.order:
            self.root = self.root.split()

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node.leaf:
            for k, v in node.keys:
                if k == key:
                    return v
            return None
        else:
            child_index = node.find_child_index(key)
            return self._search(node.children[child_index], key)

    def search_range(self, key, greater=True):
        results = []
        self._search_range(self.root, key, results, greater)
        return results

    def _search_range(self, node, key, results, greater):
        if node.leaf:
            for k, v in node.keys:
                if (greater and k > key) or (not greater and k < key):
                    results.append((k, v))
        else:
            for child in node.children:
                self._search_range(child, key, results, greater)

    def delete(self, key):
        self.root.delete(key)
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0]

    class BPlusTreeNode:
        def __init__(self, order):
            self.order = order
            self.keys = []
            self.children = []
            self.leaf = True

        def insert(self, key, value):
            if self.leaf:
                self.insert_leaf(key, value)
            else:
                self.insert_internal(key, value)

        def insert_leaf(self, key, value):
            self.keys.append((key, value))
            self.keys.sort(key=lambda x: x[0])
            if len(self.keys) >= self.order:
                return self.split()
            return None

        def insert_internal(self, key, value):
            child_index = self.find_child_index(key)
            split_node = self.children[child_index].insert(key, value)
            if split_node:
                self.keys.insert(child_index, split_node.keys[0])
                self.children[child_index] = split_node.children[0]
                self.children.insert(child_index + 1, split_node.children[1])
                if len(self.keys) >= self.order:
                    return self.split()
            return None

        def find_child_index(self, key):
            for i, item in enumerate(self.keys):
                if key < item[0]:
                    return i
            return len(self.keys)

        def split(self):
            mid_index = len(self.keys) // 2
            mid_key = self.keys[mid_index]

            left_child = BPlusTree.BPlusTreeNode(self.order)
            left_child.keys = self.keys[:mid_index]
            left_child.children = self.children[:mid_index + 1]
            left_child.leaf = self.leaf

            right_child = BPlusTree.BPlusTreeNode(self.order)
            right_child.keys = self.keys[mid_index + 1:]
            right_child.children = self.children[mid_index + 1:]
            right_child.leaf = self.leaf

            new_root = BPlusTree.BPlusTreeNode(self.order)
            new_root.keys = [mid_key]
            new_root.children = [left_child, right_child]
            new_root.leaf = False

            if self.leaf:
                new_root.leaf = False
                left_child.leaf = right_child.leaf = True

            return new_root

        def delete(self, key):
            if self.leaf:
                self.delete_leaf(key)
            else:
                self.delete_internal(key)

        def delete_leaf(self, key):
            for i, (k, v) in enumerate(self.keys):
                if k == key:
                    del self.keys[i]
                    return

        def delete_internal(self, key):
            child_index = self.find_child_index(key)
            self.children[child_index].delete(key)
            if len(self.children[child_index].keys) < self.order // 2:
                self.merge_child(child_index)

        def merge_child(self, child_index):
            if child_index == 0:
                right_child = self.children[1]
                left_child = self.children[0]
            else:
                right_child = self.children[child_index]
                left_child = self.children[child_index - 1]

            left_child.keys.extend(right_child.keys)
            left_child.children.extend(right_child.children)
            self.keys.pop(child_index - 1)
            self.children.pop(child_index)

            if not left_child.leaf:
                left_child.leaf = False
