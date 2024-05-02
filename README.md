## Modo de Uso:

Para iniciar, siga exatamente esta ordem:

No diretorio do projeto:

1. Inicie o `broker.py`:

`python3 API_Rest/Broker/broker.py`

2. Em seguida, inicie o `app_cliente.py`:

`python3 App/Client/app_cliente.py`

Ele retornará uma exceção caso você tente se conectar a um dispositivo inexistente. Além disso, não será executado caso o broker esteja desligado. Se uma requisição demorar 10 segundos sem receber resposta, será exibido um erro de timeout.

3. Por fim, inicie o `device_server.py`:

`python3 Devices/Simulator/device_server.py`

No dispositivo, defina a porta. Evite usar as portas `5000, 54310 e 54020`. Defina o tipo de dispositivo entre três opções: `air, RGBlight, door`. Em seguida, defina o seu `ID`. Dispositivos com tipos e IDs ou portas iguais serão iniciados, mas não se conectarão ao broker.

**OBS**: O `Dockerfile` está definido, mas ainda não está funcionando corretamente.

**OBS**: Esse projeto usa bibliotecas externas como `Flask` e `Request`. Se não tiver instalado em seu computador o codigo não vai funcionar.

**OBS**: Esse projeto usa `match case` logo é preciso uma versão do `python` a partir da `3.10`

Comandos para instalação:

`pip install Flask`

`pip install requests`

----------------------------------------------------------------------------
# Broker.Py

O Broker é um middleware que implementa uma API Rest utilizando Flask. Ele recebe requisições HTTPS e as encaminha para um dispositivo específico via TCP socket. O dispositivo é selecionado com base nos endpoints da requisição. O Broker aguarda uma resposta via UDP socket e a envia de volta para a aplicação.

## Classe TCP_SEND

Esta classe foi criada com o objetivo de facilitar a criação de múltiplas conexões. Possui como atributos o IP do host, a porta e o estado de conexão. Contém dois métodos: `connect` e `send_request`. O método `connect`, como o nome sugere, tenta criar um socket TCP e conectar à porta e ao host passados como parâmetro. Em caso de falha, uma mensagem de erro é exibida. O método `send_request` recebe uma mensagem como parâmetro, verifica se o broker está conectado e envia a mensagem para o cliente.

## connect_continuous e DB_refactor

Esta função permanece aguardando uma resposta dos dispositivos conectados a ela o tempo todo. É utilizada principalmente para receber a comunicação inicial quando um dispositivo se conecta a ela e atualizar o banco de dados. Inicia-se em uma thread, recebendo o host como parâmetro e utilizando a porta 54020. A mensagem recebida é transformada em um vetor e separada em três possíveis tipos: conexão com ar condicionado, conexão com luz RGB ou conexão com uma porta automática. Esse vetor, junto com outro parâmetro, é passado para a função `DB_refactor`. Esta função verifica o tipo de dispositivo da mensagem e itera sobre o vetor de dispositivos referente a esse dispositivo. Verifica se o ID do dispositivo é igual ao ID do vetor passado na mensagem e se a tupla de host e porta da mensagem equivale à do dispositivo passado. Caso uma dessas opções seja verdadeira, a execução da função é encerrada; caso contrário, ao final, o dispositivo é adicionado ao vetor de dispositivos daquele tipo. Ao final da função `connect_continuous`, é obtido o caminho absoluto da pasta e adicionado o nome do arquivo. Se o arquivo existir e tiver tamanho maior ou igual a zero, ele cria o arquivo JSON e define seu formato; caso contrário, sobrescreve o arquivo no vetor do dispositivo correto.

## udp_server

Esta função serve para receber as respostas UDP dos dispositivos às requisições TCP feitas anteriormente. Fica aguardando por 10 segundos; se receber uma resposta dentro desse tempo, retorna essa resposta; caso contrário, retorna uma mensagem de estouro de tempo.

## success_response e error_response

São funções de resposta HTTP que recebem um parâmetro. Na função de resposta de sucesso, verifica-se a existência dos dados e retorna um dicionário JSON com os pares chave-valor de status "success" e os dados solicitados, além do código de sucesso 200. Na função de erro, o parâmetro é uma mensagem de erro que é retornada com status de erro e a própria mensagem de erro. O `jsonify` é responsável pela criação do dicionário JSON.

## get_port_by_id

Esta função obtém a porta a partir do dicionário de dispositivos, utilizando o tipo e o ID do dispositivo para fazer a busca. Primeiro, verifica-se o tipo de dispositivo e, em seguida, itera-se sobre a lista desse tipo até encontrar o dispositivo com o ID correspondente. Em seguida, retorna-se a tupla de host e porta.


## Tópicos/Rotas

