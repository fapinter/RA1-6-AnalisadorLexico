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
- **Números Inteiros e Reais**: 10, 21.2
- **Operadores aritméticos**: +, -, *, /, //, %, ^
- **Parênteses**: (, )
- **Comandos Especiais**:
    - (N RES): Resposta de Nésima linha acima
    - (N MEM): Armazenamento de um Número Real(N) em uma váriavel(MEM)
        - MEM pode ser qualquer string composta somente por **letras maiúsculas**
    - (MEM): Retorno do valor armazenado em MEM
        - Caso nenhum valor tenha sido atribuído, retorna *0.0*


## Como funciona ?
O projeto consiste nas seguintes partes principais:

- **Leitura do arquivo de entrada**:
    - O programa recebe como parâmetro um arquivo de texto contendo as expressões que serão processadas.
    - Esse arquivo deve ser passado pela linha de comando, por exemplo: `python main.py teste1.txt`.
    - Para executar o projeto, é necessário ter o **Python instalado** na máquina.

- **Parse da Expressão**: Gera e valida os tokens da expressão a partir de um AFD, captando erros como:
    - Números mal formados (Ex: 10,5 10.4.3).
    - Caracteres fora da Linguagem estabelecida (Ex: &, **, strings_lower_case).
    - Parênteses desbalanceados.

- **Execução da Expressão**: Executa a expressão:
    - Salvando os resultados e variáveis em dicionários para comparação posterior com o código Assembly.

- **Gerar Assembly**: Gera o arquivo .s com o código em assembly:
    - Separa cada expressão individualmente;
    - Valida e agrupa os tokens de acordo com os parênteses e cria instruções para cada operação;
    - Armazena constantes numéricas e variáveis;
    - Gera o código Assembly em um arquivo .s com todos as informações necessárias; 

- **Exibição dos resultados**:
    - Ao final da execução, o programa mostra os resultados obtidos.

## Como testar?
Cada arquivo, que não seja o `main.py` possui uma sessão para testes.
Ao rodar este arquivo em específico, os testes são realizados e os resultados são gravados em um arquivo
`resultados_teste_*.txt`, ou imprimidos no próprio terminal.

## Como executar
Para executar o programa principal, rode no terminal:

```bash
python main.py teste1.txt
python main.py teste2.txt
python main.py teste3.txt
