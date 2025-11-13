import math

# Node class representing each node in the B+ tree
# Here, we define the Node structure
# order: maximum number of keys in a node
# leaf: boolean indicating if the node is a leaf
# keys: list of keys in the node
# values: list of values (only for leaf nodes)
# children: list of child nodes (only for internal nodes)
class Node:
    def __init__(self, order):
        self.order = order
        self.leaf = True
        self.keys = []
        self.values = []
        self.children = []
        self.next = None

# all the methods of BPlusTree class
# The methods use an interative approach to avoid recursion depth issues
# The BPlusTree supports insertion and search operations
class BPlusTree:
    def __init__(self, order: int):
        self.root = Node(order)

    def search(self, key: int):
        current = self.root
        while not current.leaf:
            i = 0
            while i < len(current.keys) and key >= current.keys[i]:
                i += 1
            current = current.children[i]

        for i, k in enumerate(current.keys):
            if k == key:
                return current.values[i]
        return None

    def insert(self, key: int, value: any):
        root = self.root

        if len(root.keys) == 0:
            root.keys.append(key)
            root.values.append([value])
            return

        parent_stack = []
        current = root
        while not current.leaf:
            parent_stack.append(current)
            i = 0
            while i < len(current.keys) and key >= current.keys[i]:
                i += 1
            current = current.children[i]

        i = 0
        while i < len(current.keys) and key > current.keys[i]:
            i += 1
        if i < len(current.keys) and current.keys[i] == key:
            current.values[i].append(value)
        else:
            current.keys.insert(i, key)
            current.values.insert(i, [value])

        if len(current.keys) > current.order:
            self._split_leaf(current, parent_stack)

    def _split_leaf(self, leaf, parent_stack):
        mid = math.ceil(leaf.order / 2)
        new_leaf = Node(leaf.order)
        new_leaf.leaf = True

        new_leaf.keys = leaf.keys[mid:]
        new_leaf.values = leaf.values[mid:]
        leaf.keys = leaf.keys[:mid]
        leaf.values = leaf.values[:mid]

        new_leaf.next = leaf.next
        leaf.next = new_leaf

        promoted_key = new_leaf.keys[0]

        if not parent_stack:
            new_root = Node(leaf.order)
            new_root.leaf = False
            new_root.keys = [promoted_key]
            new_root.children = [leaf, new_leaf]
            self.root = new_root
            return

        parent = parent_stack.pop()
        self._insert_in_parent(parent, new_leaf, promoted_key, parent_stack)

    def _insert_in_parent(self, parent, new_child, key, parent_stack):
        i = 0
        while i < len(parent.keys) and key > parent.keys[i]:
            i += 1

        parent.keys.insert(i, key)
        parent.children.insert(i + 1, new_child)

        if len(parent.keys) > parent.order:
            self._split_internal(parent, parent_stack)

    def _split_internal(self, node, parent_stack):
        mid = math.ceil(node.order / 2)
        new_node = Node(node.order)
        new_node.leaf = False

        promoted_key = node.keys[mid]
        new_node.keys = node.keys[mid + 1:]
        new_node.children = node.children[mid + 1:]

        node.keys = node.keys[:mid]
        node.children = node.children[:mid + 1]

        if not parent_stack:
            new_root = Node(node.order)
            new_root.leaf = False
            new_root.keys = [promoted_key]
            new_root.children = [node, new_node]
            self.root = new_root
            return

        parent = parent_stack.pop()
        self._insert_in_parent(parent, new_node, promoted_key, parent_stack)

    def remove(self, key: int):
        current = self.root
        parent_stack = []

        while not current.leaf:
            parent_stack.append(current)
            i = 0
            while i < len(current.keys) and key >= current.keys[i]:
                i += 1
            current = current.children[i]

        if key not in current.keys:
            return False

        index = current.keys.index(key)
        current.keys.pop(index)
        current.values.pop(index)
        if parent_stack:
            parent = parent_stack[-1]
            child_index = parent.children.index(current)
            if child_index > 0 and len(current.keys) > 0:
                parent.keys[child_index - 1] = current.keys[0]

        if current == self.root:
            if not current.leaf and len(current.children) > 0:
                self.root = current.children[0]
            return True

        min_keys = math.ceil(current.order / 2) - 1
        if len(current.keys) < min_keys:
            self._rebalance(current, parent_stack)

        return True

    def _rebalance(self, node, parent_stack):
        if not parent_stack:
            return

        parent = parent_stack.pop()
        index = parent.children.index(node)

        left_sibling = parent.children[index - 1] if index > 0 else None
        right_sibling = parent.children[index + 1] if index + 1 < len(parent.children) else None

        min_keys = math.ceil(node.order / 2) - 1

        if left_sibling and len(left_sibling.keys) > min_keys:
            borrowed_key = left_sibling.keys.pop(-1)
            borrowed_value = left_sibling.values.pop(-1)
            node.keys.insert(0, borrowed_key)
            node.values.insert(0, borrowed_value)
            parent.keys[index - 1] = node.keys[0]
            return

        if right_sibling and len(right_sibling.keys) > min_keys:
            borrowed_key = right_sibling.keys.pop(0)
            borrowed_value = right_sibling.values.pop(0)
            node.keys.append(borrowed_key)
            node.values.append(borrowed_value)
            parent.keys[index] = right_sibling.keys[0]
            return

        if left_sibling:
            left_sibling.keys.extend(node.keys)
            left_sibling.values.extend(node.values)
            left_sibling.next = node.next
            parent.children.pop(index)
            parent.keys.pop(index - 1)
            if index - 1 > 0:
                parent.keys[index - 2] = left_sibling.keys[0]
        elif right_sibling:
            node.keys.extend(right_sibling.keys)
            node.values.extend(right_sibling.values)
            node.next = right_sibling.next
            parent.children.pop(index + 1)
            parent.keys.pop(index)
            if index > 0:
                parent.keys[index - 1] = node.keys[0]

        min_parent_keys = 1 if parent == self.root else math.ceil(parent.order / 2) - 1
        if len(parent.keys) < min_parent_keys:
            self._rebalance(parent, parent_stack)

    def display(self):
        nodes = [self.root]
        level = 0
        while nodes:
            print(f"Level {level}: ", end="")
            next_nodes = []
            for n in nodes:
                print(n.keys, end=" | ")
                if not n.leaf:
                    next_nodes.extend(n.children)
            print()
            nodes = next_nodes
            level += 1


def main():
    tree = BPlusTree(order=4)

    while True:
        print("\n===== B+ TREE TERMINAL =====")
        print("1 - Inserir")
        print("2 - Buscar")
        print("3 - Remover")
        print("4 - Mostrar árvore")
        print("5 - Sair")

        op = input("Escolha: ")

        if op == "1":
            key = int(input("Chave: "))
            value = input("Valor: ")
            tree.insert(key, value)
            print("Inserido.\n")

        elif op == "2":
            key = int(input("Chave: "))
            res = tree.search(key)
            print("Resultado:", res)

        elif op == "3":
            key = int(input("Chave: "))
            ok = tree.remove(key)
            print("Removido." if ok else "Chave não encontrada.")

        elif op == "4":
            print("\nÁrvore:")
            tree.display()

        elif op == "5":
            print("Encerrando...")
            break

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()