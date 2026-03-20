def read_file(arquivo_teste):
    linhas = []

    try:
        with open(arquivo_teste, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha != "":
                    linhas.append(linha)
    except FileNotFoundError:
        print(f"Erro: arquivo '{arquivo_teste}' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao abrir o arquivo: {e}")
        return None

    return linhas

linhas = read_file("arquivo_teste.txt")
print(linhas)