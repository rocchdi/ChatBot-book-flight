#On définit un dialogue de bot intitulé CreateBookingDialog en utilisant la bibliothèque BotBuilder pour Python.
# Le dialogue permet à un utilisateur de fournir une description de vol et utilise une API LUIS pour comprendre l'intention
# de l'utilisateur et les détails du vol. Le code importe des classes nécessaires à partir de la bibliothèque BotBuilder
# pour définir les étapes du dialogue (WaterfallDialog), les boîtes de dialogue pour demander des informations
# à l'utilisateur (TextPrompt, ChoicePrompt, ConfirmPrompt), les messages à envoyer à l'utilisateur (MessageFactory),
# et le traitement des données LUIS (extract_luis_info). Le code utilise également un objet de journalisation pour enregistrer
# des informations sur les activités du bot.



from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt, ConfirmPrompt
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints

#from botbuilder.ai.luis import LuisApplication,LuisPredictionOptions,LuisRecognizer

from .completebooking_dialog import completeBookingDialog

from config import DefaultConfig
#from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
#from msrest.authentication import CognitiveServicesCredentials

import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
#from opencensus.ext.azure.log_exporter import AzureEventHandler


import string
import random
 

import luisApp


 
CONFIG = DefaultConfig()



logger = logging.getLogger(__name__)
#logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=28845d90-dbbe-4a5a-826b-6fb138c8c9e7'))
#logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=f0155c77-7588-4c00-a385-525862c02a00'))
logger.addHandler(AzureLogHandler(connection_string=f'InstrumentationKey={CONFIG.INSIGHT_INSTRUMENT_KEY}'))

#logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)




def extract_luis_info(luis_output):
    result = {}
    result['intent'] = luis_output['topScoringIntent']['intent']
    for entity in luis_output['entities']:
        result[entity['type']] = entity['entity']
    return result






