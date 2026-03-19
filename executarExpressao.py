"""

Grupo: RA1-6
Alunos:
    Fabricio Goes Pinterich : @fapinter
    Leonardo Min Woo Chung: @LeonardoChung
    Phillip Wan Tcha Yan: @PhillipYan

"""
from typing import List, Tuple, Dict
from collections import deque

#Após um parênteses ser resolvido, essa função é chamada para
#substituir o conteúdo dos parênteses pelo resultado
def remover_parenteses(tokens: List[str], idx_start: int, idx_end: int, result : float | None = None) -> List[str]:
    copia_tokens = tokens.copy()
    tokens_start = copia_tokens[0:idx_start]
    if result != None:
        tokens_start.append(str(result))
    tokens_end = copia_tokens[idx_end+1:]
    tokens_start.extend(tokens_end)
    print(f'resultado: {tokens_start}')
    return tokens_start

def executarExpressao(
    tokens: List[str],
    resultados: Dict[int, float],
    memoria: Dict[str, float],
    num_linha: int
) -> Tuple[Dict[int, float], Dict[str, float]]:


    def executar_AFD(
        tokens: List[str],
        resultados: Dict[int,float],
        memoria: Dict[str,float],
        num_linha: int
    ) -> Tuple[bool, float]:
        stack_interno = deque()


    # Extrai a partir do parênteses mais a direita para tratar parênteses aninhados ( Ex: ( 10 12 + ( 21 20 - ) + ) )
    # Caso não estejam aninhados (Ex: (10 12 -) (20 21 +) +)
    # apenas irá resolver a expressão de trás para frente, o que não altera em nada no resultado
    for l_par in reversed([i for i, val in enumerate(list) if val=='(']):
        r_par = tokens.index(start=i, value=')')
        #Extrai os tokens dentro dos parênteses e passa para a AFD resolver
        sub_tokens = tokens[l_par+1:r_par]
        print(f'Sub Tokens: {sub_tokens}')
        result_found, result_value = executar_AFD(tokens=sub_tokens, resultados=resultados, memoria=memoria, num_linha=num_linha)
        #Caso nenhum erro ocorra durante a execução
        tokens = remover_parenteses(
            tokens=tokens, idx_start=l_par, idx_end=r_par,
            result=result_value if result_found else None
        )
        print(i)


if __name__ == "__main__":
    list = ['(','10', '12', '+','(', '10', '12', '-', ')', ')']
    for i in reversed([i for i, val in enumerate(list) if val=='(']):
        r_par = list.index(')',i)
        list = remover_parenteses(tokens=list, idx_start=i, idx_end=r_par, result=None)
        print(list)
