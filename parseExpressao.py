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

def define_next_state(next_position: int, tokens: List[str], size: int) -> str:
    if next_position >= size:
        return ''
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
        raise InvalidParsingError('Caracter invalido/Mal Formatado')

#Retornara se a linha nao possui nenhum erro de sintaxe
# Erros como os listados abaixo nao sao detectados nesta fase
# apenas na fase de execucao
# - (Numero insuficiente para operador)
# - (Valor invalido para comandos/operadores)
def parseExpressao(linha: str, numero_linha: int) -> bool:

    #Utilizado para o Parse de numeros
    #erros de formatacao ja sao capturados no define_next_state()
    def estadoNumero(tokens: List[str], position: int) -> str:
        try:
            return define_next_state(next_position=position+1, tokens=tokens, size=len(tokens))
        except InvalidParsingError:
            raise

    #Utilizado tanto para Comando(MEM, RES)
    #quanto para Operadores(+, - , *, /, //, %, ^)
    def estadoOperacao(tokens: List[str], position: int) -> str:
        try:
            return define_next_state(next_position=position+1, tokens=tokens, size=len(tokens))
        except InvalidParsingError:
            raise
        
    def estadoParenteses(stack_parenteses: deque, tokens: List[str], position: int) -> str:
        try:
            #Fechamento de parenteses remove o ultimo item do stack
            if tokens[position] == ')':
                #Nenhuma abertura no stack
                if len(stack_parenteses) == 0:
                    raise InvalidParsingError('Fechamento de parenteses sem abertura')
                if tokens[position-1] == '(':
                    raise InvalidParsingError('Parenteses sem conteudo dentro')
                #Remove a ultima abertura de parenteses
                stack_parenteses.pop()
            #Abertura de parenteses adicionam um item no final do stack
            elif tokens[position] == '(':
                stack_parenteses.append('(')
            
            return define_next_state(next_position=position+1, tokens=tokens, size=len(tokens))
        
        except InvalidParsingError:
            raise
           
    #Stack para controlar abertura e fechamento de parenteses
    stack_parenteses = deque()
    tokens = linha.split(' ')
    position = 0
    try:
        next_state = define_next_state(tokens=tokens, next_position=0, size=len(tokens))
    except InvalidParsingError as ipe:
        print(f'Linha {numero_linha} eh invalida: {ipe}')
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
                    next_state = estadoOperacao(tokens=tokens, position=position)

                case None:
                    raise InvalidParsingError
        except InvalidParsingError as ipe:
            print(f'Linha {numero_linha} eh invalida: {ipe}')
            return False, tokens
    
    if len(stack_parenteses) > 0:
        print(f'Linha {numero_linha} eh invalida: Parenteses nao fechados')
        return False, tokens
    return True, tokens
        
    
if __name__ == "__main__":
    num_passed = 0
    count_line = 0
    f_res = open('resultados_teste.txt', 'w')
    with open('arquivo_teste.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            #Tratamento da linha para separar dados para o relatorio
            count_line += 1
            separate_line = line.split(' @')
            line = separate_line[0]
            should = separate_line[1].replace('\n', '')
            if should.startswith('errado'):
                validation_step = separate_line[1].split(' ')[1]
            else:
                validation_step = ''
            print(f'[{count_line}]Tokenized line: {line.split(' ')}')
            valid_line, tokenized_string = parseExpressao(linha=line, numero_linha=count_line)
            
            #Verifica se o parser acertou ou errou
            passed = False
            if valid_line:
                if should=='certo':
                    passed = True
                    num_passed += 1
                if validation_step.startswith('exec'):
                    passed = True
                    num_passed += 1
            #Se encontra um erro que deve ser detectado
            #na fase do parse, o parser acertou
            else:
                if validation_step.startswith('parse'):
                    passed=True
                    num_passed += 1
            f_res.write(f'Passed[{passed}] Parse[{valid_line}] Answer[{should}] {line}\n')
    f_res.write(f'Passed [{num_passed}/{count_line}]')
    f_res.close()