from parseExpressao import parseExpressao
from lerArquivo import lerArquivo

# separa os tokens válidos gerados do parseExpressao e organiza em grupos conforme os parênteses
def groupTokens(tokens, index=0, must_close=False):

    # grupo atual de tokens
    group = []

    while index < len(tokens):
        token = tokens[index]

        # caso abra parenteses, cria um grupo interno
        if token == "(":
            nested_group, index = groupTokens(tokens, index + 1, True)
            group.append(nested_group)
            continue

        # caso feche parenteses, devolve o grupo montado
        if token == ")":
            if not must_close:
                raise ValueError("Fechamento de parenteses sem abertura.")
            return group, index + 1

        # adiciona o token no grupo
        group.append(token)
        index += 1

    if must_close:
        raise ValueError("Parenteses nao fechados.")

    return group, index


# verifica se o token gerado é um número
def is_number(token):
    try:    
        float(token)
        return True
    except ValueError:
        return False


# verifica o tipo do item (numero, operador, MEM, RES ou subexpressao) e gera o Assembly
def emitAssembly(item, assembly_lines, literal_labels, memory_labels):
    # caso seja uma lista, pode ser subexpressao ou comando especial (MEM, RES)
    if isinstance(item, list):
        # Caso (MEM): le o valor salvo em memoria
        if len(item) == 1 and item[0].isupper() and item[0] != "RES":
            memory_name = item[0]
            label = "label_" + memory_name

            # Guarda esse nome para depois declarar na .data
            memory_labels.add(label)

            assembly_lines.append(f"ldr r0, ={label}") # carrega o endereço do valor
            assembly_lines.append("vldr d0, [r0]") # le o double da memoria para d0
            assembly_lines.append("bl push_d0") # empilha o valor lido
            return

        # caso (N RES): busca um resultado anterior
        if len(item) == 2 and item[1] == "RES":
            emitAssembly(item[0], assembly_lines, literal_labels, memory_labels)
            assembly_lines.append("bl pop_to_d0") # recupera o numero no RES
            assembly_lines.append("bl res_lookup")  # busca o resultado anterior correspondente
            assembly_lines.append("bl push_d0") # empilha o resultado encontrado
            return

        # caso (valor MEM): grava um valor na memoria
        if len(item) == 2 and item[1].isupper() and item[1] != "RES":
            memory_name = item[1]
            label = "label_" + memory_name

            # guarda esse nome para declarar depois
            memory_labels.add(label)

            # gera o valor que vai ser salvo
            emitAssembly(item[0], assembly_lines, literal_labels, memory_labels)
            assembly_lines.append("bl pop_to_d0")
            assembly_lines.append(f"ldr r0, ={label}") # carrega o endereco da variavel
            assembly_lines.append("vstr d0, [r0]") # salva o valor na memoria
            assembly_lines.append("bl push_d0") # reempilha o valor para continuar a expressao
            return

        # se nao for caso especial percorre normalmente a subexpressao
        for subitem in item:
            emitAssembly(subitem, assembly_lines, literal_labels, memory_labels)
        return

    # se for numero cria o label e empilha o valor em d0
    if is_number(item):
        label = "label_" + item.replace(".", "_")

        # Guarda o literal para declarar depois na .data
        literal_labels[label] = item

        assembly_lines.append(f"ldr r0, ={label}")
        assembly_lines.append("vldr d0, [r0]")
        assembly_lines.append("bl push_d0")
        return

    # operações aritmeticas com os dois valores do topo da pilha
    # desempilha os dois operandos, faz a operação e empilha o resultado
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

     # divisao inteira
    if item == "//":
        assembly_lines.append("bl pop_to_d0")
        assembly_lines.append("bl pop_to_d1")
        assembly_lines.append("bl op_int_div")
        assembly_lines.append("bl push_d0")
        return

    # resto da divisao inteira
    if item == "%":
        assembly_lines.append("bl pop_to_d0")
        assembly_lines.append("bl pop_to_d1")
        assembly_lines.append("bl op_int_mod")
        assembly_lines.append("bl push_d0")
        return

    # potencia com expoente inteiro
    if item == "^":
        assembly_lines.append("bl pop_to_d0")
        assembly_lines.append("bl pop_to_d1")
        assembly_lines.append("bl op_pow")
        assembly_lines.append("bl push_d0")
        return


# gera o corpo da expressao
def gerarCorpoAssembly(tokens, literal_labels, memory_labels):
    grouped_tokens, final_index = groupTokens(tokens)

    # Se sobrou token sem usar, tem algo errado na expressao
    if final_index != len(tokens):
        raise ValueError("Nao foram utilizados todos os tokens.")

    assembly_lines = []

    # gera instruções para cada item da expressao
    for item in grouped_tokens:
        emitAssembly(item, assembly_lines, literal_labels, memory_labels)

    return assembly_lines



