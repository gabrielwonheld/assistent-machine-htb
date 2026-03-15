#!/bin/bash

# Cores para o terminal
GREEN='\03rd[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}[*] Iniciando configuração do laboratório CTF...${NC}"

# 1. Configurar o Python e dependências
echo -e "${GREEN}[+] Configurando ambiente Python...${NC}"
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}[!] 'uv' não encontrado. Instalando dependências via pip...${NC}"
    pip install -r requirements.txt
else
    echo -e "${GREEN}[+] 'uv' encontrado. Sincronizando dependências...${NC}"
    uv pip install -r requirements.txt
fi

# 2. Configurar permissões do script de backup (bkp.py)
echo -e "${GREEN}[+] Configurando script de backup para Privilege Escalation (Python Library Hijacking)...${NC}"
chmod 755 bkp.py

# Descobrir o usuário atual
CURRENT_USER=$(whoami)

# Criar uma tarefa no Cron para rodar o bkp.py a cada 1 minuto como root
CRON_JOB="* * * * * root /usr/bin/python3 $(pwd)/bkp.py"
CRON_FILE="/etc/cron.d/bkp_ctf"

echo -e "${YELLOW}[!] Configurando crontab em $CRON_FILE. Será solicitada sua senha atual:${NC}"
echo "$CRON_JOB" | sudo tee $CRON_FILE > /dev/null
if [ $? -eq 0 ]; then
    sudo chmod 644 $CRON_FILE
    echo -e "${GREEN}[+] Cron task adicionada com sucesso! O script rodará a cada 1 min como root.${NC}"
else
    echo -e "${RED}[-] Falha ao adicionar regra no cron. Faça manualmente:${NC}"
    echo "    echo \"$CRON_JOB\" | sudo tee $CRON_FILE"
fi

# 3. Preparando o ambiente do Python Path (Library Hijacking)
echo -e "${GREEN}[+] Garantindo que o diretório atual será vulnerável a PATH hijacking...${NC}"
# Não é necessário fazer nada extra aqui, pois o comando 'sudo python3 bkp.py' no mesmo
# diretório já busca bibliotecas locais primeiro antes da stdlib (como o zipfile.py).

echo -e "${YELLOW}========================================================================${NC}"
echo -e "${GREEN}[+] Laboratório configurado com sucesso!${NC}"
echo -e "${YELLOW}Resumo das vulnerabilidades:${NC}"
echo -e "1. ${GREEN}Mass Assignment:${NC} Modificar /update-profile injetando campos como 'is_admin'."
echo -e "2. ${GREEN}SSTI / RCE:${NC} Upload de ficha técnica com payload Jinja."
echo -e "3. ${GREEN}Privilege Escalation:${NC} O root executa '$(pwd)/bkp.py' via cron a cada minuto."
echo -e "   Para explorar (Library Hijacking), crie um arquivo 'zipfile.py' malicioso no "
echo -e "   diretório do script de backup!"
echo -e "${YELLOW}========================================================================${NC}"
