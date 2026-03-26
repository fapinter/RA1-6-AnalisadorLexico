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
from gerarAssembly import lerArquivo, gerarAssembly


def exibirResultados(resultados):
    print("\nResultados:")
    for linha in sorted(resultados):
        print(f"Linha {linha}: {resultados[linha]:.1f}")

def main():
    if len(sys.argv) < 2:
        print("Passe o nome do arquivo de teste")
        return

    nome_arquivo = sys.argv[1]

    linhas = []
    if not lerArquivo(nome_arquivo, linhas):
        return

    resultados = {}
    memoria = {}
    ultimo_token_valido = []
    linhas_invalidas = []
    erros_execucao = {}
    tokens_por_linha = []
    linhas_executadas = 0

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
        tokens_por_linha.append(tokens)

        try:
            executarExpressao(tokens, resultados, memoria, numero_linha)
            linhas_executadas += 1

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

    print("\nResumo:")
    print(f"Linhas executadas com sucesso: {linhas_executadas}")
    print(f"Linhas com resultado exibido: {len(resultados)}")
    print(f"Linhas invalidas no parse: {len(linhas_invalidas)}")
    print(f"Linhas com erro de execucao: {len(erros_execucao)}")

    with open("tokens_ultima_execucao.txt", "w", encoding="utf-8") as arquivo_tokens:
        arquivo_tokens.write(" ".join(ultimo_token_valido))

    if len(tokens_por_linha) > 0:
        assembly = gerarAssembly(tokens_por_linha)

        with open("programa.s", "w", encoding="utf-8") as arquivo_asm:
            arquivo_asm.write(assembly)


if __name__ == "__main__":
    main()