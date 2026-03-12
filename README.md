# RA1-6-AnalisadorLexico
## Grupo RA1-6
Alunos:
- Fabricio Goes Pinterich : @fapinter
- Leonardo Min Woo Chung : @LeonardoChung
- Phillip Wan Tcha Yan : @PhillipYan

## Do que se trata o Repositorio?
Este repositorio é um projeto para a matéria de *Construção de Interpretadores*
lecionada pelo professor *Frank Alcantara*

O projeto consiste em construir um *Analisador Léxico* para leitura, execução e
conversão para Assembly de *expressões aritméticas* escritas em *RPN(Reverse Polish Notation)*
a partir de uma linguagem pré-definida.

## Linguagem Estabelecida
O projeto possui os seguintes componentes para montar as expressões:
- **Números Inteiros e Reais**: 10, 21.2, -23
- **Operadores aritméticos**: +, -, *, /, //, %, ^
- **Parênteses**: (  )
- **Comandos Especiais**:
    - (N RES): Resposta de Nésima linha acima
    - (N MEM): Armazenamento de um Número Real(N) em uma váriavel(MEM)
        - MEM pode ser qualquer string composta somente por **letras maiúsculas**
    - (MEM): Retorno do valor armazenado em MEM
        - Caso nenhum valor tenha sido atribuído, retorna *0.0*


## Como funciona ?
O projeto consiste em 4 partes principais:

- **Parsing da Expressão**: Analisa a expressão em termos de sintaxe, captando erros como:
    - Números mal formados (Ex: 10,5 10.4.3).
    - Caracteres fora da Linguagem estabelecida (Ex: &, **, strings_lower_case).
    - Parênteses não fechados, fechamento sem abertura e parênteses vazios.

- **Execução da Expressão**: Executa a expressão e valida a expressão em termos de:
    - Falta de parâmetros para uma operação (Ex: 2 +)
    - Parâmetros inválidos para uma operação (Ex: 10 0 /(divisão por zero), 20.4 2 //(divisão inteira com reais))