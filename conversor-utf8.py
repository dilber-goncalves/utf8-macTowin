import os
import unicodedata
import tkinter as tk
from tkinter import filedialog, messagebox

def corrigir_nome_mojibake(nome_antigo):
    """
    FEITO POR ==Dilber Goncalves==
    Tenta corrigir nomes de arquivos com problemas de 'mojibake'.
    """
    try:
        nome_corrigido = nome_antigo
        
        # Tentativa 1: Latin-1 para UTF-8
        bytes_corrompidos = nome_antigo.encode('latin-1', errors='ignore')
        nome_tentativa_1 = bytes_corrompidos.decode('utf-8', errors='ignore')
        
        if nome_tentativa_1 != nome_antigo:
            nome_corrigido = nome_tentativa_1
        
        if nome_corrigido == nome_antigo:
            # Tentativa 2: UTF-8 para Latin-1
            bytes_corrompidos = nome_antigo.encode('utf-8', errors='ignore')
            nome_tentativa_2 = bytes_corrompidos.decode('latin-1', errors='ignore')
        
            if nome_tentativa_2 != nome_antigo:
                nome_corrigido = nome_tentativa_2
        
        nome_normalizado = unicodedata.normalize('NFC', nome_corrigido)
        return nome_normalizado
        
    except Exception:
        return nome_antigo

def renomear_arquivos_mantendo_acentos():
    # --- INTERFACE PARA SELECIONAR PASTA ---
    root = tk.Tk()
    root.withdraw() # Esconde a janela principal do tkinter
    root.attributes("-topmost", True) # Faz a janela aparecer na frente de tudo
    
    diretorio_alvo = filedialog.askdirectory(title="Selecione a pasta com os arquivos para corrigir")
    
    if not diretorio_alvo: # Se o usuário cancelar a seleção
        print("Operação cancelada pelo usuário.")
        return

    print(f"--- Iniciando a correção no diretório: {diretorio_alvo} ---")
    
    arquivos_renomeados = 0
    
    for nome_antigo in os.listdir(diretorio_alvo):
        caminho_antigo_completo = os.path.join(diretorio_alvo, nome_antigo)
        
        if os.path.isdir(caminho_antigo_completo):
            continue

        nome_corrigido = corrigir_nome_mojibake(nome_antigo)

        if nome_corrigido != nome_antigo:
            try:
                caminho_novo_completo = os.path.join(diretorio_alvo, nome_corrigido)
                os.rename(caminho_antigo_completo, caminho_novo_completo)
                print(f"Renomeado: '{nome_antigo}' -> '{nome_corrigido}'")
                arquivos_renomeados += 1
            except Exception as e:
                print(f"Erro ao renomear o arquivo '{nome_antigo}': {e}")

    # Mensagem final visual para o usuário
    messagebox.showinfo("Concluído", f"Processo finalizado!\n{arquivos_renomeados} arquivos foram corrigidos.")
    print(f"--- Concluído. {arquivos_renomeados} arquivos renomeados. ---")

if __name__ == "__main__":
    renomear_arquivos_mantendo_acentos()