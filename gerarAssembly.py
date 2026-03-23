from parseExpressao import parseExpressao

#le o arquivo do parseExpressao
def read_file(file_name, lines):
    lines.clear()
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    lines.append(line)
        return True
    except FileNotFoundError:
        print(f"Erro ao abrir arquivo: '{file_name}' nao foi encontrado.")
        return False

#separa os tokens válidos gerados do parseExpressao
def groupTokens(tokens, index=0, must_close=False):
    group = []

    while index < len(tokens):
        token = tokens[index]

        if token == "(":
            nested_group, index = groupTokens(tokens, index + 1, True)
            group.append(nested_group)
            continue

        if token == ")":
            if not must_close:
                raise ValueError("Fechamento de parenteses sem abertura.")
            return group, index + 1

        group.append(token)
        index += 1

    if must_close:
        raise ValueError("Parenteses nao fechados.")

    return group, index

#Verifica se o token gerado é um número
def is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False

#Faz conferência de número ou operador para guardar as informações na variável
def emitAssembly(item, assembly_lines):
    if isinstance(item, list):
        if len(item) == 1 and item[0].isupper() and item[0] != "MEM":
            memory_name = item[0]
            assembly_lines.append(f"ldr r0, ={memory_name}")
            assembly_lines.append("vldr d0, [r0]")
            assembly_lines.append("bl push_d0")
            return

        if len(item) == 2 and item[1] == "MEM":
            emitAssembly(item[0], assembly_lines)
            assembly_lines.append("bl pop_to_d0")
            assembly_lines.append("bl res_lookup")
            assembly_lines.append("bl push_d0")
            return

        if len(item) == 2 and item[1].isupper() and item[1] != "MEM":
            memory_name = item[1]
            emitAssembly(item[0], assembly_lines)
            assembly_lines.append("bl pop_to_d0")
            assembly_lines.append(f"ldr r0, ={memory_name}")
            assembly_lines.append("vstr d0, [r0]")
            assembly_lines.append("bl push_d0")
            return

        for subitem in item:
            emitAssembly(subitem, assembly_lines)
        return

    if is_number(item):
        assembly_lines.append(f"ldr r0, ={item}")
        assembly_lines.append("vldr d0, [r0]")
        assembly_lines.append("bl push_d0")
        return

    if item == "+":
        assembly_lines.append("bl pop_to_d0")
        assembly_lines.append("bl pop_to_d1")
        assembly_lines.append("vadd.f64 d0, d1, d0")
        assembly_lines.append("bl push_d0")
        return

    if item == "-":
        assembly_lines.append("bl pop_to_d0")
        assembly_lines.append("bl pop_to_d1")
        assembly_lines.append("vsub.f64 d0, d1, d0")
        assembly_lines.append("bl push_d0")
        return

    if item == "*":
        assembly_lines.append("bl pop_to_d0")
        assembly_lines.append("bl pop_to_d1")
        assembly_lines.append("vmul.f64 d0, d1, d0")
        assembly_lines.append("bl push_d0")
        return

    if item == "/":
        assembly_lines.append("bl pop_to_d0")
        assembly_lines.append("bl pop_to_d1")
        assembly_lines.append("vdiv.f64 d0, d1, d0")
        assembly_lines.append("bl push_d0")
        return

    if item == "//":
        assembly_lines.append("bl pop_to_d0")
        assembly_lines.append("bl pop_to_d1")
        assembly_lines.append("bl op_int_div")
        assembly_lines.append("bl push_d0")
        return

    if item == "%":
        assembly_lines.append("bl pop_to_d0")
        assembly_lines.append("bl pop_to_d1")
        assembly_lines.append("bl op_int_mod")
        assembly_lines.append("bl push_d0")
        return

    if item == "^":
        assembly_lines.append("bl pop_to_d0")
        assembly_lines.append("bl pop_to_d1")
        assembly_lines.append("bl op_pow")
        assembly_lines.append("bl push_d0")
        return



#Função para gerar o arquivo em assembly
def gerarAssembly(tokens):
    grouped_tokens, final_index = groupTokens(tokens)

    if final_index != len(tokens):
        raise ValueError("Nem todos os tokens foram consumidos.")

    assembly_lines = []

    for item in grouped_tokens:
        emitAssembly(item, assembly_lines)

    return "\n".join(assembly_lines)


if __name__ == "__main__":
    tests = [
    "(3.14 2.0 +)",
    "((1.5 2.0 *) (3.0 4.0 *) /)",
    "(5.0 MEM)",
    "(MEM)",
    "(2 RES)",
    "(10 3 //)",
    "(10 3 %)",
    "(2 4 ^)"
]


    for i, line in enumerate(tests, start=1):
        valid, tokens = parseExpressao(line, i)
        print(f"\nLinha: {line}")
        print("Valida:", valid)
        print("Tokens:", tokens)

        if valid:
            assembly = gerarAssembly(tokens)
            print(assembly)
