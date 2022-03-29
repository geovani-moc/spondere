
<h1 align="center"> Spondere </h1>

<h2> Sistema para controle de frequência acadêmica por meio de verificação biométrica</h2>

<h3 align="center">Índice</h3>

* [Requisitos de sistema](#Requisitos-de-sistema)
* [Instalação](#Instalação)
* [Configurando o sistema](#Configurando-o-sistema)
* [Iniciando o sistema](#Iniciando-o-sistema)
* [Tabela de erros](#Tabela-de-erros)


<h3 align="center">Requisitos de sistema</h3>
    
    ...
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