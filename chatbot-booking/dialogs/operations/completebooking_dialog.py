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

#import json
#import requests






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

        order_l = user_details.orders_list
        if "or_city" not in order_l:
            message_text = "Please provide the depature city "
            prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        else:
            user_details.entities.update({"or_city": order_l["or_city"]})

        return await step_context.next(user_details)

 



    async def dst_city_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options
        rep =  step_context.result
        if "or_city" not in user_details.entities:
            user_details.entities.update({"or_city": rep})

        order_l = user_details.orders_list
        if "dst_city" not in order_l:
            message_text = "Please provide the destination city"
            prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        else:
            user_details.entities.update({"dst_city": order_l["dst_city"]})

        return await step_context.next(user_details)





    async def str_date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options
        rep =  step_context.result
        if "dst_city" not in user_details.entities:
            user_details.entities.update({"dst_city": rep})      

        order_l = user_details.orders_list
        if "str_date" not in order_l:
            message_text = "Please provide the departure date"
            prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        else:
            user_details.entities.update({"str_date": order_l["str_date"]})

        return await step_context.next(user_details)



    async def end_date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options
        rep =  step_context.result
        if "str_date" not in user_details.entities:
            user_details.entities.update({"str_date": rep})

        order_l = user_details.orders_list
        if "end_date" not in order_l:
            message_text = "Please provide the return date"
            prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        else:
            user_details.entities.update({"end_date": order_l["end_date"]})

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
    

        order_l = user_details.orders_list
        if "budget" not in order_l:        
            return await step_context.begin_dialog(
                BudgetResolverDialog.__name__, user_details
            )  # pylint: disable=line-too-long
        else:
            user_details.entities.update({"budget": order_l["budget"]})
        
        return await step_context.next(user_details)



   
    async def summary_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options
        rep =  step_context.result  # check the format
        if "budget" not in user_details.entities:
            user_details.entities.update({"budget": rep})

        return await step_context.end_dialog(user_details)
