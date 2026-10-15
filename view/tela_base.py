from builtins import ValueError, int, list, print, str
from fileinput import input
import os


class TelaBase:
    def mostrar_titulo(self, titulo: str):
        print("\n" + "=" * 40)
        print(f"{titulo.center(40)}")
        print("=" * 40)

    def mostrar_mensagem(self, mensagem: str):
        print(f"\n[INFO] {mensagem}")

    def mostrar_erro(self, erro: str):
        print(f"\n[ERRO] {erro}")

    def selecionar_opcao(self, opcoes_validas: list) -> int:
        while True:
            try:
                opcao = int(input("\nEscolha uma opção: "))
                if opcao in opcoes_validas:
                    return opcao
                print(f"Opção inválida! Escolha entre {opcoes_validas}.")
            except ValueError:
                print("Entrada inválida! Digite apenas números inteiros.")