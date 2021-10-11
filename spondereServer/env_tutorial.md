#Instalando o virtualenv:
    -pip install virtualenv

#Criando o ambiente virtual(deve estar dentro da pasta do projeto):
    -python -m venv nome_do_ambiente_virtual

#Acessar ambiente virtual:
    -source nome_do_ambiente_virtual/bin/activate

#listar pacotes instalados(ambiente já deve estar ativado):
    -pip list

#instalar novos pacotes(ambiente já deve estar ativado):
    -pip install nome-do-pacote

#Sair do ambiente virtual:
    -deactivate

#Criar arquivo com bbibliotecas em uso:
    -pip freeze > requirements.txt

#Instalar todas as dependências de um arquivo:
    -pip install -r requirements.txt 

