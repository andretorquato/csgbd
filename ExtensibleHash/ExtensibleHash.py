class ExtensibleHash:
    def __init__(self, bucket_size: int):
        """Inicializa a tabela hash com o tamanho máximo de registros por bucket."""
        # profundidade global
        self.bucket_size = bucket_size
        self.global_depth = 1

        # lista de buckets 
        self.buckets = []

        # iniciar 2 buckets
        for _ in range(2): 
            self.buckets.append({
                "local_depth": 1,
                "items": []
            })

        # diretório inicial apontando para os dois buckets
        self.directory = [0, 1]  

        def _hash(self, key: int) -> int:
            """hash simples(retornando propria chave)"""
            return key
        
        def _get_directory_index(self, key: int) -> int:
            h = self._hash(key)
            mask = (1 << self.global_depth) - 1
            return h & mask
        
        def _split_bucket(self, bucket_id: int): 
            """Divide o bucket quando ele estiver cheio e aumentar a profundidade local"""
            old_bucket = self.buckets[bucket_id]
            old_local_depth = old_bucket["local_depth"]

            print(f"\n dividindo bucket {bucket_id} profundidade local {old_local_depth}")

            old_bucket["local_depth"] += 1

            if old_bucket["local_depth"] > self.global_depth: 
                print("aumentando profundidade global")
                self.global_depth += 1

                self.directory = self.directory * 2

                print(f"nova profundidade global: {self.global_depth}")

            new_bucket_id = len(self.buckets)
            new_bucket = {
                "local_depth": old_bucket["local_depth"],
                "items": []
            }
            self.buckets.append(new_bucket)
            
            diff_bit = 1 << (old_bucket["local_depth"] - 1)

            # realocar entradas do diretório
            for i in range(len(self.directory)): 
                if self.directory[i] == bucket_id:
                    if i & diff_bit:
                        self.directory[1] = new_bucket_id

            # redistribuir os itens do bucket antigo
            old_items = old_bucket["items"]
            old_bucket["items"] = []
            for (k, v) in old_items:
                dir_index = self._get_directory_index(k)
                b_id = self.directory[dir_index]
                self.buckets[b_id]["items"].append((k, v))


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