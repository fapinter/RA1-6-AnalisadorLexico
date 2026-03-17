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

#Definição das Transições
def define_next_state(next_token: str, next_position: int, size: int) -> str:
    #Evita erros de index out of range pela natureza da captura do próximo estado
    if next_position >= size:
        return ''
    operacoes = {'+','-','*','/', '//', '%', '^'}
    parenteses = {'(', ')'}
    if next_token in operacoes:
        return 'operacao'
    elif next_token in parenteses:
        return 'parenteses'
    elif is_float(next_token):
        return 'numero'
    elif next_token.isupper():
        return 'comando'
    else:
        raise InvalidParsingError(f'Caracter [{next_token}] invalido/Mal Formatado')


def parseExpressao(linha: str, numero_linha: int) -> Tuple[bool, List[str]]:
    #Utilizado para Números inteiros e reais
    def estadoNumero(tokens: List[str], position: int) -> str:
        try:
            return define_next_state(next_token=tokens[position+1], next_position=position+1, size=len(tokens))
        except InvalidParsingError:
            raise

    #Utilizado para Operadores(+, - , *, /, //, %, ^)
    def estadoOperacao(tokens: List[str], position: int) -> str:
        try:
            return define_next_state(next_token=tokens[position+1], next_position=position+1, size=len(tokens))
        except InvalidParsingError:
            raise
    
    #Utilizado para Comandos (MEM, RES)
    def estadoComando(tokens: List[str], position: int) -> str:
        try:
            return define_next_state(next_token=tokens[position+1], next_position=position+1, size=len(tokens))
        except InvalidParsingError:
            raise
        
    #Utilizado para Parênteses
    def estadoParenteses(stack_parenteses: deque, tokens: List[str], position: int) -> str:
        try:
            #Fechamentos de parênteses removem o último item do stack
            if tokens[position] == ')':
                #Nenhuma abertura no stack
                if len(stack_parenteses) == 0:
                    raise InvalidParsingError('Fechamento de parenteses sem abertura')
                #Remove a ultima abertura de parenteses
                stack_parenteses.pop()
            #Abertura de parenteses adicionam um item no final do stack
            elif tokens[position] == '(':
                stack_parenteses.append('(')
            
            return define_next_state(next_token=tokens[position+1], next_position=position+1, size=len(tokens))
        
        except InvalidParsingError:
            raise
           
    #Stack para controlar abertura e fechamento de parenteses
    stack_parenteses = deque()
    tokens = linha.split(' ')
    try:
        next_state = define_next_state(tokens=tokens, next_position=0, size=len(tokens))
    except InvalidParsingError as ipe:
        print(f'Linha [{numero_linha}] é inválida: {ipe}')
        return False, tokens

    for position in range(0, len(tokens)):
        try:
            match(next_state):
                case 'numero':
                    next_state = estadoNumero(tokens=tokens, position=position)
                case 'parenteses':
                    next_state = estadoParenteses(stack_parenteses=stack_parenteses, tokens=tokens, position=position)
                case 'operacao':
                    next_state = estadoOperacao(tokens=tokens, position=position)
                case 'comando':
                    next_state = estadoComando(tokens=tokens, position=position)
                
        except InvalidParsingError as ipe:
            print(f'Linha [{numero_linha}] é inválida: {ipe}')
            return False, tokens
    
    #Caso os parênteses estejam desbalanceados, a expressão é considerada inválida
    if len(stack_parenteses) > 0:
        print(f'Linha {numero_linha} eh invalida: Parenteses nao fechados')
        return False, tokens
    return True, tokens
        
    
if __name__ == "__main__":
    test_cases = [
        '5.5.5 2 +',
        '10,5 4 -',
        '10 5 $',
        '10 ( 2 4 +',
        '10 asa +',
        '10 12 +',
        '10 13.5 //'
    ]
    f_res = open('resultados_teste_parse.txt', 'w')
    for test_idx in range(0, len(test_cases)):
        line = test_cases[test_idx]
        print(f'[{test_idx}]Tokenized line: {line.split(' ')}')

        valid_line, tokenized_string = parseExpressao(linha=line, numero_linha=test_idx)
        
        f_res.write(f'Parse[{valid_line}] {line}\n')
    f_res.close()