class CreateBookingDialog(ComponentDialog):
    def __init__(self, completebooking_dialog: completeBookingDialog, dialog_id:str = None):
        super(CreateBookingDialog, self).__init__(dialog_id or CreateBookingDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))

        self._completebooking_dialog_id = completebooking_dialog.id
        self.add_dialog(completebooking_dialog)

        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [self.demand_step, self.luis_step, self.completebooking_step, self.summary_step, self.confirmation_step]
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def demand_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        message_text = "Please provide your flight description..."
        logger.info("Bot ---> Please provide your flight description...")
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input)
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    
    async def luis_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options
        user_id = user_details.user_id
        booking_desc = str(step_context.result)

        user_details.bookings_list = dict()

        # Luis configuration
         
        
        data = luisApp.getLuisResponse(booking_desc)
        print(data)
        logger.info(f"user --> : {booking_desc}")

        results = extract_luis_info(data)
        intent = results['intent']
        print(results)
        #properties = {"custom_dimensions": {"function": 'luisApp', 'Luis results': results}}
        #logger.info("createbookingdialog.py : ", extra=properties)


        #Greetings  : Hello phrases
        if (booking_desc.lower() =="hello")  \
                or not(booking_desc.lower().find("how are") == -1) \
                or not(booking_desc.lower().find("morning") == -1) \
                or not(booking_desc.lower().find("good") == -1) \
                or not(booking_desc.lower().find("bye") == -1):  
            msg_text = "Happy to serve you!"
            logger.info("Happy to serve you!")
            msg = MessageFactory.text(
                msg_text, msg_text, InputHints.ignoring_input
            ) 
            await step_context.context.send_activity(msg)
            return await step_context.end_dialog() 
        elif not(booking_desc.lower().find("your name") == -1) or not(booking_desc.lower().find("are") == -1) or not(booking_desc.lower().find("a bot") == -1): #intent for identity
            msg_text = "I am an AI language model Bot created by FlyMe, trained on a diverse range of intents and flight booking descriptions to help you book your flight...."
            logger.info("Bot --> : I am an AI language model Bot created by FlyMe, trained on a diverse range of intents and flight booking descriptions to help you book your flight....")
            msg = MessageFactory.text(
                msg_text, msg_text, InputHints.ignoring_input
            ) 
            await step_context.context.send_activity(msg)
            return await step_context.end_dialog()
        elif not(booking_desc.lower().find("i love") == -1) \
                    or not(booking_desc.lower().find("i like") == -1) \
                    or not(booking_desc.lower().find("you") == -1) \
                    or not(booking_desc.lower().find("what") == -1): #intent hors contexte
            msg_text = "I do not understand your request, This is a Flight Booking bot!"
            logger.info("Bot --> : I do not understand your request, This is a Flight Booking bot!")
            logger.error("Bad answer!")
            msg = MessageFactory.text(
                msg_text, msg_text, InputHints.ignoring_input
            ) 
            await step_context.context.send_activity(msg)
            return await step_context.end_dialog()  
        elif intent == "BookFlight":
            #check missing entities
            if 'or_city' in results:
                user_details.bookings_list.update({"or_city": results['or_city']})
            if 'dst_city' in results:
                user_details.bookings_list.update({"dst_city": results['dst_city']})
            if 'str_date' in results:
                user_details.bookings_list.update({"str_date": results['str_date']})
            if 'end_date' in results:
                user_details.bookings_list.update({"end_date": results['end_date']})
            if 'budget' in results:
                user_details.bookings_list.update({"budget": results['budget']})
        else:
            msg_text = "I do not understand your request, This is a Flight Booking bot !"
            logger.info("Bot --> : I do not understand your request, This is a Flight Booking bot !")
            msg = MessageFactory.text(
                msg_text, msg_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(msg)
            return await step_context.end_dialog()

  
            
        return await step_context.next(user_details)




    #ask for missing entities
    async def completebooking_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options

        if len(user_details.bookings_list) < 5:
            return await step_context.begin_dialog(self._completebooking_dialog_id, user_details)
        
        else:
            user_details.entities = user_details.bookings_list
            return await step_context.next(user_details)






    async def summary_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        user_details = step_context.options
        results = user_details.entities
 
        print("print the complete entities:")
        or_city = results['or_city']
        dst_city = results['dst_city']
        str_date = results['str_date']
        end_date = results['end_date']
        budget = results['budget']
        print(or_city, " ", dst_city, " ", str_date, " ", end_date, " ", budget) 

        
        # Confirm booking details with user
        msg_text = (f"You would like to book a flight from {or_city} to {dst_city} on the {str_date} returning {end_date} with a budget of {budget} : Please Confirm")

        logger.info(f"Bot --> : You would like to book a flight from {or_city} to {dst_city} on the {str_date} returning {end_date} with a budget of {budget} : Please Confirm")
        print(f"Booking summary : flight from {or_city} to {dst_city} on the {str_date} returning {end_date} with a budget of {budget} : Please Confirm")

         

        msg = MessageFactory.text(
            msg_text, msg_text, InputHints.ignoring_input
        )
        await step_context.context.send_activity(msg)
        
        # Offer a YES/NO prompt.
        return await step_context.prompt(ConfirmPrompt.__name__, PromptOptions(prompt=MessageFactory.text(msg)))


        #return await step_context.next(user_details)




    async def confirmation_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        #generate booking id
        N = 4
        booking_id = ''.join(random.choices(string.digits, k= N))
        booking_id = 'ord' + booking_id

        response = step_context.result
        if response:
            msg_text = ("Your flight booking is confirmed, your Booking number is : " + booking_id)
            logger.info(f"Bot --> : Your flight booking is confirmed, your Booking number is : {booking_id}")
            msg = MessageFactory.text(msg_text, msg_text, InputHints.ignoring_input)
            await step_context.context.send_activity(msg)            
             
        else:
            msg_text = ("Your flight is not confirmed!")
            msg = MessageFactory.text(msg_text, msg_text, InputHints.ignoring_input)
            await step_context.context.send_activity(msg)

            logger.info("Bot --> :  : flight is not confirmed!")
            print("confirmation step : flight is not confirmed!")

            logger.error("Bad answer!")
            print("Bad answer!")


        return await step_context.end_dialog()