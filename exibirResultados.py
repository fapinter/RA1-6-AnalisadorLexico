"""
Grupo: RA1-6
Alunos:
    Fabricio Goes Pinterich : @fapinter
    Leonardo Min Woo Chung: @LeonardoChung
    Phillip Wan Tcha Yan: @PhillipYan
"""

# funcao responsavel por mostrar os resultados finais na tela
def exibirResultados(resultados):
    # imprime o titulo da secao de resultados
    print("\nResultados:")
    # percorre as chaves do dicionario em ordem crescente de linha
    for linha in sorted(resultados):
        # imprime o numero da linha e o resultado formatado com 1 casa decimal
        print(f"Linha {linha}: {resultados[linha]:.4f}")

if __name__ == "__main__":
    resultado_teste = {
        1: 1.24,
        2: 4.20,
        3: 67,
        4: 21
    }
    exibirResultados(resultados=resultado_teste)