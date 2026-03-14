import sys

def main():
    if len(sys.argv) < 2:
        print("escreva o nome do arquivo")
        return
        
    arquivoNome = sys.argv[1]
    
    try:
        with open(arquivoNome, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
    except FileNotFoundError:
        print("ñ foi possivel abrir o arquivo")
        return
    
    print(arquivoNome)
    print(len(linhas))            
    
if __name__ == "__main__":
    main()