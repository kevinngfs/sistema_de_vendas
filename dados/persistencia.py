#Biblioteca do python para serialização e deserialização
import pickle
#Módulo nativo de python que permite interagir com o sistema operacional
import os

class PersistenciaDados:
    """
    Classe para persistência de dados(salvar dados)
    Métodos:
    __init__: Inicializa, recebe o nome do arquivo do banco de dados, automaticamente definido como dados_sistema.dat
    salvar: Método que permite salvar qualquer informação, recebe o dado que será salvo
    carregar: Método que permite carregar dados previamente salvos
    """
    def __init__(self, arquivo_banco="dados_sistema.dat"):
        self.arquivo_banco = arquivo_banco

    def salvar(self, dados):
        """Salva qualquer informação (lista de vendas, produtos, etc) no arquivo."""
        try:
            with open(self.arquivo_banco, 'wb') as f:
                pickle.dump(dados, f)
            return True, "Dados salvos com sucesso!"
        except Exception as e:
            return False, f"Erro ao salvar: {e}"

    def carregar(self):
        """Carrega os dados salvos. Retorna a estrutura inicial se for a primeira vez."""
        if not os.path.exists(self.arquivo_banco):
            return {"estoque": [], "vendas": []}

        try:
            with open(self.arquivo_banco, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Erro ao carregar banco de dados: {e}")
            return {"estoque": [], "vendas": []}
