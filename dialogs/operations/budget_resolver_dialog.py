"""
On défini une classe "BudgetResolverDialog" . La classe utilise un "WaterfallDialog" pour gérer les étapes du dialogue
et un "NumberPrompt" pour demander et valider le budget du flight booking.
on utilise  également un logger pour enregistrer des erreurs produites sur le budget entré par l'utilisateur
"""


from botbuilder.core import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext
from botbuilder.dialogs.prompts import (
    NumberPrompt,
    PromptValidatorContext,
    PromptOptions,
)
#from .cancel_and_help_dialog import CancelAndHelpDialog

from botbuilder.dialogs import ComponentDialog
from config import DefaultConfig

import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

CONFIG = DefaultConfig()


logger = logging.getLogger(__name__)
#logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=28845d90-dbbe-4a5a-826b-6fb138c8c9e7'))
logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=f0155c77-7588-4c00-a385-525862c02a00'))
#logger.addHandler(AzureLogHandler(connection_string=f'InstrumentationKey={CONFIG.INSIGHT_INSTRUMENT_KEY}'))


#logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)
 


class BudgetResolverDialog(ComponentDialog):
    """Resolve the budget"""

    def __init__(self, dialog_id: str = None):
        super(BudgetResolverDialog, self).__init__(
            dialog_id or BudgetResolverDialog.__name__
        )

        self.add_dialog(
            NumberPrompt(
                NumberPrompt.__name__, BudgetResolverDialog.budget_prompt_validator
            )
        )
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__ + "2", [self.initial_step, self.final_step]
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__ + "2"

    async def initial_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for the budget."""

        prompt_msg = "What is your budget for this purchase?"
        reprompt_msg = (
            "I'm sorry, for best results, please enter your budget "
            "in a numerical format or with a $ sign."
        )


        return await step_context.prompt(
            NumberPrompt.__name__,
            PromptOptions(   
                prompt=MessageFactory.text(prompt_msg),
                retry_prompt=MessageFactory.text(reprompt_msg),
            ),
        )

    async def final_step(self, step_context: WaterfallStepContext):
        """Cleanup - set final return value and end dialog."""

        budget = step_context.result
        return await step_context.end_dialog(budget)

    

    @staticmethod
    async def budget_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        """ Validate the budget provided is in proper form. """
        if prompt_context.recognized.succeeded:
            budget = prompt_context.recognized.value
            if  float(budget) > 0:
                return True
            else:
                #properties = {"custom_dimensions": {"function": 'summary_step', 'error format or value of budget entred by the user': budget}}
                print("Captured user answer on budget : Bad value 0 for budget")
                logger.error("Captured user answer on budget : Bad value 0 for budget")
                logger.error("Bad answer!")
        else:
            print("Captured user answer on budget : Bad format or value of budget")
            logger.error("Captured user answer on budget : Bad format or value of budget")
            logger.error("Bad answer!")
        return False
