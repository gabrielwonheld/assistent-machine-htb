import os
import zipfile

def realizar_backup():
    print("Iniciando backup do banco de dados...")
    
    # 1. Cria um arquivo ZIP
    with zipfile.ZipFile("backup_secreto.zip", "w") as zf:
        zf.write("instance/assistencia.db")

    # 2. Envia o arquivo para o servidor do atacante
    os.system(f"cp backup_secreto.zip /tmp/backup_secreto.zip")

    time.sleep(1)
    print("Backup finalizado e compactado.")
if __name__ == "__main__":
    realizar_backup()