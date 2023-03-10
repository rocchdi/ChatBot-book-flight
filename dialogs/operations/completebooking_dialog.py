# dans le cas où on a des missing entities dans la demande de l'utilisateur, On crée une boîte de dialogue personnalisée, completeBookingDialog,
# qui est un WaterfallDialog qui collecte des informationssur le voyage telles que la ville de départ, la ville de destination, la date de départ, la date de retour et le budget.
# Il utilise plusieurs autres boîtes de dialogue intégrées (TextPrompt, ChoicePrompt, BudgetResolverDialog) ainsi que des entités
# personnalisées (telles que "or_city", "dst_city", "str_date", "end_date") pour stocker les entrées de l'utilisateur.
# La boîte de dialogue est conçue pour demander à l'utilisateur des informations étape par étape, en passant d'une étape à la suivante
# jusqu'à ce que toutes les informations nécessaires aient été collectées.



from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints

from .budget_resolver_dialog import BudgetResolverDialog


from config import DefaultConfig

import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler


CONFIG = DefaultConfig()

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=f'InstrumentationKey={CONFIG.INSIGHT_INSTRUMENT_KEY}'))
logger.setLevel(logging.DEBUG)




class completeBookingDialog(ComponentDialog):
    def __init__(self, dialog_id:str = None):
        super(completeBookingDialog, self).__init__(dialog_id or completeBookingDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(BudgetResolverDialog(BudgetResolverDialog.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [self.or_city_step, self.dst_city_step, self.str_date_step, self.end_date_step, self.budget_step, self.summary_step]
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

 


    async def or_city_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options
        user_details.entities = dict()

        booking_l = user_details.bookings_list
        if "or_city" not in booking_l:
            message_text = "Please provide the depature city "
            logger.info("Bot --> : Please provide the departure city")
            prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        else:
            user_details.entities.update({"or_city": booking_l["or_city"]})

        return await step_context.next(user_details)

 



    async def dst_city_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options
        rep =  step_context.result
        if "or_city" not in user_details.entities:
            user_details.entities.update({"or_city": rep})
            logger.info(f"departure city : {rep}")

        booking_l = user_details.bookings_list
        if "dst_city" not in booking_l:
            message_text = "Please provide the destination city"
            logger.info("Bot --> : Please provide the destination city")
            prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        else:
            user_details.entities.update({"dst_city": booking_l["dst_city"]})

        return await step_context.next(user_details)





    async def str_date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options
        rep =  step_context.result
        if "dst_city" not in user_details.entities:
            user_details.entities.update({"dst_city": rep})
            logger.info(f"destination city : {rep}")    

        booking_l = user_details.bookings_list
        if "str_date" not in booking_l:
            message_text = "Please provide the departure date"
            logger.info("Bot --> : Please provide the departure date")
            prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        else:
            user_details.entities.update({"str_date": booking_l["str_date"]})

        return await step_context.next(user_details)



    async def end_date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options
        rep =  step_context.result
        if "str_date" not in user_details.entities:
            user_details.entities.update({"str_date": rep})
            logger.info(f"departure date : {rep}")

        booking_l = user_details.bookings_list
        if "end_date" not in booking_l:
            message_text = "Please provide the return date"
            logger.info("Bot --> : Please provide the return date")
            prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        else:
            user_details.entities.update({"end_date": booking_l["end_date"]})

        return await step_context.next(user_details)


  

    async def budget_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for budget.
        This will use the BUDGET_RESOLVER_DIALOG."""

        user_details = step_context.options
        rep =  step_context.result
        if "end_date" not in user_details.entities:
            user_details.entities.update({"end_date": rep})
            logger.info(f"return date : {rep}")
    

        booking_l = user_details.bookings_list
        if "budget" not in booking_l:        
            return await step_context.begin_dialog(
                BudgetResolverDialog.__name__, user_details
            )  # pylint: disable=line-too-long
        else:
            user_details.entities.update({"budget": booking_l["budget"]})
        
        return await step_context.next(user_details)



   
    async def summary_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options
        rep =  step_context.result  # check the format
        if "budget" not in user_details.entities:
            user_details.entities.update({"budget": rep})
            logger.info(f"budget : {rep}")

        return await step_context.end_dialog(user_details)