# junta todas as linhas do arquivo no mesmo programa para MEM e RES funcionarem
def gerarAssembly(tokens_por_linha):
    # dicionario para os numeros/literais usados no programa
    literal_labels = {}

    # conjunto para memória
    memory_labels = set()

    # codigo principal de todas as linhas
    program_lines = []

    for line_number, tokens in enumerate(tokens_por_linha, start=1):
        # Gera o corpo da linha atual
        assembly_lines = gerarCorpoAssembly(tokens, literal_labels, memory_labels)

        # ocupa 8 bytes porque eh double
        result_offset = (line_number - 1) * 8

        # antes de executar a linha, salva o numero dela em current_line, depois executa a expressao e salva o resultado em results
        program_lines.extend(
            [
                f"mov r0, #{line_number}",
                "ldr r1, =current_line",
                "str r0, [r1]",
                *assembly_lines,
                "bl pop_to_d0",
                "ldr r0, =results",
                f"add r0, r0, #{result_offset}",
                "vstr d0, [r0]",
                "",
            ]
        )

    # dados do programa
    data_lines = [".data"]

    # literais sao usados pelas rotinas auxiliares 0.0 e 1.0
    if "label_0_0" not in literal_labels:
        data_lines.append("label_0_0: .double 0.0")
    if "label_1_0" not in literal_labels:
        data_lines.append("label_1_0: .double 1.0")

    # deeclara todos os numeros encontrados nas expressoes
    for label, value in literal_labels.items():
        data_lines.append(f"{label}: .double {value}")

    # declara as variaveis de memoria usadas nas expressões
    for label in memory_labels:
        data_lines.append(f"{label}: .double 0.0")

    # variaveis auxiliares do programa
    data_lines.append("current_line: .word 0")
    data_lines.append(f"results: .space {len(tokens_por_linha) * 8}")
    data_lines.append("stack_base: .space 4096")
    data_lines.append("stack_top: .word 0")

    # início do codigo gerado
    text_lines = [
        "",
        ".text",
        ".global _start",
        "_start:",
        "ldr r0, =stack_base",
        "ldr r1, =stack_top",
        "str r0, [r1]",
    ]

    # rotinas auxiliares sao chamadas durante a execucao
    runtime_lines = [
        "",
        "b end",
        "",
        "push_d0:",
        "push {r0, r1}",
        "ldr r0, =stack_top",
        "ldr r1, [r0]",
        "vstr d0, [r1]",
        "add r1, r1, #8",
        "str r1, [r0]",
        "pop {r0, r1}",
        "bx lr",
        "",
        "pop_to_d0:",
        "push {r0, r1}",
        "ldr r0, =stack_top",
        "ldr r1, [r0]",
        "sub r1, r1, #8",
        "vldr d0, [r1]",
        "str r1, [r0]",
        "pop {r0, r1}",
        "bx lr",
        "",
        "pop_to_d1:",
        "push {r0, r1}",
        "ldr r0, =stack_top",
        "ldr r1, [r0]",
        "sub r1, r1, #8",
        "vldr d1, [r1]",
        "str r1, [r0]",
        "pop {r0, r1}",
        "bx lr",
        "",
        "res_lookup:",
        "ldr r0, =current_line",
        "ldr r1, [r0]",
        "vcvt.s32.f64 s0, d0",
        "vmov r2, s0",
        "sub r1, r1, r2",
        "sub r1, r1, #1",
        "cmp r1, #0",
        "blt res_zero",
        "mov r2, #8",
        "mul r1, r1, r2",
        "ldr r0, =results",
        "add r0, r0, r1",
        "vldr d0, [r0]",
        "bx lr",
        "res_zero:",
        "ldr r0, =label_0_0",
        "vldr d0, [r0]",
        "bx lr",
        "",
        # divisao inteira por subtracoes sucessivas (//)
        "op_int_div:",
        "vcvt.s32.f64 s0, d1",
        "vcvt.s32.f64 s2, d0",
        "vmov r0, s0",
        "vmov r1, s2",
        "cmp r1, #0",
        "beq int_div_zero",
        "mov r2, #0",
        "mov r3, r0",
        "int_div_loop:",
        "cmp r3, r1",
        "blt int_div_done",
        "sub r3, r3, r1",
        "add r2, r2, #1",
        "b int_div_loop",
        "int_div_done:",
        "vmov s4, r2",
        "vcvt.f64.s32 d0, s4",
        "bx lr",
        "int_div_zero:",
        "ldr r0, =label_0_0",
        "vldr d0, [r0]",
        "bx lr",
        "",
        # modulo tambem por subtracoes sucessivas (%)
        "op_int_mod:",
        "vcvt.s32.f64 s0, d1",
        "vcvt.s32.f64 s2, d0",
        "vmov r0, s0",
        "vmov r1, s2",
        "cmp r1, #0",
        "beq int_mod_zero",
        "mov r2, r0",
        "int_mod_loop:",
        "cmp r2, r1",
        "blt int_mod_done",
        "sub r2, r2, r1",
        "b int_mod_loop",
        "int_mod_done:",
        "vmov s4, r2",
        "vcvt.f64.s32 d0, s4",
        "bx lr",
        "int_mod_zero:",
        "ldr r0, =label_0_0",
        "vldr d0, [r0]",
        "bx lr",
        "",
        # potencia com expoente inteiro
        "op_pow:",
        "push {r0, r1}",
        "vcvt.s32.f64 s0, d0",
        "vmov r1, s0",
        "ldr r0, =label_1_0",
        "vldr d0, [r0]",
        "cmp r1, #0",
        "beq pow_done",
        "pow_loop:",
        "vmul.f64 d0, d0, d1",
        "subs r1, r1, #1",
        "bne pow_loop",
        "pow_done:",
        "pop {r0, r1}",
        "bx lr",
        "",
        "end:",
        "b end",
    ]

    # retorna as linhas do programa
    return "\n".join(data_lines + text_lines + program_lines + runtime_lines)



# Lê o arquivo, chama o parseExpressao e gera o programa.s final
if __name__ == "__main__":
    lines = []

    if lerArquivo("arquivo_teste.txt", lines):
        tokens_por_linha = []

        for line_number, line in enumerate(lines, start=1):
            valid, tokens = parseExpressao(line, line_number)

            if valid:
                tokens_por_linha.append(tokens)
            else:
                raise ValueError(f"Linha invalida no arquivo de entrada: {line}")

        assembly = gerarAssembly(tokens_por_linha)

        with open("programa.s", "w", encoding="utf-8") as file:
            file.write(assembly)

        print("Arquivo salvo: programa.s")
