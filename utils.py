"""

Grupo: RA1-6
Alunos:
    Fabricio Goes Pinterich : @fapinter
    Leonardo Min Woo Chung: @LeonardoChung
    Phillip Wan Tcha Yan: @PhillipYan

"""
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

#Validação se um token é um inteiro ou não
def is_int(token: str) -> bool:
    try:
        int(token)
        return True
    except ValueError:
        return False