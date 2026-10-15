from abc import ABC
from builtins import ValueError, dict, float, int, list, print, str
from fileinput import input



class TelaBase(ABC):
    def mostrar_titulo(self, titulo: str):
        print("\n" + "=" * 50)
        print(f"{titulo.center(50)}")
        print("=" * 50)

    def mostrar_mensagem(self, mensagem: str):
        print(f"\n[SUCESSO] {mensagem}")

    def mostrar_erro(self, erro: str):
        print(f"\n[ERRO] {erro}")

    def selecionar_opcao(self, opcoes_validas: list) -> int:
        while True:
            try:
                opcao = int(input("\nEscolha uma opção: "))
                if opcao in opcoes_validas:
                    return opcao
                print(f"Opção inválida! Escolha uma opção entre {opcoes_validas}.")
            except ValueError:
                print("Entrada inválida! Digite apenas números inteiros.")

    def ler_float(self, mensagem: str) -> float:
        while True:
            try:
                valor = float(input(mensagem).replace(",", "."))
                if valor >= 0:
                    return valor
                print("O valor não pode ser negativo!")
            except ValueError:
                print("Entrada inválida! Digite um número válido.")