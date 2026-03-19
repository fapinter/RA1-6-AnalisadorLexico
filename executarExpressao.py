"""

Grupo: RA1-6
Alunos:
    Fabricio Goes Pinterich : @fapinter
    Leonardo Min Woo Chung: @LeonardoChung
    Phillip Wan Tcha Yan: @PhillipYan

"""
from typing import List, Tuple, Dict
from collections import deque
from parseExpressao import is_float
from math import pow

def is_int(token: str) -> bool:
    try:
        int(token)
        return True
    except ValueError:
        return False

#Após um parênteses ser resolvido, essa função é chamada para
#substituir o conteúdo dos parênteses pelo resultado
def remover_parenteses(tokens: List[str], idx_start: int, idx_end: int, result : float | None = None) -> List[str]:
    copia_tokens = tokens.copy()
    tokens_start = copia_tokens[0:idx_start]
    if result != None:
        tokens_start.append(str(result))
    tokens_end = copia_tokens[idx_end+1:]
    tokens_start.extend(tokens_end)
    return tokens_start


def executar_AFD(
    tokens: List[str],
    resultados: Dict[int,float],
    memoria: Dict[str,float],
    num_linha: int
) -> float:
    def estadoNumero(token: str, stack: deque) -> None:
        stack.append(token)

    def estadoOperador(token: str, stack: deque) -> None:
        num_2 = float(stack.pop())
        num_1 = float(stack.pop())
        match(token):
            case '+':
                stack.append(num_1 + num_2)
            case '-':
                stack.append(num_1 - num_2)
            case '*':
                stack.append(num_1 * num_2)
            case '/':
                stack.append(num_1 / num_2)
            case '//':
                stack.append(num_1 // num_2)
            case '%':
                stack.append(num_1 % num_2)
            case '^':
                stack.append(pow(num_1, num_2))
    
    def estadoComando(
        token: str, stack: deque,
        resultados: Dict[int, float],
        memoria: Dict[str, float],
        num_linha: int
    ) -> None:
        
        if token=='RES':
            num_res = int(stack.pop())
            res = resultados[num_linha - num_res]
            print(f'resultado da linha {num_linha-num_res} invocado: {res}')
            stack.append(res)
        else:
            # Se existe um valor anterior, é armazenado na variável
            # Se não existir, inicializa a variável com valor 0.0 e adiciona ela ao stack
            if len(stack) > 0:
                value_mem = float(stack.pop())
                print(f'Valor {value_mem} atribuído a {token}')
                memoria[token] = value_mem
            else:
                if token not in memoria:
                    memoria[token] = 0.0
                print(f'Variável {token} chamada, valor {memoria[token]}')
                stack.append(str(memoria[token]))
                    

    operadores = {'+', '-', '*', '/', '//', '%', '^'}
    stack_RPN = deque()
    for token in tokens:
        if is_float(token) or is_int(token):
            estadoNumero(token=token, stack=stack_RPN)
        elif token in operadores:
            estadoOperador(token=token, stack=stack_RPN)
        else:
            estadoComando(token=token, stack=stack_RPN, resultados=resultados, memoria=memoria, num_linha=num_linha)
    return float(stack_RPN.pop())


def executarExpressao(
    tokens: List[str],
    resultados: Dict[int, float],
    memoria: Dict[str, float],
    num_linha: int
) -> None:

    # Extrai a partir do parênteses mais a direita para tratar parênteses aninhados ( Ex: ( 10 12 + ( 21 20 - ) + ) )
    # Caso não estejam aninhados (Ex: (10 12 -) (20 21 +) +)
    # apenas irá resolver primeiro pelos parênteses da direita à esquerda, o que não altera em nada no resultado
    for l_par in reversed([i for i, val in enumerate(tokens) if val=='(']):
        r_par = tokens.index(')', l_par)
        #Extrai os tokens dentro dos parênteses e passa para a AFD resolver
        sub_tokens = tokens[l_par+1:r_par]
        result_value = executar_AFD(tokens=sub_tokens, resultados=resultados, memoria=memoria, num_linha=num_linha)
        
        #Caso nenhum erro ocorra durante a execução
        tokens = remover_parenteses(
            tokens=tokens, idx_start=l_par, idx_end=r_par,
            result=result_value
        )
    resultado = executar_AFD(tokens=tokens, resultados=resultados, memoria=memoria, num_linha=num_linha)
    resultados[num_linha] = resultado


if __name__ == "__main__":
    list = [
    ["(", "15.5", "-4.2", "*", ")", "(", "10", "5", "+", ")", "/"],
    ["(", "10", "2", "^", ")", "(", "50", "5", "//", ")", "(", "1", "RES", "10", "%", ")", "+", "+"],
    ["(", "25.5", "10.5", "+", ")", "(", "3.14", "PI", "PI", ")", "*"],
    ["(", "(", "8", "2", "/", ")", "(", "3", "1", "-", ")", "*", ")", "(", "100", "50", "%", ")", "+"],
    ["-100", "(", "(", "5", "2", "%", ")", "(", "10", "2", "*", ")", "+", ")", "/"],
]
    expected_results = [
        -4.340000000000001,
        115.66,
        113.04,
        8.0,
        -4.761904761904762
    ]
    resultados = {}
    memoria = {}
    for idx_string in range (0, len(list)):
        token_string = list[idx_string]
        print(f'Tokenized string: {token_string}')
        executarExpressao(tokens=token_string,resultados=resultados, memoria=memoria, num_linha=idx_string+1)
        print(f'Resultado da linha {idx_string+1}: {resultados[idx_string+1]}')
    print(f'Resultados: {resultados}')
    for idx in range (1, max(resultados.keys())+1):
        if resultados[idx]==expected_results[idx-1]:
            print(f'Linha {idx} correta')
    print(f'Memoria: {memoria}')
    