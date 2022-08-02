## Instituição escolhida 

**Bicharada Universitária**

A Bicharada universitária começou em 2012, com o intuito de ajudar animais abandonados dentro das dependências da Universidade Federal de Rio Grande (FURG) e bairros próximos.
Por diversos motivos, pessoas descartam animais em volta da Furg, e todos eles sofrem pela falta de alimentação e frio. E para suprimir esse mal, estudantes e funcionários se juntaram em prol desses animais abandonados.
A partir dessa premissa, a bicharada busca suprir primeiro a necessidade de alimentação desses animais, depois saúde e por último, adoção.

## Equipe
- 👩‍💻 [Ana Flávia Moraes](https://www.linkedin.com/in/ana-flavia-moraes)
- 👨‍💻 [Everton Feijó](https://www.linkedin.com/in/evertonlwf)
- 👨‍💻 [Vinicius Telles](https://www.linkedin.com/in/vinicius-telles-743155150/)
- 👩‍💻 [Suélen Peres](https://www.linkedin.com/in/suélen-peres-b91a56190/)
- 👨‍💻 [Rodrigo Valadão](https://www.linkedin.com/in/rodrigo-valadão-b38919141/)

## Tecnologias Utilizadas

[Rasa](https://rasa.com/)
[Metta for Developer](https://developers.facebook.com/) [Okteto](https://www.okteto.com/)
[Gmail](gmail.com) 
[smtplib](https://docs.python.org/3/library/smtplib.html)
[ssl](https://www.ssl.com/)


## Funcionalidades do BOT Dolly

O BOT Dolly possui cinco funcionalidades principais, são elas:

**Doação**

A Bicharada Universitária recebe muitas mensagens de pessoas que querem contribuir com seu trabalho, essas doações costumam ser em forma de ajuda financeira (envio de pix, dinheiro e/ou transferências bancárias), doação de rações, remédios, doação de roupas, agasalhos ou objetos que possam ser usados no brechó da Bicharada.

Quando um usuário passa a intenção que deseja fazer alguma doação para bicharada, Dolly irá questionar qual seria a forma de contribuição e depois em quais locais esse usuário pode levar sua colaboração. Já para os casos de doações financeiras, o usuário poderá encontrar todas as formas como pode fazer essa contribuição

**Adoção de animais**

Outra ação muito procurada é pessoas que desejam adotar algum animalzinho. Sendo assim, o usuário que chamar a Bicharada a procura de um pet, fará com que nosso BOT questione qual tipo de animal (gato ou cachorro) ele está buscando.Depois de reconhecido o tipo, a Dolly coletará os dados de contato desse usuário para repassar via e-mail para os responsáveis da bicharada.

**Resgate de animais**

A maioria das conversas da Bicharada com usuários é sobre animais que precisam de alguma ajuda. Sendo assim, quando for reconhecido algum chamado de socorro o bot irá coletar uma breve descrição do que aconteceu, perguntar informações de contato e endereço da pessoa que localizou esse animal. Depois de coletadas essas informações, a Bicharada será notificada via email, para que possa responder o quanto antes essa ocorrência.

**Colaborador**

Outra funcionalidade também projetada é para quando o usuário tem interesse em ser um voluntário no grupo. Dolly irá fazer uma pequena verificação inicial se o usuário deseja ser voluntário ou apenas um lar temporário, depois coletar nome e telefone para que um dos membros da Bicharada possa entrar em contato com essa pessoa diretamente e tirar possíveis dúvidas e explicar o funcionamento do voluntariado no grupo.

**Informações Gerais**

Por fim, a última funcionalidade é informativa. Seu objetivo é repassar informações sobre próximos eventos que a Bicharada irá participar, contar um pouco sobre a história do grupo, repassar informações de contato e até mesmo mostrar quantos animais já foram ajudados. 

## Fluxograma operacional 
![Fluxograma](https://raw.githubusercontent.com/Compass-pb-rasa-2022-RG-Pel/aubotdolly/main/assets/images/fluxograma_sprint5.png)

## Okteto

Em um primeiro momento para disponibilizar a aplicação de forma online, foi escolhido hospedar o servidor rasa no [okteto](https://www.okteto.com/). Para a configuração inicial foi necessário utilizar um arquivo docker-compose.yml e um Dockerfile para cada serviço utilizado que estão descritos abaixo.

### docker-compose.yml
```sh
version: '3.0'
services:

  bot:
    build:
      context: .
      dockerfile: ./bot/docker/Rasa.dockerfile
    container_name: rasa
    networks: 
      - rasa-network
    ports:
      - 5005:5056
    depends_on:
      - "server"
    volumes:
      - ./bot:/app
    command:
      - run
      - --enable-api
      - --cors
      - "*"
      - --debug
      - -p 5056
      - --model
      - models
      - --credentials
      - credentials.yml
  
  server:
    build:
      context: .
      dockerfile: ./bot/docker/Actions.dockerfile
    image: rasa-action-server
    container_name: actions
    networks: 
      - rasa-network
    ports:
      - "5055:5055"
    volumes:
      - "./actions:/app/actions"

networks: 
    rasa-network:
        driver: bridge
```
### Actions.dockerfile

```sh
# Utiliza a imagem rasa-sdk oficial como base
FROM rasa/rasa-sdk:3.0.2
WORKDIR /app

# Copia para o container arquivo que define as dependências externas
COPY bot/actions/requirements-actions.txt ./

# Utiliza o root user para instalar as dependências
USER root

# Instala as dependências
RUN pip install -r requirements-actions.txt

# Copia as actions para o workdir
COPY bot/actions /app/actions

# Seguindo as boas práticas não executo o código com user root
USER 1001
```

### Server.dockerfile

```sh
# Utiliza a imagem rasa oficial como base
FROM rasa/rasa:3.2.4-full

# Utiliza o root user para instalar as dependências
USER root

# Instala as dependências
RUN python -m spacy download pt_core_news_lg 

# Seguindo as boas práticas não executo o código com user root
USER 1001
```
## Integração com o [Facebook](https://www.facebook.com/)

 Para integrar os serviços do [rasa](https://rasa.com/) hospedados no [okteto](https://www.okteto.com/) foi necessário realizar alguns passos na plataforma de desenvolvedores da [meta](https://developers.facebook.com/?locale=pt_BR), seguindo a documentação do [rasa-facebook-messenger](https://rasa.com/docs/rasa/connectors/facebook-messenger/) que serão descritos abaixo:

1 -  Para criar o aplicativo, acesse o [Facebook For Develop](https://developers.facebook.com/) e clique em Meus aplicativos → Adicionar novo aplicativo .
2 - Vá para o painel do aplicativo e, em Produtos , encontre a seção Messenger e clique em Configurar . Role para baixo até Token Generation e clique no link para criar uma nova página para seu aplicativo.
3 - Crie sua página e selecione-a no menu suspenso para Geração de Token . O token de acesso à página mostrado é o page-access-token necessário mais tarde.
4 - Localize o App Secret no painel do aplicativo em Configurações → Básico . Este será o seu secret.
Use o coletado secrete page-access-token no seu credentials.yml, e adicione um campo chamado verify contendo uma string de sua escolha. Comece rasa run com a --credentials credentials.ymlopção.
5 - Configure um Webhook e selecione pelo menos as assinaturas messaging e messaging_postback . Insira seu URL de retorno de chamada, que se parecerá com https://<host>:<port>/webhooks/facebook/webhook, substituindo o host e a porta pelos valores apropriados do servidor Rasa Open Source em execução.
6 - Insira o token de verificação que deve corresponder à verify entrada em seu arquivo credentials.yml.

## Exemplos de Funcionamento
  
### Adoção
  
![adoção de um gato](https://github.com/EvertonLWF/sprint-5-pb-rg-pel/blob/master/assets/images/Captura%20de%20tela%20de%202022-07-28%2016-29-51.png?raw=true)
  
![adoção de um cão, com pergunta sobre o porte](https://github.com/EvertonLWF/sprint-5-pb-rg-pel/blob/master/assets/images/Captura%20de%20tela%20de%202022-08-01%2016-14-33.png?raw=true)
  
### Doação
  
![doacão de ração](https://github.com/EvertonLWF/sprint-5-pb-rg-pel/blob/master/assets/images/Captura%20de%20tela%20de%202022-07-28%2016-16-42.png?raw=true)
  
![respostas para doacoes](https://github.com/EvertonLWF/sprint-5-pb-rg-pel/blob/master/assets/images/Captura%20de%20tela%20de%202022-07-28%2016-16-49.png?raw=true)
  
### Resgate
  
![animal que precisa de resgate](https://github.com/EvertonLWF/sprint-5-pb-rg-pel/blob/master/assets/images/Captura%20de%20tela%20de%202022-08-01%2015-14-51.png?raw=true)
  
![armazenando contato para resgate](https://github.com/EvertonLWF/sprint-5-pb-rg-pel/blob/master/assets/images/Captura%20de%20tela%20de%202022-08-01%2015-16-04.png?raw=true)
  
### Voluntário
  
![cadastro de voluntarios](https://github.com/EvertonLWF/sprint-5-pb-rg-pel/blob/master/assets/images/Captura%20de%20tela%20de%202022-08-01%2015-20-53.png?raw=true)
  
### Informações
  
![informações sobre a ONG](https://github.com/EvertonLWF/sprint-5-pb-rg-pel/blob/master/assets/images/Captura%20de%20tela%20de%202022-08-01%2015-21-25.png?raw=true)
  
![uma das respostas automaticas de informações](https://github.com/EvertonLWF/sprint-5-pb-rg-pel/blob/master/assets/images/Captura%20de%20tela%20de%202022-08-01%2015-24-03.png?raw=true)
  
### Continuar conversa ou sair    
  
![pergunta por uma nova questão](https://github.com/EvertonLWF/sprint-5-pb-rg-pel/blob/master/assets/images/Captura%20de%20tela%20de%202022-08-01%2015-13-21.png?raw=true) 
  
## Observações Gerais 

 **Mongo DB**

Nesse projeto optamos por não utilizar um banco de dados, uma vez que não foi apresentada necessidade por parte da ONG de realizar buscas ou manter dados antigos, sendo boa parte das principais informações necessárias de caráter temporário. além disso o próprio aplicativo de conversa do facebook já mantém o registro das informações necessárias para ONG e os dados recebidos através do bot não são utilizados em outras aplicações para que fosse essencial a utilização de um banco de dados.

**Facebook**

O Messenger do Facebook foi escolhido por necessidade da ONG, uma vez que eles não possuem um único responsável  para outras plataformas de conversa como o WhatsApp e o Telegram, tornando problemático para eles criar um WhatsApp ou Telegram onde todos envolvidos tivessem acesso às conversas. A primeiro momento foi informado à nossa equipe que recebem mais conversas através do Messenger do Instagram, porém no momento não existe uma aplicação própria para o Messenger do Instagram, tornando o Facebook a melhor opção.
## Dificuldades encontradas
* Primeiramente, usamos as entidades do Spacy para nossos slots, porém o bot tinha muita dificuldade para reconhecer quase nada passado nos testes. Para contornar essa situação optamos em não usar as entidades do spacy, removendo do arquivo config.yml a linha:
    - _name: SpacyEntityExtractor_

* As intents _info_contato_ e _info_local_  são utilizadas por mais de uma funcionalidade, desta forma, o bot se perdia e não conseguia distinguir de qual funcionalidade estava invocando tais intents. O bot costuma buscar o primeiro aparecimento delas nos stories e seguir o fluxo da conversa a partir daí. Como solução, usamos os botões para definir os valores de entidades e o uso das _rules_ para lidar com tais intents e assim validá-las nos actions quando necessário.

* O  bot funciona tranquilamente com o uso dos botões, porém tivemos que construir uma abordagem para os casos de o usuário não usá-los. Nos primeiros testes em que eram passados frases inteiras, o bot até conseguia localizar em qual funcionalidade ele deveria acessar, porém os botões sempre quando acionados preenchiam as entidades dos seus respectivos formulários, ou seja, quando o usuário não usava os botões, ele chama as utters para preencher as entidades dos formulários e isso quebrava o fluxo da conversa. Para contornar esse problema, tivemos que criar outras _forms_ e administrar as entidades de cada funcionalidade, assim o bot conseguia facilmente se encontrar e solicitar apenas o que falta para preencher as entidades. Depois disso, tivemos que fazer o tratamento dos slots relacionados a essas entidades nas _actions_ através de um vetor de sinônimos, para que ele sempre mostrasse o fluxo de conversa adequado ao usuário. 

* O BOT Dolly faz o envio de email em alguns momentos da conversa para notificar alguém da Bicharada de que algo precisa da atenção deles. Na configuração dos envios dos email pelo Gmail, tivemos um barramento do próprio Google. Desde  30 de maio de 2022, o Google não autoriza mais o uso de apps ou dispositivos de terceiros que exigem apenas nome de usuário e senha para fazer login na Conta do Google, sendo assim, mesmo que nosso app estivesse devidamente configurado, a Google impedia o acesso ao gmail criado. Para contornar essa questão, seguindo orientação do youtuber _Lira da Hastag_, criamos uma senha de verificação dentro da conta do Google do bot, e nas configurações do envio nas actions, fornecemos essa senha para que o Google liberasse o acesso ao nosso app.

* Algumas vezes nosso bot simplesmente, sem ninguém ter modificado o código, parava de funcionar sem nenhuma explicação. Notamos que esse problema acontecia quando fazíamos o _git clone_ de alguma _branch_. Tivemos que fazer o download da branch e abrir diretamente no VS Code.  

## Próximos passos 

Baseado na estrutura pensada inicialmente para o BOT Dolly, o projeto está totalmente funcional. Entretanto, como visamos das seguimento e manutenção a ele, em um outro momento temos a ideia de anexar outra função que seria o encaminhamento do usuário que está utilizando o bot diretamente com a direção ou gerenciador da página da bicharada para que possa ter o diálogo direto na conversa sem comprometer a funcionalidade do bot, assim sendo criado uma funcionalidade onde a pessoa contribuinte terá um recurso para caso queira ser encaminhado para o atendimento humano caso não consiga pelo menu de opções do bot.
