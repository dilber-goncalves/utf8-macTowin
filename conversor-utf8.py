import os
import unicodedata
import tkinter as tk
from tkinter import filedialog, messagebox
from ftfy import fix_text

def corrigir_nome_mojibake(nome_antigo):
    try:
        nome_corrigido = fix_text(nome_antigo)
        nome_corrigido = unicodedata.normalize('NFC', nome_corrigido)
        return nome_corrigido
    except Exception:
        return nome_antigo

def renomear_tudo():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    
    diretorio_alvo = filedialog.askdirectory(title="Selecione a pasta (arquivos e subpastas serão corrigidos)")
    
    if not diretorio_alvo:
        return

    itens_renomeados = 0
    
    for raiz, diretorios, arquivos in os.walk(diretorio_alvo, topdown=False):
        
        for nome_antigo in (arquivos + diretorios):
            caminho_antigo = os.path.join(raiz, nome_antigo)
            
            if caminho_antigo == diretorio_alvo:
                continue
                
            nome_corrigido = corrigir_nome_mojibake(nome_antigo)

            if nome_corrigido != nome_antigo:
                try:
                    caminho_novo = os.path.join(raiz, nome_corrigido)
                    
                    if not os.path.exists(caminho_novo):
                        os.rename(caminho_antigo, caminho_novo)
                        itens_renomeados += 1
                except Exception as e:
                    print(f"Erro ao renomear {nome_antigo}: {e}")

    mensagem_final = (f"Processo concluído!\n"
                      f"{itens_renomeados} itens (arquivos/pastas) foram corrigidos.\n\n"
                      f"Obrigado!\nCreated by Dilber Gonçalves")
    messagebox.showinfo("Sucesso", mensagem_final)

if __name__ == "__main__":
    renomear_tudo()