Este serviço de Broker utiliza as rotas fornecidas pelo Flask como tópicos. Essas rotas usam os endpoints como parâmetros para que o dispositivo que recebe a solicitação possa saber qual ação tomar. Existem rotas para respostas gerais, dispositivos de ar condicionado, luz RGB e portas. Nesta API Rest, só foi necessário o uso dos métodos GET para obtenção de valores e PATCH para alteração. Os tópicos de dispositivos, ou seja, suas rotas, seguem sempre a mesma lógica: ler um arquivo JSON com a função `ler_json` e armazenar o dicionário lido numa variável. Esta variável é passada como parâmetro da função `get_port_by_id`, juntamente com os outros parâmetros necessários, já mencionados anteriormente. A tupla retornada é utilizada para iniciar a classe `TCP_SEND` e estabelecer comunicação com o dispositivo, enviando a requisição para o mesmo. Tenta-se receber uma resposta; se obtida, utiliza-se a função de resposta bem-sucedida para enviá-la; caso contrário, envia-se uma mensagem de dados não recebidos utilizando a função de erro `response`. Em caso de falha, indica-se um erro de índice caso o ID do dispositivo seja inválido ou um erro de tempo de resposta caso exceda o limite máximo.

-----------------------------------------------------------------------------

# app_cliente.py

Este arquivo implementa a aplicação do cliente responsável por fazer requisições HTTP para o broker. Ele importa a biblioteca `requests` do Python e utiliza o localhost na porta 5000, que é o padrão do Flask. Como mencionado anteriormente, no Broker, apenas os métodos GET e PATCH são necessários para a API REST. Todos os requests seguem o mesmo padrão de chave: a URL base, seguida pelo tipo de dispositivo e o ID do dispositivo desejado. Essa é a chave para obter cada item do banco de dados. Para se inscrever nos "tópicos", são necessários alguns endpoints além da chave padrão. No caso de ligar e desligar o ar ou a luz, é necessário adicionar "/on" ou "/off" a essa chave, respectivamente, e para a porta serial, "open" ou "close". Neste caso, é utilizado o método PATCH. Especificamente para a luz RGB e o ar condicionado, o método GET é utilizado para obter a cor e a temperatura dos dispositivos mencionados, respectivamente. Para o ar, é necessário adicionar "/temperature" e para a luz, "/color". Se ainda for necessário alterar o valor da temperatura ou mudar a cor, adiciona-se mais um endpoint com um "/", seguido do valor da temperatura (inteiro) ou cor desejada, respectivamente. Novamente, neste caso, é utilizado o método PATCH. Isso resume o formato de todas as requisições possíveis de serem utilizadas.

## response_receiver

Esta função utiliza o método GET para fazer uma requisição, passando como endpoint "/response", um tópico para uma resposta genérica fora das respostas padrões. É iniciado com uma thread e é usado para indicar que um novo dispositivo está disponível.

## handle_response

Esta função recebe como parâmetro a requisição fornecida no request. É responsável por manipular as mensagens de sucesso e erro recebidas do broker e exibi-las. Para isso, verifica o código HTTP de status da resposta. Se estiver presente, imprime que a operação foi bem-sucedida e exibe os dados retornados; se houver algum erro nos dados, indica o erro.

## app_machine

Interface responsável por lidar com as entradas do usuário e definir qual rota deve ser enviada na requisição.
-----------------------------------------------------------------------------

# Device_server.py

O Device_server é responsável por implementar um simulador capaz de assumir o formato de três tipos de dispositivos: Ar condicionado, Luz RGB e Porta automática.

## Classe Device

Esta classe contém os atributos do tipo de dispositivo, ID, host, porta, status e os dados de retorno. Além disso, possui as funções `set_initial_params`, que verifica o tipo de dispositivo e modifica o tipo de status apresentado e os dados retornados, bem como as funções `get` e `set` para obter e alterar os parâmetros, como é comum em programação orientada a objetos. A função principal da classe é `initial_send`, que concatena as informações de tipo, ID, host e porta em uma string e envia por UDP para o broker.

## handle_tcp_received

Esta função é responsável por manipular a solicitação TCP enviada pelo Broker. Recebe como parâmetros o endereço e a conexão. Inicia estabelecendo a conexão e tenta receber uma solicitação de tamanho máximo de 1024 bytes. Se não receber, a função retorna; caso contrário, transforma a mensagem em um vetor usando '/' como separador de rotas e retorna esse vetor.

## middleware_tcp_udp e access_database

Essa função integra a obtenção da requisição com o envio da resposta. Recebe como parâmetros os hosts e portas UDP e TCP e o dispositivo em questão. É executada em uma thread. Começa tentando criar um socket TCP e associando-o às portas passadas, definindo o limite de 5 usuários em espera. Em seguida, há um loop infinito que pega essa conexão e usa seu retorno como parâmetro da função que manipula o recebimento de mensagens TCP. O retorno dessa função se torna parâmetro para a função `access_database`, juntamente com o dispositivo em execução. Esta função verifica o tamanho do vetor de dados e retorna a informação associada àquele tamanho, ou então, caso o dispositivo esteja desligado, retorna esse fato. Esse retorno é a mensagem UDP que será enviada ao broker. A mensagem é transformada em string, e se não estiver vazia, tenta criar o socket e envia essa string, fechando o socket logo depois. Caso ocorram exceções de erro e timeout, são enviadas mensagens específicas caso os dados não venham da forma esperada.

## Interface

Interface de terminal para permitir que o usuário mude diretamente os dados do dispositivo sem precisar de uma aplicação.

