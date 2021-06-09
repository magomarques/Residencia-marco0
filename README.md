# Residencia-marco0
Projeto MVP C.E.S.A.R. - Squad Marco[0] - Residência de Software

Roteiro para execução da aplicação:

1.	Fazer download e instalar o Python 3.9:
	https://www.python.org/downloads/ 
    Manuais para instalação: 
    https://python.org.br/instalacao-windows/ 
    https://python.org.br/instalacao-linux/ 

2.	Fazer download do repositório da aplicação: ver link do item 1

3.	Abrir o projeto numa IDE (Visual Studio Code preferencialmente)

4.	No terminal da IDE executar os seguintes comandos:
    4.1.	pip install -r requirements.txt
    4.2.	python manage.py makemigrations
    4.3.	python manage.py migrate
    4.4.	python manage.py runserver

    Obs.: Caso o gerenciador de pacotes ‘pip’ não seja instalado junto com o Python deve-se instalá-lo. Favor acessar: https://www.treinaweb.com.br/blog/gerenciando-pacotes-em-projetos-python-com-o-pip 

5.	Após a execução do comando 4.4 acessar o link http://127.0.0.1:8000/  gerado no terminal da IDE

6.	A aplicação irá iniciar o funcionamento no seu browser.

