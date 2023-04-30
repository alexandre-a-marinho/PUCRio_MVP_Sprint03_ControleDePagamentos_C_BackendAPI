# Controle de Pagamentos

MVP da primeira Sprint da pós graduação em Engenharia de Software da PUC-Rio (**MVP Sprint 01**)

Autor: Alexandre Alves Marinho

---
## Como executar:

É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment).
 
Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

O comando abaixo instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`:
```
(env)$ pip install -r requirements.txt
```
Para executar a API  basta executar:
```
(env)$ flask run --host 0.0.0.0 --port 5000
```
Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte.
```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status e documentação da API em execução.
