
<h1 align="center"> Spondere </h1>

<h2> Sistema para controle de frequência acadêmica por meio de verificação biométrica</h2>

<h3 align="center">Índice</h3>

* [Requisitos de sistema](#introdução)
* [Requisitos de sistema](#Requisitos-de-sistema)
* [Instalação](#Instalação)
* [Configurando o sistema](#Configurando-o-sistema)
* [Iniciando o sistema](#Iniciando-o-sistema)
* [Tabela de erros](#Tabela-de-erros)

<h3 align="center">Introdução</h3>
...
Todos os passos descritos são referentes ao sistema operacional Linux com Kernel 5.0 ou superior. 
...

<h3 align="center">Requisitos de sistema</h3>
Para a utilização do sistema de forma adequada e de acordo com com a sua finalidade é necessária a instalação de uma série de programas ou módulos. Parte desses pacotes é especificada no arquivo "requirements.txt" encontrada na pasta raiz do servidor (pasta nomeada de "spondereServer"). Alguns dos pacotes e/ou módulos podem ser substituídos por outros com finalidade semelhante, mas o uso de tais não garante o correto funcionamento da plataforma. Entre os principais componentes necessários ou não incluídos no arquivo "requirements.txt" estão descritos na tabela 1.

| | Tabela 1: Principais requisitos de sistema ||
Nome | Descrição | Versão |
------------ | :-----------: | -----------: |
OpenCV | ... | ... |
Codecs| Pré requisito para o funcionamento do OPenCV. ||
FastAPI | ... | ... |
Python | ... | 3.9.10|



<h3 align="center">Instalação </h3>

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