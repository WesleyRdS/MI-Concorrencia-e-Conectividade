## Modo de Uso:

Para iniciar, siga exatamente esta ordem:

### Pull da imagem do Docker Hub

1. No terminal digite o comando: `docker pull wesleyrds/broker:TAG`
2.                               `docker run -e IP=ip_da_maquina --network host -it wesleyrds/broker:TAG`
3. No terminal digite o comando: `docker pull wesleyrds/device:TAG`
4.                               `docker run -e UDP_HOST=ip_do_broker -e TCP_HOST=ip_da_maquina --network host -it wesleyrds/device:TAG`
5. No terminal digite o comando: `docker pull wesleyrds/app:TAG`
6.                               `docker run -e IP=ip_do_broker --network host -it wesleyrds/app:TAG`


### Para gerar a imagem direto no seu PC ou executar em uma IDE

Inicie o terminal no diretorio do projeto(Para a execução direto na IDE você pode executalo na pasta raiz mas para o broker você tera que acessar a subpasta de cada um onde esta localizado a `Dockerfile`):

1. Inicie o `broker.py`:
   
`a.docker buildx build -t broker .`(Cria a imagem Docker)

`docker run -e IP=ip_da_maquina --name container-broker --network host -it broker`(Cria um container a partir da imagem e o executa)

`ou`

`b.IP=ip_da_maquina python3 API_Rest/Broker/broker.py`(IDE)

2. Em seguida, inicie o `app_cliente.py`:

`a.docker buildx build -t app .`(Cria a imagem Docker)

`docker run -e IP=ip_do_broker --name container-app --network host -it app`(Cria um container a partir da imagem e o executa)

`ou`

`b.IP=ip_do_broker python3 App/Client/app_cliente.py`(IDE)

Ele retornará uma exceção caso você tente se conectar a um dispositivo inexistente. Além disso, não será executado caso o broker esteja desligado. Se uma requisição demorar 10 segundos sem receber resposta, será exibido um erro de timeout.

3. Por fim, inicie o `device_server.py`:

`a.docker buildx build -t device .`(Cria a imagem Docker)

`docker run -e UDP_HOST=ip_do_broker -e TCP_HOST=ip_da_maquina --name container-device --network host -it device`(Cria um container a partir da imagem e o executa)

`ou`

`b.UDP_HOST=ip_do_broker  TCP_HOST=127.0.0.1 python3 Devices/Simulator/device_server.py`(IDE)

No dispositivo, defina a porta. Evite usar as portas `5000, 54310 e 54020`. Defina o tipo de dispositivo entre três opções: `air, RGBlight, door`. Em seguida, defina o seu `ID`. Dispositivos com tipos e IDs ou portas iguais serão iniciados, mas não se conectarão ao broker.

**OBS**: Caso queira executar o container é necessario ter o docker instalado.

As observações a seguir só precisam ser levadas em consideração se você for compilar o codigo na IDE

**OBS**: Esse projeto usa bibliotecas externas como `Flask` e `Request`. Se não tiver instalado em seu computador o codigo não vai funcionar.

**OBS**: Esse projeto usa `match case` logo é preciso uma versão do `python` a partir da `3.10`

Comandos para instalação:

`pip install Flask`

`pip install requests`

----------------------------------------------------------------------------
# Introdução

O projeto apresenta um sistema distribuído que facilita a comunicação entre uma aplicação e diversos dispositivos simulados, proporcionando uma arquitetura distribuída eficiente e escalável. O objetivo principal é permitir que a aplicação envie requisições HTTP via API Rest para um Service Broker, que por sua vez encaminha essas requisições para dispositivos específicos usando TCP socket. Após o processamento pelo dispositivo, o Broker aguarda uma resposta via UDP socket e a retorna para a aplicação.

O projeto é composto por três principais componentes: 
- O Broker, responsável pela comunicação entre a aplicação e os dispositivos.
- A aplicação do cliente, que realiza requisições HTTP para o Broker
- As simulções de dispositivo IOT. Para esse prototipo existem três tipos de dispositivos disponiveis: Ar condicionado, Luz RGB e Porta automática.

# Tecnologias ultilizadas:

1. Python 3.12
2. Microframework flask para implementação da API
3. Bibliotecas: Socket, Request, Thread, json e os
4. Postman para o teste das rotas.

# Broker.Py

O Broker utiliza Flask para implementar uma API Rest, usando as rotas como tópicos para direcionar as requisições para os dispositivos corretos ultilizado endpoints especificos. Ele também gerencia as respostas recebidas dos dispositivos e as retorna para a aplicação cliente. Além disso, há funcionalidades como manipulação de erros e sucesso nas respostas, e métodos para obter a porta com base no ID do dispositivo.

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

## Class app

Esta classe existe principalmente para gerenciar o número de novos dispositivos de cada tipo conectados. Ela possui um parâmetro para cada tipo de dispositivo e os métodos get e set correspondentes a cada um deles. Esses métodos serão utilizados na função "device_connect", que será explicada no próximo tópico.

