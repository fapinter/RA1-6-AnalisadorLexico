"""

Grupo: RA1-6
Alunos:
    Fabricio Goes Pinterich : @fapinter
    Leonardo Min Woo Chung: @LeonardoChung
    Phillip Wan Tcha Yan: @PhillipYan

"""
from typing import List, Tuple
from collections import deque

# Exceção customizada para indicar erros de validação
class InvalidParsingError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

#Validação se um token é um float ou não
def is_float(token: str) -> bool:
    try:
        float(token)
        return True
    except ValueError:
        return False

def parseExpressao(linha: str, numero_linha: int) -> Tuple[bool, List[str]]:

    #Cria tokens de Números inteiros e reais
    def estadoNumero(linha: str, position: int) -> Tuple[str, int]:
        idx = position+1
        token = linha[position]
        process = True
        is_float = False
        try:
            while process:
                if idx >= len(linha):
                    break
                char = linha[idx]
                if char.isdigit():
                    token += char
                elif char=='.':
                    if not is_float:
                        token+=char
                        is_float = True
                    else:
                        raise InvalidParsingError(f'Número Real [{token+char}] mal formatado')
                elif char==' ':
                    process = False
                else:
                    raise InvalidParsingError(f'Número [{token+char}] mal formatado')
                idx += 1
            return token, idx
        except InvalidParsingError:
            raise

    #Cria tokens de Operadores(+, - , *, /, //, %, ^)
    def estadoOperador(linha: str, position: int) -> Tuple[str, int]:
        idx = position+1
        token = linha[position]
        try:            
            if idx >= len(linha):
                return token, idx
            next_char = linha[idx]
            if next_char=='/':
                token+=next_char
                return token, idx+1
            elif next_char==' ':
                return token, idx
            else:
                raise InvalidParsingError(f'Operador [{token+next_char}] inválido')
        except InvalidParsingError:
            raise
    
    #Cria tokens de Comandos (MEM, RES)
    def estadoComando(linha: str, position: int) -> Tuple[str, int]:
        idx = position+1
        token = linha[position]
        process = True
        try:
            while process:
                if idx >= len(linha):
                    break
                char = linha[idx]
                if char.isupper():
                    token += char
                elif char == ' ':
                    process = False
                else:
                    raise InvalidParsingError(f'Caracter [{token+char}] Inválido/Mal Formatado')
                idx += 1
            return token, idx

        except InvalidParsingError:
            raise
        
    #Cria tokens de Parênteses
    def estadoParenteses(stack_parenteses: deque, linha: str, position: int) -> Tuple[str, int]:
        idx = position
        token = linha[idx]
        try:
            if token == ')':
                if len(stack_parenteses) > 0:
                    stack_parenteses.pop()
                else:
                    raise InvalidParsingError('Fechamento de parênteses sem abertura')
            elif token == '(':
                stack_parenteses.append('(')
            return token, idx+1        
        except InvalidParsingError:
            raise
    
    #Definição das Transições

    def define_transition(linha: str, position: int) -> str:
        operacoes = {'+','-','*','/', '%', '^'}
        parenteses = {'(', ')'}
        char = linha[position]
        if char in operacoes:
            return 'operacao'
        elif char in parenteses:
            return 'parenteses'
        elif char.isdigit():
            return 'numero'
        elif char==' ':
            return 'espaco'
        elif char.isupper():
            return 'comando'
        else:
            raise InvalidParsingError(f'Caracter [{char}] inválido/Mal Formatado')

           
    #Stack para controlar abertura e fechamento de parenteses
    tokens = []
    stack_parenteses = deque()
    idx = 0
    while idx < len(linha):
        try:
            next_state = define_transition(linha=linha, position=idx)
            match(next_state):
                case 'numero':
                    token, idx = estadoNumero(linha=linha, position=idx)
                    tokens.append(token)
                case 'parenteses':
                    token, idx = estadoParenteses(stack_parenteses=stack_parenteses, linha=linha, position=idx)
                    tokens.append(token)
                case 'operacao':
                    token, idx = estadoOperador(linha=linha, position=idx)
                    tokens.append(token)
                case 'comando':
                    token, idx = estadoComando(linha=linha, position=idx)
                    tokens.append(token)
                #Espaços demarcam a separação de tokens
                case 'espaco':
                    idx += 1

        except InvalidParsingError as ipe:
            print(f'Linha [{numero_linha}] é inválida: {ipe}')
            return False, []
    
    #Caso os parênteses estejam desbalanceados, a expressão é considerada inválida
    if len(stack_parenteses) > 0:
        print(f'Linha {numero_linha} eh invalida: Parenteses nao fechados')
        return False, []
    return True, tokens
        
    
if __name__ == "__main__":
    test_cases = [
        '5.5.5 2 +',
        '10,5 4 -',
        '10 ( ) 5 $',
        '10 ( 2 4 +',
        '10 AsA +',
        '10 12 +',
        '10 13.5 //',
        '10 MEMORIA',
        '10 RES',
        '( 10 MEM ) 20 +',
        '20 10 +'
    ]
    f_res = open('resultados_teste_parseExpressao.txt', 'w')
    for test_idx in range(0, len(test_cases)):
        line = test_cases[test_idx]
        valid_line, tokenized_string = parseExpressao(linha=line, numero_linha=test_idx)
        print(f'[{test_idx}]Tokenized line: {tokenized_string}')

        f_res.write(f"Parse[{valid_line}]\nToken split: {line.split(' ')} : AFD split: {tokenized_string}\n")
    f_res.close()
