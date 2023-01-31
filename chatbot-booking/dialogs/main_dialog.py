from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt, ConfirmPrompt
from botbuilder.core import MessageFactory, TurnContext, CardFactory, UserState
from botbuilder.schema import InputHints, CardAction, ActionTypes, SuggestedActions

from botbuilder.dialogs.choices import Choice

import string
import random

from .operations.createbooking_dialog import CreateBookingDialog
from .operations.help_dialog import HelpDialog


class MainDialog(ComponentDialog):
    def __init__(
        self, createbooking_dialog: CreateBookingDialog,
        help_dialog: HelpDialog
    ):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self._createbooking_dialog_id = createbooking_dialog.id
        self._help_dialog_id = help_dialog.id
        self.add_dialog(createbooking_dialog)
        self.add_dialog(help_dialog)
        
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog", [self.userid_step, self.intro_step, self.act_step, self.final_step]
            )
        )

        self.initial_dialog_id = "WFDialog"



    async def userid_step(self, step_context: WaterfallStepContext)-> DialogTurnResult:
        user_details = step_context.options
         

        #attribuer un user_id d'office
        N= 7
        user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
        user_details.user_id = user_id

        #user_id = user_details.user_id

        return await step_context.next(user_details)




    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        user_details = step_context.options
        user_id = None
        
        if user_details:
            if user_details.user_id == None:
                user_id = None
            else:
                user_id = user_details.user_id
        else:
            user_id = None

        if user_id == None:
            if (step_context.result):
                step_context.values['user_id']= step_context.result
                user_details.user_id = step_context.result

        reply = MessageFactory.suggested_actions(
            [CardAction(title='Flight Booking', type=ActionTypes.im_back, value='Flight Booking'),
            CardAction(title='Help', type=ActionTypes.im_back, value='Help'),
            ], 'Please Select a Choice')

        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=reply,
                choices=[Choice("Flight Booking"), Choice("Help")],
            ),
        )

    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values['Operation'] = step_context.result.value
        operation = step_context.values['Operation']

        msg_text = "you have selected " + operation
        msg = MessageFactory.text(
            msg_text, msg_text, InputHints.ignoring_input
        ) 
        await step_context.context.send_activity(msg) 

        user_details = step_context.options
        if operation == "Flight Booking":
            return await step_context.begin_dialog(self._createbooking_dialog_id, user_details)  

        if operation == "Help":
            return await step_context.begin_dialog(self._help_dialog_id, user_details)



    async def final_step(self, step_context: WaterfallStepContext)-> DialogTurnResult:
        user_details = step_context.options
        return await step_context.replace_dialog(self.id, user_details)
        #return await step_context.end_dialog(user_details)