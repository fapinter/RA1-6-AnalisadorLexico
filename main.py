"""
Grupo: RA1-6
Alunos:
    Fabricio Goes Pinterich : @fapinter
    Leonardo Min Woo Chung: @LeonardoChung
    Phillip Wan Tcha Yan: @PhillipYan
"""

import sys
from parseExpressao import parseExpressao
from executarExpressao import executarExpressao


def exibirResultados(resultados):
    print("\nResultados:")
    for linha in sorted(resultados):
        print(f"Linha {linha}: {resultados[linha]:.1f}")

def main():
    if len(sys.argv) < 2:
        print("Passe o nome do arquivo de teste.")
        return

    nome_arquivo = sys.argv[1]

    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
    except FileNotFoundError:
        print("Arquivo nao encontrado.")
        return

    resultados = {}
    memoria = {}
    ultimo_token_valido = []
    linhas_invalidas = []
    erros_execucao = {}

    for numero_linha, linha in enumerate(linhas, start=1):
        linha = linha.strip()

        if linha == "":
            continue

        valido, tokens = parseExpressao(linha, numero_linha)

        if not valido:
            linhas_invalidas.append(numero_linha)
            print(f"Linha {numero_linha} invalida no parse.")
            continue

        ultimo_token_valido = tokens

        try:
            executarExpressao(tokens, resultados, memoria, numero_linha)

            # assembly entra aqui

        except Exception as e:
            erros_execucao[numero_linha] = str(e)
            print(f"Erro na execucao da linha {numero_linha}: {e}")

    exibirResultados(resultados)

    if len(linhas_invalidas) > 0:
        print("\nLinhas invalidas no parse:")
        for linha in linhas_invalidas:
            print(f"Linha {linha}")

    if len(erros_execucao) > 0:
        print("\nLinhas com erro de execucao:")
        for linha in sorted(erros_execucao):
            print(f"Linha {linha}: {erros_execucao[linha]}")

    print(f"Linhas executadas com sucesso: {len(resultados)}")
    print(f"Linhas invalidas no parse: {len(linhas_invalidas)}")
    print(f"Linhas com erro de execucao: {len(erros_execucao)}")

    with open("tokens_ultima_execucao.txt", "w", encoding="utf-8") as arquivo_tokens:
        arquivo_tokens.write(" ".join(ultimo_token_valido))

if __name__ == "__main__":
    main()