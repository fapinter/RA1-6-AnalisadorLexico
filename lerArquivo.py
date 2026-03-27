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