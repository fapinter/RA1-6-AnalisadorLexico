from typing import List
from collections import deque

class InvalidParsingError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

#Validacao se um token eh um float ou nao
def is_float(token: str) -> bool:
    try:
        float(token)
        return True
    except ValueError:
        return False

def is_int(token: str) -> bool:
    try:
        int(token)
        return True
    except ValueError as e:
        return False



def define_next_state(next_position: int, tokens: List[str]) -> str:
    operacoes = {'+','-','*','/', '//', '%', '^'}
    parenteses = {'(', ')'}
    next_token = tokens[next_position]
    if next_token in operacoes:
        return 'operacao'
    elif next_token in parenteses:
        return 'parenteses'
    elif is_float(next_token):
        return 'numero'
    elif next_token.isupper():
        return 'comando'
    else:
        raise InvalidParsingError('Caracter invalido')

#Retornara se a linha nao possui nenhum erro de sintaxe
# Erros como os listados abaixo nao sao detectados nesta fase
# apenas na fase de execucao
# - (Numero insuficiente para operador)
# - (Valor invalido para comandos/operadores)
def parseExpressao(linha: str, numero_linha: int) -> bool:
    #Stack para controlar abertura e fechamento de parenteses
    stack_parenteses = deque()

    def estadoNumero(tokens: List[str], position: int):
        #Validacao da formatacao do numero(seja inteiro ou float)
        curr_token = tokens[position]
        if not is_float(curr_token):
            raise InvalidParsingError('Formatacao invalida do numero')
        
        return define_next_state(next_position=position+1, tokens=tokens)

        
    def estadoParenteses(stack_parenteses: deque, tokens: List[str], position: int):
        #Fechamento de parenteses remove o ultimo item do stack
        if tokens[position] == ')':
            #Nenhuma abertura no stack
            if len(stack_parenteses) == 0:
                raise InvalidParsingError('Fechamento de parenteses sem abertura')
            #Remove a ultima abertura de parenteses
            else:
                stack_parenteses.pop()
        
        #Abertura de parenteses adicionam um item no final do stack
        else:
            stack_parenteses.append(tokens[position])
        
        return define_next_state(next_position=position+1, tokens=tokens)        

    #Utilizado tanto para Comando(MEM, RES)
    #quanto para Operadores(+, - , *, /, //, %, ^)
    def estadoOperacao(tokens: List[str], position: int):
        return define_next_state(next_position=position+1, tokens=tokens)
           

    tokens = linha.split(' ')
    position = 0
    print('string tokenizada\n:',tokens)
    next_state = define_next_state(tokens=tokens, next_position=0)
    
    for position in range(0, len(tokens)):
        try:
            match(next_state):
                case 'numero':
                    next_state = estadoNumero(tokens=tokens, position=position)
                case 'parenteses':
                    next_state = estadoParenteses(stack_parenteses=stack_parenteses, tokens=tokens, position=position)
                case 'operacao', 'comando':
                    next_state = estadoOperacao(tokens=tokens, position=position)
                case None:
                    raise InvalidParsingError
        except InvalidParsingError as ipe:
            print(f'Linha {numero_linha} eh invalida: {ipe.message}')
            return False
    
    if len(stack_parenteses) > 0:
        print(f'Linha {numero_linha} eh invalida: Parenteses nao fechados')
        return False
    return True
        
    
if __name__ == "__main__":
    with open('arquivo_teste.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            separate_line = line.split('@')
            line = separate_line[0]
            should = separate_line[1]
            print(f'Linha : {line} , should: {should}')
            parseExpressao(linha=line, numero_linha=1)