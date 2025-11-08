class ExtensibleHash:
    def __init__(self, bucket_size: int):
        """Inicializa a tabela hash com o tamanho máximo de registros por bucket."""
        pass

    def insert(self, key: int, value: any):
        """Insere um par (chave, valor) na estrutura."""
        pass

    def search(self, key: int) -> any:
        """Retorna o valor associado à chave, se existir."""
        pass

    def remove(self, key: int) -> bool:
        """Remove o registro com a chave informada."""
        pass

    def display(self):
        """Exibe o diretório e os buckets da tabela hash."""
        pass