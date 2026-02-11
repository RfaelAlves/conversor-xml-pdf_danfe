# Importa o módulo do conversor
from conversor_danfe import processar_pasta
from pathlib import Path

# ========================================
# CONFIGURAÇÕES
# ========================================

# Caminho da pasta com os arquivos XML
PASTA_XML = f"{Path.cwd()}\\xml"

# Caminho da pasta onde os PDFs serão salvos
PASTA_PDF =  f"{Path.cwd()}\\xml\\pdf"

# Número de processos paralelos (ajuste conforme seu processador)
# Recomendado: 4, 8, ou 16
NUM_PROCESSOS = 8

# ========================================
# EXECUÇÃO
# ========================================

if __name__ == "__main__":
    print("=" * 80)
    print("CONVERSOR DE XML NF-e PARA DANFE PDF")
    print("=" * 80)
    print(f"\nPasta de entrada: {PASTA_XML}")
    print(f"Pasta de saída: {PASTA_PDF}")
    print(f"Processos paralelos: {NUM_PROCESSOS}\n")
    
    # Confirmação antes de iniciar
    resposta = input("Deseja iniciar o processamento? (s/n): ")
    
    if resposta.lower() == 's':
        print("\nIniciando processamento...\n")
        
        #Processamento PARALELO
        sucesso, erros = processar_pasta(
            pasta_entrada=PASTA_XML,
            pasta_saida=PASTA_PDF,
            num_processos=NUM_PROCESSOS
        )

        
        print("\n" + "=" * 80)
        print("PROCESSO FINALIZADO!")
        print("=" * 80)
        print(f"\n✅ Arquivos processados com sucesso: {sucesso}")
        print(f"❌ Arquivos com erro: {erros}")
        
        if erros > 0:
            print(f"\n⚠️  Verifique o arquivo 'log_erros.txt' na pasta de saída")
    else:
        print("\nProcessamento cancelado.")