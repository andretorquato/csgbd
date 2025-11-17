class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.items = []  # valores inseridos neste nó

    def add_child(self, child_node):
        self.children.append(child_node)


class ISATree:
    def __init__(self):
        # ---------- Criando a ISA Tree Estática ----------
        self.root = Node(0)

        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)
        node4 = Node(4)
        node5 = Node(5)
        node6 = Node(6)

        # estrutura:
        # 0 -> {1, 2}
        # 1 -> {3, 4}
        # 2 -> {5, 6}

        self.root.add_child(node1)
        self.root.add_child(node2)

        node1.add_child(node3)
        node1.add_child(node4)

        node2.add_child(node5)
        node2.add_child(node6)

        # Dicionário para acesso rápido
        self.map = {
            0: self.root,
            1: node1,
            2: node2,
            3: node3,
            4: node4,
            5: node5,
            6: node6,
        }

    # --------------------- OPERAÇÕES ------------------------

    def insert(self, node_value, item):
        if node_value not in self.map:
            print("Tipo inexistente na ISA Tree.")
            return

        self.map[node_value].items.append(item)
        print(f"Inserido {item} no tipo {node_value}")

    def search(self, item):
        for node_value, node in self.map.items():
            if item in node.items:
                print(f"Encontrado: valor {item} está no tipo {node_value}")
                return True

        print("Valor não encontrado na árvore.")
        return False

    def remove(self, item):
        for node_value, node in self.map.items():
            if item in node.items:
                node.items.remove(item)
                print(f"Removido {item} do tipo {node_value}")
                return True

        print("Valor não encontrado para remoção.")
        return False

    def display(self):
        print("\n====== Estrutura da ISA Tree ======\n")
        self._display_pretty(self.root, "", True)
        print("\n===================================\n")

    def _display_pretty(self, node, prefix, is_last):
        # prefixo visual
        connector = "└── " if is_last else "├── "

        # imprime o nó
        print(prefix + connector + f"{node.value}  (itens: {node.items})")

        # prepara prefixo para filhos
        new_prefix = prefix + ("    " if is_last else "│   ")

        # imprime filhos
        count = len(node.children)
        for i, child in enumerate(node.children):
            last = (i == count - 1)
            self._display_pretty(child, new_prefix, last)



# ===================== MENU INTERATIVO ======================

def menu():
    tree = ISATree()

    while True:
        print("\n===== MENU ISA TREE =====")
        print("1 - Inserir valor em um tipo")
        print("2 - Buscar valor")
        print("3 - Remover valor")
        print("4 - Exibir árvore")
        print("0 - Sair")
        opc = input("Escolha: ")

        if opc == "1":
            tipo = int(input("Digite o tipo (0 a 6): "))
            valor = input("Digite o valor a inserir: ")
            tree.insert(tipo, valor)

        elif opc == "2":
            valor = input("Digite o valor a buscar: ")
            tree.search(valor)

        elif opc == "3":
            valor = input("Digite o valor a remover: ")
            tree.remove(valor)

        elif opc == "4":
            tree.display()

        elif opc == "0":
            print("Encerrando...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
