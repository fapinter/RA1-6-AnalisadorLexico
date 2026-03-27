# lê o arquivo das expressões
def lerArquivo(file_name, lines):
    # Limpa a lista antes de reutilizar
    lines.clear()

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:

                # tira espacos e quebra de linha
                line = line.strip()

                # so adiciona se a linha nao estiver vazia
                if line:
                    lines.append(line)
        return True

    except FileNotFoundError:
        print(f"Erro ao abrir arquivo: '{file_name}' nao foi encontrado.")
        return False

if __name__ == "__main__":
    test_files = [
        'arquivo_teste.txt',
        'arquivo_que_nao_existe.txt'
    ]
    for file in test_files:
        linhas = []
        arquivo_aberto = lerArquivo(file_name=file, lines=linhas)
        print(f'Arquivo {file} Existente? {arquivo_aberto}')
        for l in linhas:
            print(l)