#! /bin/zsh
# Execute o script com o comando: source venv_setup.sh
# Para sair do ambiente virtual, execute o comando: deactivate
python3 -m venv .venv
source .venv/bin/activate   
python3 -m ensurepip --upgrade
pip install --upgrade pip
pip list