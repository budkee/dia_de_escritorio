#!/bin/zsh

# Ativar o ambiente virtual
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "--> Ambiente virtual não encontrado. Criando ambiente virtual... <--"
    python3 -m venv .venv
    source .venv/bin/activate
fi

# Verificar se o arquivo requirements.txt existe
if [ -f "requirements.txt" ]; then
    echo "--> requirements.txt encontrado. Instalando dependências... <--"
    pip install -r requirements.txt
    pip list
else
    echo "--> requirements.txt não encontrado. Nenhuma dependência para instalar. <--"
fi
