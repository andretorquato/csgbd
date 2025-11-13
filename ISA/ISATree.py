class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class ISATree:

    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
        else:
            self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if key == node.key:
            node.value = value
        elif key < node.key:
            if node.left:
                self._insert(node.left, key, value)
            else:
                node.left = Node(key, value)
        else:
            if node.right:
                self._insert(node.right, key, value)
            else:
                node.right = Node(key, value)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node:
            return None
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def remove(self, key):
        self.root = self._remove(self.root, key)

    def _remove(self, node, key):
        if not node:
            return None
        if key < node.key:
            node.left = self._remove(node.left, key)
        elif key > node.key:
            node.right = self._remove(node.right, key)
        else:
            if not node.left and not node.right:
                return None
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            min_larger_node = self._min_value_node(node.right)

            print (min_larger_node.key)

            node.key, node.value = min_larger_node.key, min_larger_node.value
            node.right = self._remove(node.right, min_larger_node.key)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def display(self):
        print("Arvore ISA (em ordem):")
        self._inorder(self.root)
        print()

    def _inorder(self, node):
        if node:
            self._inorder(node.left)
            print(f"{node.key}: {node.value}", end=" | ")
            self._inorder(node.right)


if __name__ == "__main__":
    isa = ISATree()
    #isa.insert(40, "Filme A")
    #isa.insert(60, "Filme C")
    #isa.insert(10, "Filme D")
    #isa.insert(30, "Filme E")
    isa.insert(1, "Filme A")
    isa.insert(2, "Filme B")
    isa.insert(3, "Filme C")

    isa.display()

    print("\nBusca pela chave 20:", isa.search(20))
    print("Busca pela chave 99:", isa.search(99))

    print("\nRemovendo a chave 20...")
    isa.remove(2)
    isa.display()

    isa.insert(2, "Filme B")

    isa.display()
