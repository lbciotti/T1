from datetime import date
from models.pagamento import Pagamento


class PagamentoCartao(Pagamento):
    def __init__(self, data: date, valor_pago: float, numero_cartao: str, bandeira: str):
        super().__init__(data, valor_pago)
        self.__numero_cartao = numero_cartao
        self.__bandeira = bandeira

    @property
    def numero_cartao(self) -> str:
        return self.__numero_cartao

    @numero_cartao.setter
    def numero_cartao(self, numero_cartao: str):
        self.__numero_cartao = numero_cartao

    @property
    def bandeira(self) -> str:
        return self.__bandeira

    @bandeira.setter
    def bandeira(self, bandeira: str):
        self.__bandeira = bandeira
        