
<h1 align="center"> Spondere </h1>

<h2> Sistema para controle de frequência acadêmica por meio de verificação biométrica</h2>

<h3 align="center">Índice</h3>

* [Introdução](#introdução)
* [Requisitos de sistema](#Requisitos-de-sistema)
* [Instalação](#Instalação)
* [Configurando o sistema](#Configurando-o-sistema)
* [Iniciando o sistema](#Iniciando-o-sistema)
* [Tabela de erros](#Tabela-de-erros)

<h3 align="center">Introdução</h3>
Este subsistema se trata da interface de programação de aplicações (API, do inglês <i>application programming interface</i>) da metodologia de controle de frequência acadêmica por validação biométrica. Esta API tem como propósito fornecer funcionalidades para aplicações dedicadas a docentes e discentes(como por exemplo uma aplicação móvel) e a instituições de ensino.

Neste documento são descritos os passos necessários para que o sistema possa ser colocado em funcionamento. Todos os passos descritos são referentes ao sistema operacional Linux com Kernel 5.0 ou superior. Deste modo, é relatado os requisitos de sistema necessários, os passos para configuração do sistema, como pode ser realizada a inicialização e, por fim, é descrito uma tabela de erros.


<h3 align="center">Requisitos de sistema</h3>
Para a utilização do sistema de forma adequada e de acordo com com a sua finalidade é necessária a instalação de uma série de programas ou módulos. Parte desses pacotes é especificada no arquivo "requirements.txt" encontrada na pasta raiz do servidor (pasta nomeada de "spondereServer"). Alguns dos pacotes e/ou módulos podem ser substituídos por outros com finalidade semelhante, mas o uso de tais não garante o correto funcionamento da plataforma. Entre os principais componentes necessários ou não incluídos no arquivo "requirements.txt" estão descritos na tabela 1.


<center><h5><b>Tabela 1: Principais requisitos de sistema</b></h5></center>


Nome | Descrição | Versão |
------------ | :-----------: | -----------: |
<i>OpenCV</i> |O <i>OpenCV</i>(do inglês <i>Open Source Computer Vision Library</i>) é uma biblioteca de software de visão computacional e aprendizado de máquina de código aberto. | 4.5.3 |
Codecs| Pré requisito para o funcionamento do OPenCV. | --- |
Python-jose | Biblioteca do python para gerar e verificar JWT (do inglês <i>JSON Web Token</i>). | 3.3.0 |
<i>FastAPI</i> | <i>FastAPI</i> é um framework web moderno e rápido(de alto desempenho) para construir APIs com Python 3.6+. | 0.68.1 |
Python | Python é uma linguagem de programação de alto nível, interpretada por script, imperativa, orientada a objetos, funcional, de tipagem dinâmica e forte.  | 3.9.10|
Numpy | NumPy é uma biblioteca para a linguagem de programação Python, que suporta o processamento de grandes, multidimensionais arranjos e matrizes, juntamente com uma grande coleção de funções matemáticas de alto nível para operar sobre estas matrizes. | 1.21.2 |
<i>Scikit-Learn</i> | O <i>scikit-learn</i> é uma biblioteca de aprendizado de máquina de código aberto para a linguagem de programação Python. | 1.0.1 |
<i>Scikit-image</i> | O <i>Scikit-image</i> é uma biblioteca de processamento de imagens de código aberto para a linguagem de programação Python. | 0.18.3 |

<h3 align="center">Instalação </h3>
    
    ...

Recomendase a utilizar um gerenciador de ambiente de desenvovimento, como por exemplo virtualev.

Tambem é recomendado a utilização seguir os passos da instalaçao do docker e dockercompose oficiais. A instalação do docker e docker compose pode ser ignorada caso opte por utilizar o banco de dados de outra forma.

    ...

<h3 align="center">Configurando o sistema </h3>

    ...

<h3 align="center">Iniciando o sistema</h3>
Com o sistema devidamente instalado e configurado bas executar o seguinte comando:

    $ python main.py


<summary> <h2>Tabela de erros</h2></summary>

|Código do erro | tipo | descrição|
|--- | --- | ---|
|u001| Usuário | Usuário ou senha incorreto.|
|u002| Usuário | Usuário não tem credencial de administrador.|
|r001| Reconhecimento| caracteristicas e rotulos não coincidem.|
|r002| Reconhecimento| Nenhuma caracterista de face encontrada.|
|r003| Reconhecimento| Imagens insufucientes com a face detectavel.|
|r004| Reconhecimento| quantidade de caracteristicas insuficiente.|
|r005| Reconhecimento| A face do usuário não foi reconhecida.|
|f001| Frequência| Nehuma frequência encontrada com os dados fornecidos.|
|b001| Biométri|Horário de checagem de imagens já foi ultrapassado, ou o aluno não pertence a essa turma.|