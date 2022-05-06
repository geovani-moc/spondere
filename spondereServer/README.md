
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


<center>
<h5><b>Tabela 1: Principais requisitos de sistema</b></h5>
</center>


Nome | Descrição | Versão |
------------ | :-----------: | -----------: |
<i>OpenCV</i> |O <i>OpenCV</i>(do inglês <i>Open Source Computer Vision Library</i>) é uma biblioteca de software de visão computacional e aprendizado de máquina de código aberto. | 4.5.3 |
Codecs(FFmpeg)| FFmpeg é um projeto de software livre e de código aberto que consiste em um conjunto de bibliotecas e programas para lidar com vídeo, áudio e outros arquivos e fluxos multimídia(é um pré requisito para o funcionamento do <i>OPenCV</i>). | 4.4.1 |
Python-jose | Biblioteca do python para gerar e verificar JWT (do inglês <i>JSON Web Token</i>). | 3.3.0 |
<i>FastAPI</i> | <i>FastAPI</i> é um framework web moderno e rápido(de alto desempenho) para construir APIs com Python 3.6+. | 0.68.1 |
Python | Python é uma linguagem de programação de alto nível, interpretada por script, imperativa, orientada a objetos, funcional, de tipagem dinâmica e forte.  | 3.9.10|
Numpy | NumPy é uma biblioteca para a linguagem de programação Python, que suporta o processamento de grandes, multidimensionais arranjos e matrizes, juntamente com uma grande coleção de funções matemáticas de alto nível para operar sobre estas matrizes. | 1.21.2 |
<i>Scikit-Learn</i> | O <i>scikit-learn</i> é uma biblioteca de aprendizado de máquina de código aberto para a linguagem de programação Python. | 1.0.1 |
<i>Scikit-image</i> | O <i>Scikit-image</i> é uma biblioteca de processamento de imagens de código aberto para a linguagem de programação Python. | 0.18.3 |
|Dblib| -- | -- |

<h3 align="center">Instalação </h3>

Para a realização da instalação é recomendado a utilizar um gerenciador de ambiente de desenvolvimento, como por exemplo, virtualenv. Com o python e pip devidamente instalados e configurados a instalação do sistema segue as seguintes etapas:

1 - Instalação dos meta-pacotes necessários para compilar software:

    sudo apt install build-essential

2 - Instalação dos codecs necessários para o funcionamento do :

    sudo apt install ffmpeg libsm6 libxext6

3 - Instalação das bibliotecas necessárias:

    pip install -r requeriments.txt
    
<h3 align="center">Configurando o sistema </h3>

Com o sistema devidamente instalado é necessário realizar as configurações.

Criar um arquivo("config.ini") de configurações para informações do banco de dados e chave secreta:

    touch config.ini

No arquivo de configuração deverá ter informações sobre o banco de dados(suportado apenas postgres) e chave secreta como no exemplo a seguir:

    [postgres]
    DB_NAME = BD_MY_DATA_BASE
    PASSWORD = admin
    USERNAME = admin
    HOST = 127.0.0.1
    PORT = 5432

    [token]
    SECRET_KEY = 9251d7350a113a369b5fb1c6431f7bd91818607b479e98461d0c18474efb1873


A chave secreta("SECRET_KEY") é uma chave secreta aleatória segura, para gerar chaves pode-se usar o comando:

    openssl rand -hex 32

Também é necessário realizar a configuração do arquivo "settings.py" nele se encontram os parâmetros de funcionamento do sistema. Existem algumas variáveis que devem ser modificadas como:

- PATH_IMAGES: local onde as imagens de treinamento serão armazenadas para extração de características. O caminho da pasta indicada nesta variável deve existir, caso contrário, podem ocorrer erros na execução do sistema.

- TIMEZONE_API_SERVER: Deve ser informado a zona de tempo do sistema no formato +-HH:MM(Exemplo: +03:00).

<h3 align="center">Iniciando o sistema</h3>
Com o sistema devidamente instalado e configurado bas executar o seguinte comando:

    python main.py

<b>Observação:</b> Caso o sistema esteja sendo iniciado para a relaização de teste, os scripts encontrados na pasta [scripts](/spondereServer/scripts/) cotém dados para a [criação](/spondereServer/scripts/database/) da estrutura do banco de dados relacional(<i>postgres</i>) e [adição](/spondereServer/scripts/populate/) de tuplas fakes para popular o banco de dados criado.


<summary> <h2>Tabela de erros</h2></summary>

|Código do erro | tipo | descrição|
|--- | --- | ---|
|u001| Usuário | Usuário ou senha incorreta.|
|u002| Usuário | Usuário não tem credencial de administrador.|
|r001| Reconhecimento | Quantidade de características e rótulos não coincidem.|
|r002| Reconhecimento | Nenhuma característica de face encontrada.|
|r003| Reconhecimento | Imagens insuficientes que tenham a face detectável.|
|r004| Reconhecimento | A quantidade de características é insuficiente.|
|r005| Reconhecimento | A face do usuário não foi reconhecida.|
|r006| Reconhecimento | A extração de características falhou.|
|f001| Frequência | Nehuma frequência encontrada com os dados fornecidos.|
|f002| Frequência | Falha ao verificar se já existe frequência válida.|
|b001| Biométria| Horário de checagem de imagens já foi ultrapassado, ou o aluno não pertence a essa turma.|
|b002| Biometria| Não foi possível desabilitar a biometria.|
|b003| Biometria| A biometria foi desabilitada, mas ocorreu um problema ao apagar os arquivos de biometria.|
|b004| Biometria| Ocorreu algum problema ao tentar remover os aquivos com o cache de treinamento dos dados biometricos.|
|bd001| Banco de dados | Erro ao apagar este item, caso exista tuplas que utilizam esse item, apague-os primeiro.|