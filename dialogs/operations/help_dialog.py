from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt, ConfirmPrompt
from botbuilder.core import MessageFactory, TurnContext, CardFactory, UserState
from botbuilder.schema import InputHints, CardAction, ActionTypes, SuggestedActions


class HelpDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(HelpDialog, self).__init__(dialog_id or HelpDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__, [self.help_step]
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__



    async def help_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options
 
        message_text = "To help you choose a travel offer, please select Flight Booking and enter the description of your flight. For example enter : Book a flight from Paris"
        prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
        await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

        return await step_context.end_dialog(user_details)
