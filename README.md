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