## device_connect

Essa função, denominada `device_connect`, tem como objetivo identificar e retornar os novos dispositivos conectados à rede. Recebendo como parâmetros uma string contendo os dados dos dispositivos conectados e uma instância da classe `app`, que fornece o número de dispositivos conectados de cada tipo. Primeiramente, a função converte a string em um dicionário utilizando a biblioteca `ast.literal_eval`. Em seguida, ela compara o número de dispositivos de cada tipo presentes no dicionário com os números previamente registrados pela instância da classe `app`. Se houver um aumento no número de dispositivos de um determinado tipo, a função atualiza o contador correspondente na instância da classe `app` e retorna uma mensagem indicando a nova conexão.

## response_receiver

Esta função utiliza o método GET para realizar uma requisição, utilizando "/response" como endpoint para obter novas conexões. Ela recebe uma instância do dispositivo como parâmetro e a utiliza para chamar a função `device_connect`, passando o dispositivo como parâmetro junto com a resposta recebida do servidor. A função armazena a resposta retornada em uma string e, caso não esteja vazia, imprime esse retorno. Ela usa um timer da threads para chamar a sí propria depois de um determinado periodo para que possa sempre detectar quando um novo dispositivo se conectar.

## handle_response

Esta função recebe como parâmetro a requisição fornecida no request. É responsável por manipular as mensagens de sucesso e erro recebidas do broker e exibi-las. Para isso, verifica o código HTTP de status da resposta. Se estiver presente, imprime que a operação foi bem-sucedida e exibe os dados retornados; se houver algum erro nos dados, indica o erro.

## app_machine

Interface responsável por lidar com as entradas do usuário e definir qual rota deve ser enviada na requisição. 

## execute

Esta função visa garantir a continuidade da execução da aplicação mesmo quando a conexão com o broker é interrompida ou se ocorre uma entrada incorreta de dados. Ela utiliza exceções para manter um loop de tentativas de interface com o usuário, permitindo que este escolha entre tentar reconectar-se ou encerrar o dispositivo em caso de falha.

Esta função é crucial para garantir a robustez da aplicação em cenários adversos, mantendo-a em funcionamento mesmo diante de desafios na conexão ou interação com o usuário.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Device_server.py

O Device_server é responsável por implementar um simulador capaz de assumir o formato de três tipos de dispositivos: Ar condicionado, Luz RGB e Porta automática. Ele também possui uma interface de terminal para interação direta com os dispositivos.

## Classe Device

Esta classe encapsula os atributos essenciais de um dispositivo, incluindo o tipo, ID, host, porta, status e os dados associados. Ela oferece o método `set_initial_params`, que ajusta dinamicamente o status e os dados dependendo do tipo de dispositivo. Além disso, disponibiliza métodos `get` e `set` para acessar e modificar esses parâmetros, seguindo o paradigma da programação orientada a objetos. O principal propósito da classe é a função `initial_send`, que constrói uma string concatenada contendo informações sobre o tipo, ID, host e porta do dispositivo, e a envia via UDP para o broker.

## handle_tcp_received

Esta função é responsável por manipular a solicitação TCP enviada pelo Broker. Recebe como parâmetros o endereço e a conexão. Inicia estabelecendo a conexão e tenta receber uma solicitação de tamanho máximo de 1024 bytes. Se não receber, a função retorna; caso contrário, transforma a mensagem em um vetor usando '/' como separador de rotas e retorna esse vetor.

## middleware_tcp_udp e access_database

Esta função desempenha um papel crucial na integração entre a recepção de requisições e o envio de respostas. Recebe como entrada os hosts e portas UDP e TCP, além do dispositivo em questão. É projetada para ser executada em uma thread. 

Inicialmente, tenta criar um socket TCP e associá-lo aos hosts e portas fornecidos, definindo um limite de 5 usuários em espera. Em seguida, entra em um loop infinito para aceitar conexões e usar o retorno dessas conexões como parâmetro para a função responsável pelo tratamento das mensagens TCP recebidas. O resultado dessa função de tratamento é então passado como argumento para a função `access_database`, juntamente com o dispositivo relevante em execução. Esta função verifica o tamanho do vetor de dados retornado e, se não estiver vazio, retorna a informação associada a esse tamanho. Se o dispositivo estiver desligado, retorna essa condição. O retorno da função `access_database` é formatado como mensagem UDP, que será enviada ao broker. Esta mensagem é transformada em uma string antes do envio. Caso a mensagem não esteja vazia, tenta-se criar um socket UDP para enviar a mensagem, fechando o socket logo em seguida. 

Em caso de exceções, como erros ou timeouts, são enviadas mensagens específicas indicando a natureza do problema encontrado durante o processamento da requisição.

## Interface

Interface de terminal para permitir que o usuário mude diretamente os dados do dispositivo sem precisar de uma aplicação.

