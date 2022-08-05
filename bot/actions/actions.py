# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from unicodedata import name
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
import requests
import os
from dotenv import load_dotenv
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ActionOption(Action):
    def name(self) -> Text:
        return "action_option"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        option = tracker.get_slot("type_option")
        print(option)
        if option != 'doacao' and option != 'adocao' and option != 'resgate' and option != 'colaborador' and option != 'informacoes':
            doacao = ['doacao','DOACAO','doação','DOAÇÃO','Doação','doações','DOAÇÕES','ração','remedio','roupas',
            'brechó','ajudar','pix day','vakinha','RAÇÃO','REMEDIO','ROUPAS','BRECHÓ','AJUDAR','PIX DAY',
            'VAKINHA','remédios','REMÉDIOS','Medicamentos','doar','doa','Ração','camisas','calças','cobertas',
            'agasalhos','MEDICAMENTOS','DOAR','DOA','RAÇÃO','CAMISAS','CALÇAS','COBERTAS','AGASALHOS']

            voluntario = ['voluntario','voluntário','Voluntário','voluntária','voluntaria','Voluntária','lar temporário','Lar temporário','Lar Temporário','lar solidário','lar temporario','lar solidario','voluntariado','VOLUNTARIO','VOLUNTÁRIO','VOLUNTÁRIO','VOLUNTÁRIA','VOLUNTARIA','VOLUNTÁRIA','LAR TEMPORÁRIO','LAR TEMPORÁRIO','LAR TEMPORÁRIO','LAR SOLIDÁRIO','LAR TEMPORARIO','LAR SOLIDARIO','VOLUNTARIADO']
            lar_temp = ['lar','LAR','Lar','Lartemporario']
            resgate = ['atropelado','perdido','mal','desnutridos','abandonados','judiados','sangrando','quebrada','quebrado','bicheira','resgate','ATROPELADO','PERDIDO','MAL','DESNUTRIDOS','ABANDONADOS','JUDIADOS','SANGRANDO','QUEBRADA','QUEBRADO','BICHEIRA','RESGATE']
            adocao = ['adotar','adoção','adocao','Adotar','Adoção','Adocao','ADOTAR','ADOÇÃO','ADOCAO','ADOTAR','ADOÇÃO','ADOCAO','porte','Porte','PORTE','Pequeno','pequeno','PEQUENO','Médio','Medio','medio','médio','MÉDIO','mediano','pequenininho','grandão','Grande','grande','GRANDE','p','m','g','P','M','G']
            informacao = ['informação','informações','informacao','informacoes']

            temp= option.split(' ')
            for x in temp:
                if x in doacao:
                    option = 'doacao'
                    break
                if x in voluntario:
                    option = 'voluntario'
                    break
                if x in lar_temp:
                    option = 'lar_temporario'
                    break
                if x in adocao:
                    option = 'adocao'
                    break
                if x in resgate:
                    option = 'resgate'
                    break
                if x in informacao:
                    option = 'informacoes'
                    break

        if option == 'doacao':
            dispatcher.utter_message(response="utter_type_donation")
        elif option == 'adocao':
            dispatcher.utter_message(response="utter_adoption_type")
            dispatcher.utter_message(response="action: info_usuario_form")
            dispatcher.utter_message(response="active_loop: info_usuario_form")
        elif option == 'resgate':
            dispatcher.utter_message(response="utter_ask_description_form")
        elif option == 'colaborador':
            dispatcher.utter_message(response="utter_collaboration")
        elif option == 'informacoes':
            dispatcher.utter_message(response="utter_information")

        print(f"Opção escolhida {option}")

        return [SlotSet("type_option", None)]

class ActionInformUser(Action):
    def name(self) -> Text:
        return "action_informacao"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Quando o usuário precisar falar seu nome e telefone, fazer a validação aqui
        acao = tracker.get_slot("informacao_usuario")
        print(acao)

        if acao == 'lar_temporario':
            dispatcher.utter_message(response="utter_goodbye_voluntario")
            dispatcher.utter_message(response="utter_return_choice")
        elif acao == 'voluntario':
            dispatcher.utter_message(response="utter_goodbye_voluntario")
            dispatcher.utter_message(response="utter_return_choice")
        elif acao == 'resgate':
            dispatcher.utter_message(response="utter_informe_resgate")
            dispatcher.utter_message(response="utter_return_choice")
        elif acao == 'adocao':
            dispatcher.utter_message(response="utter_esclarece_adocao")
            dispatcher.utter_message(response="utter_return_choice")

        return [SlotSet("informacao_usuario", None)]

