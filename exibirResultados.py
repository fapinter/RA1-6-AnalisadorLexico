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

# funcao responsavel por mostrar os resultados finais na tela
def exibirResultados(resultados):
    # imprime o titulo da secao de resultados
    print("\nResultados:")
    # percorre as chaves do dicionario em ordem crescente de linha
    for linha in sorted(resultados):
        # imprime o numero da linha e o resultado formatado com 1 casa decimal
        print(f"Linha {linha}: {resultados[linha]:.1f}")


# funcao principal do programa
def main():
    # verifica se foi passado pelo menos um argumento alem do nome do arquivo python
    if len(sys.argv) < 2:
        # mostra mensagem de erro caso o nome do arquivo de teste nao tenha sido informado
        print("Passe o nome do arquivo de teste")
        # encerra a funcao principal
        return

    # pega o nome do arquivo passado por parametro na linha de comando
    nome_arquivo = sys.argv[1]

    # cria uma lista vazia que sera preenchida com as linhas do arquivo
    linhas = []
    # chama a funcao que le o arquivo; se falhar, encerra o programa
    if not lerArquivo(nome_arquivo, linhas):
        return

    # dicionario que guarda os resultados numericos das expressoes executadas
    resultados = {}
    # dicionario que guarda os valores salvos em memoria, como MEM, VAR, X
    memoria = {}
    # guarda os tokens da ultima linha valida processada
    ultimo_token_valido = []
    # lista com os numeros das linhas que falharam no parse
    linhas_invalidas = []
    # dicionario com os erros de execucao, usando a linha como chave
    erros_execucao = {}
    # lista com os tokens de todas as linhas validas, usada para gerar assembly no final
    tokens_por_linha = []
    # contador de quantas linhas foram executadas sem erro
    linhas_executadas = 0

    # percorre todas as linhas lidas do arquivo, com numeracao começando em 1
    for numero_linha, linha in enumerate(linhas, start=1):
        # remove espacos e quebras de linha extras do inicio e do fim
        linha = linha.strip()

        # se a linha estiver vazia, pula para a proxima
        if linha == "":
            continue

        # chama o parser para validar a linha e obter os tokens
        valido, tokens = parseExpressao(linha, numero_linha)

        # se a linha nao for valida no parse
        if not valido:
            # registra o numero da linha na lista de linhas invalidas
            linhas_invalidas.append(numero_linha)
            # mostra mensagem informando que a linha falhou no parse
            print(f"Linha {numero_linha} invalida no parse.")
            # vai para a proxima linha do arquivo
            continue

        # guarda os tokens da ultima linha valida encontrada
        ultimo_token_valido = tokens
        # adiciona os tokens dessa linha na lista geral para gerar assembly depois
        tokens_por_linha.append(tokens)

        # tenta executar a expressao dessa linha
        try:
            # chama a funcao que executa a expressao e atualiza resultados/memoria
            executarExpressao(tokens, resultados, memoria, numero_linha)
            # se executou sem erro, soma 1 no contador de linhas executadas
            linhas_executadas += 1

        # captura qualquer erro que acontecer durante a execucao
        except Exception as e:
            # salva a mensagem de erro associada ao numero da linha
            erros_execucao[numero_linha] = str(e)
            # mostra a mensagem de erro na tela
            print(f"Erro na execucao da linha {numero_linha}: {e}")

    # chama a funcao que exibe os resultados finais
    exibirResultados(resultados)

    # verifica se houve alguma linha invalida no parse
    if len(linhas_invalidas) > 0:
        # imprime o titulo da secao de erros de parse
        print("\nLinhas invalidas no parse:")
        # percorre todas as linhas invalidas
        for linha in linhas_invalidas:
            # imprime o numero da linha invalida
            print(f"Linha {linha}")

    # verifica se houve algum erro de execucao
    if len(erros_execucao) > 0:
        # imprime o titulo da secao de erros de execucao
        print("\nLinhas com erro de execucao:")
        # percorre os erros em ordem de numero da linha
        for linha in sorted(erros_execucao):
            # imprime a linha e a mensagem de erro correspondente
            print(f"Linha {linha}: {erros_execucao[linha]}")

    # imprime o titulo da secao de resumo final
    print("\nResumo:")
    # mostra quantas linhas executaram com sucesso
    print(f"Linhas executadas com sucesso: {linhas_executadas}")
    # mostra quantas linhas geraram resultado exibivel
    print(f"Linhas com resultado exibido: {len(resultados)}")
    # mostra quantas linhas falharam no parse
    print(f"Linhas invalidas no parse: {len(linhas_invalidas)}")
    # mostra quantas linhas tiveram erro de execucao
    print(f"Linhas com erro de execucao: {len(erros_execucao)}")

    # abre/cria o arquivo que guarda os tokens da ultima execucao valida
    with open("tokens_ultima_execucao.txt", "w", encoding="utf-8") as arquivo_tokens:
        # escreve os tokens separados por espaco no arquivo
        arquivo_tokens.write(" ".join(ultimo_token_valido))

    # verifica se existe pelo menos uma linha valida para gerar assembly
    if len(tokens_por_linha) > 0:
        # gera o codigo assembly a partir dos tokens validos
        assembly = gerarAssembly(tokens_por_linha)

        # abre/cria o arquivo de saida do assembly
        with open("programa.s", "w", encoding="utf-8") as arquivo_asm:
            # escreve todo o codigo assembly no arquivo
            arquivo_asm.write(assembly)


if __name__ == "__main__":
    main()