class Node:
    """Representa um nó da árvore ISA."""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class ISATree:
    """Implementação simples de uma árvore ISA (índice secundário agrupado)."""

    def __init__(self):
        self.root = None

    def insert(self, key, value):
        """Insere um par chave-valor na árvore."""
        if self.root is None:
            self.root = Node(key, value)
        else:
            self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if key == node.key:
            node.value = value  # Atualiza valor se a chave já existir
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
        """Busca um valor pela chave."""
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
        """Remove uma chave da árvore."""
        self.root = self._remove(self.root, key)

    def _remove(self, node, key):
        if not node:
            return None
        if key < node.key:
            node.left = self._remove(node.left, key)
        elif key > node.key:
            node.right = self._remove(node.right, key)
        else:
            # Caso 1: nó sem filhos
            if not node.left and not node.right:
                return None
            # Caso 2: um filho
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            # Caso 3: dois filhos — substitui pelo menor da subárvore direita
            min_larger_node = self._min_value_node(node.right)
            node.key, node.value = min_larger_node.key, min_larger_node.value
            node.right = self._remove(node.right, min_larger_node.key)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def display(self):
        """Mostra a árvore (ordem simétrica)."""
        if self.root is None:
            print("Árvore vazia.")
            return
        print("\nÁrvore ISA (em ordem):")
        self._inorder(self.root)
        print("\n")

    def _inorder(self, node):
        if node:
            self._inorder(node.left)
            print(f"{node.key}: {node.value}", end=" | ")
            self._inorder(node.right)


# ========== MENU INTERATIVO ==========
def menu():
    isa = ISATree()

    while True:
        print("\n===== MENU - ARVORE ISA =====")
        print("1. Inserir chave e valor")
        print("2. Buscar chave")
        print("3. Remover chave")
        print("4. Exibir arvore (em ordem)")
        print("5. Sair")

        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            try:
                chave = int(input("Digite a chave (inteiro): "))
                valor = input("Digite o valor: ")
                isa.insert(chave, valor)
                print(f"Inserido: {chave} → {valor}")
            except ValueError:
                print("A chave deve ser um número inteiro.")

        elif opcao == "2":
            try:
                chave = int(input("Digite a chave a buscar: "))
                resultado = isa.search(chave)
                if resultado:
                    print(f"Valor encontrado: {resultado}")
                else:
                    print("Chave não encontrada.")
            except ValueError:
                print("A chave deve ser um número inteiro.")

        elif opcao == "3":
            try:
                chave = int(input("Digite a chave a remover: "))
                isa.remove(chave)
                print(f"Chave {chave} removida (se existia).")
            except ValueError:
                print("A chave deve ser um número inteiro.")

        elif opcao == "4":
            isa.display()

        elif opcao == "5":
            print("Encerrando o programa...")
            break

        else:
            print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    menu()