class ActionEmail(Action):
    def name(self) -> Text:
        return "action_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        option = tracker.get_slot("informacao_usuario")
        description = tracker.get_slot("description_form")
        address = tracker.get_slot("address_form")        
        contact = tracker.get_slot("contact_form")
        
        print("OPTION =",option)
        print("USER_INFO =", contact) # nome e telefone
        print("DESCRIPTON =", description)
        print("ADDRESS =", address)

        if option == None and description != None:
            dispatcher.utter_message(response="utter_goodbye_resgate")
            dispatcher.utter_message(response="utter_return_choice")
            sendEmail('resgate', description, contact, address)

        if option == 'resgate':
            dispatcher.utter_message(response="utter_informe_resgate")
            dispatcher.utter_message(response="utter_goodbye_resgate")
            dispatcher.utter_message(response="utter_return_choice")
            sendEmail(option, description, contact, address)
        elif option == 'adocao':
            dispatcher.utter_message(response="utter_esclarece_adocao")
            dispatcher.utter_message(response="utter_return_choice")
            sendEmail(option, description, contact, address)
        elif option == 'voluntario':
            dispatcher.utter_message(response="utter_goodbye_voluntario")
            dispatcher.utter_message(response="utter_return_choice")
            sendEmail(option, description, contact, address)
        elif option == 'lar_temporario':
            dispatcher.utter_message(response="utter_goodbye_voluntario")
            dispatcher.utter_message(response="utter_return_choice")
            sendEmail(option, description, contact, address)
        elif option == 'doacao':
            sendEmail(option, description, contact, address)

        return [SlotSet("type_option", None), SlotSet("contact_form", None), SlotSet("description_form", None), SlotSet("address_form", None)]

class ActionEmailEscrita(Action):
    def name(self) -> Text:
        return "action_escrita_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        description = tracker.get_slot("description_escrita")
        descricao = tracker.get_slot("description_form")
        address = tracker.get_slot("address_form")        
        contact = tracker.get_slot("contact_form")
        option = ''
        
        doacao = ['doacao','DOACAO','doação','DOAÇÃO','Doação','doações','DOAÇÕES','ração','remedio','roupas',
            'brechó','ajudar','pix day','vakinha','RAÇÃO','REMEDIO','ROUPAS','BRECHÓ','AJUDAR','PIX DAY',
            'VAKINHA','remédios','REMÉDIOS','Medicamentos','doar','doa','Ração','camisas','calças','cobertas',
            'agasalhos','MEDICAMENTOS','DOAR','DOA','RAÇÃO','CAMISAS','CALÇAS','COBERTAS','AGASALHOS']

        voluntario = ['voluntario','voluntário','Voluntário','voluntária','voluntaria','Voluntária','lar temporário','Lar temporário','Lar Temporário','lar solidário','lar temporario','lar solidario','voluntariado','VOLUNTARIO','VOLUNTÁRIO','VOLUNTÁRIO','VOLUNTÁRIA','VOLUNTARIA','VOLUNTÁRIA','LAR TEMPORÁRIO','LAR TEMPORÁRIO','LAR TEMPORÁRIO','LAR SOLIDÁRIO','LAR TEMPORARIO','LAR SOLIDARIO','VOLUNTARIADO']
        lar_temp = ['lar','LAR','Lar','Lartemporario']
        adocao = ['adotar','adoção','adocao','Adotar','Adoção','Adocao','ADOTAR','ADOÇÃO','ADOCAO','ADOTAR','ADOÇÃO','ADOCAO']

        temp=''
        if description != None:
            temp = description.split(' ')
        else:
            temp = descricao.split(' ')
            description = descricao

        for x in temp:
            if x in doacao:
                option = 'doacao'
                break
            if x in voluntario:
                option = 'voluntario'
                break
            if x in lar_temp:
                option = 'lar_temporario'
                break
            if x in adocao:
                option = 'adocao'
                break
            
       
        print("OPTION =",option)
        print("USER_INFO =", contact) # nome e telefone
        print("DESCRIPTON =", description)
        print("ADDRESS =", address)

        if option == None and description != None:
            description = "Gostaria de contribuir com ajuda financeira"
            dispatcher.utter_message(response="utter_explain_donation")
            dispatcher.utter_message(response="utter_thanks_donation")
            dispatcher.utter_message(response="utter_return_choice")
            sendEmail('doacao', description, contact, address)

        if option == 'resgate':
             dispatcher.utter_message(response="utter_informe_resgate")
             dispatcher.utter_message(response="utter_goodbye_resgate")
             dispatcher.utter_message(response="utter_return_choice")
             sendEmail(option, description, contact, address)
        elif option == 'adocao':
             dispatcher.utter_message(response="utter_esclarece_adocao")
             dispatcher.utter_message(response="utter_return_choice")
             sendEmail(option, description, contact, address)
        elif option == 'voluntario':
            dispatcher.utter_message(response="utter_goodbye_voluntario")
            dispatcher.utter_message(response="utter_return_choice")
            sendEmail(option, description, contact, address)
        elif option == 'lar_temporario':
            dispatcher.utter_message(response="utter_goodbye_voluntario")
            dispatcher.utter_message(response="utter_return_choice")
            sendEmail(option, description, contact, address)
        elif option == 'doacao':
            sendEmail(option, description, contact, address)

        return [SlotSet("type_option", None), SlotSet("contact_form", None), SlotSet("description_escrita", None), SlotSet("address_form", None)]

