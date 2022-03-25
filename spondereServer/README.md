# Projeto spondere-Server

## Iniciar servidor (uvicorn main:app --reload):
    
    python main.py

Em desenvolvimento ...

<summary> <h2>Tabela de erros </h2></summary>

|Código do erro | tipo | descrição|
|--- | --- | ---|
|u001| Usuário | Usuário ou senha incorreto.|
|u002| Usuário | Usuário não tem credencial de administrador.|
|r001| Reconhecimento| caracteristicas e rotulos não coincidem.|
|r002| Reconhecimento| Nenhuma caracterista de face encontrada.|
|r003|Reconhecimento|Imagens insufucientes com a face detectavel.|
|r004|Reconhecimento|quantidade de caracteristicas insuficiente.|
|r005|Reconhecimento|A face do usuário não foi reconhecida.|
|f001| Frequência| Nehuma frequência encontrada com os dados fornecidos.|