def sendEmail(assunto, descricao, contato, endereco):
    message = MIMEMultipart("alternative")   
    models = {
        "resgate": f"""\
            
            Olá AUmigos da Bicharada, aqui é a Dolly o BOT para mensagens recebidas no Facebook.

            Venho através desse e-mail avisar que foi recebido um novo PEDIDO DE AJUDA!
            Separei algumas informações importantes para você:

                📝 Descrição: {descricao}
                ☎️ Contato de quem informou a ocorrência: {contato}
                🏠 Endereço: {endereco}

            Espero ter ajudado, com carinho,
            Dolly.

       """,
        "adocao":f"""\
            Olá AUmigos da Bicharada, aqui é a Dolly o BOT para mensagens recebidas no Facebook.

            Venho através desse e-mail avisar que foi recebido um novo contato para ADOÇÕES DE ANIMAIS
            Separei algumas informações importantes para você:

                📝 Descrição: {descricao}
                ☎️ Contato de quem informou a ocorrência: {contato}
                🏠 Endereço: {endereco}


            Espero ter ajudado, com carinho,
            Dolly.
        
        """,
        "lar_temporario": f"""\
            Olá AUmigos da Bicharada, aqui é a Dolly o BOT para mensagens recebidas no Facebook.

            Venho através desse e-mail avisar que foi recebido um novo contato para novos voluntários
            Separei algumas informações importantes para você:

                📝 Descrição: {descricao}
                ☎️ Contato de quem informou a ocorrência: {contato}

            Espero ter ajudado, com carinho,
            Dolly.
            """,
        "voluntario": f"""\
            Olá AUmigos da Bicharada, aqui é a Dolly o BOT para mensagens recebidas no Facebook.

            Venho através desse e-mail avisar que foi recebido um novo contato para novos voluntários
            Separei algumas informações importantes para você:

                📝 Descrição: {descricao}
                ☎️ Contato de quem informou a ocorrência: {contato}

            Espero ter ajudado, com carinho,
            Dolly.
            """,
        "doacao": f"""\
            Olá AUmigos da Bicharada, aqui é a Dolly o BOT para mensagens recebidas no Facebook.

            Venho através desse e-mail avisar que foi recebido um novo contato para doações
            Separei algumas informações importantes para você:

                📝 Descrição: {descricao}

            Espero ter ajudado, com carinho,
            Dolly.
            """
    }
                  
    From = 'aubotdolly@gmail.com'
    To = 'anaflavia.chamoraes@gmail.com'
    ## Lendo arquivo .env
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')       
    load_dotenv(dotenv_path)
    PSK = os.getenv("PSK")

    message["Subject"] = assunto
    message["From"] = From
    message["To"] = To

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(models[assunto], "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

     #Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(From, PSK)
        server.sendmail(
           From, To, message.as_string()
        )

    print(models[assunto])
