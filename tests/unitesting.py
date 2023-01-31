"""
ensemble de tests unitaires pour une application de chatbot.
on a deux classes de tests: "TestLuis" et "BudgetPromptTest".

La classe "TestLuis" contient un test qui vérifie si les informations extraites par l'application LUIS 
(le service de reconnaissance de la langue naturelle) à partir d'une phrase donnée sont correctes. 
Il teste si l'intention de la phrase est "BookFlight" et s'il contient les informations correctes
sur la ville de départ, la ville de destination, la date de départ et la date de retour, ainsi que le budget.

La classe "BudgetPromptTest" contient deux tests pour tester les fonctionnalités de prompts, une pour demander
un budgetet l'autre pour demander une date de voyage. Ces tests utilisent des instances de la classe "TestAdapter"
pour simuler des interactions avec un utilisateur et vérifier si le bot répond correctement aux prompts et si les
réponses de l'utilisateur sont correctement traitées.

"""

#pytest unittesting.py
#pytest unittesting.py::test_booking_details
#python unitesting.py
#python -m unittest unitesting.py
#python -m unittest tests\unitesting.py
#python -m unittest unittesting.TestLuis.test_booking_details



import unittest


from luisApp import getLuisResponse
from dialogs.operations.createbooking_dialog import extract_luis_info


# BOT FRAMEWORK
from botbuilder.dialogs.prompts import (
    PromptOptions, 
)

from botbuilder.core import (
    TurnContext, 
    ConversationState, 
    MemoryStorage, 
    MessageFactory, 
)
from botbuilder.dialogs import DialogSet, DialogTurnStatus
from botbuilder.core.adapters import TestAdapter
from botbuilder.dialogs.prompts import NumberPrompt,DateTimePrompt

import aiounittest

class TestLuis(unittest.TestCase):

	def test_booking_details(self):

		text = "I need book a fly from paris to london on august 16 back on august 17 for a budget of 300"
		data = getLuisResponse(text)
		results = extract_luis_info(data)
		intent = results['intent']

		self.assertEqual(intent,"BookFlight")
		self.assertIn("paris",results['or_city'])
		self.assertIn("london",results['dst_city'])
		self.assertIn("august 16",results['str_date'])
		self.assertIn("august 17",results['end_date'])
		self.assertIn("300",results['budget'])

           

class BudgetPromptTest(aiounittest.AsyncTestCase):
    async def test_budget_prompt(self):
        async def exec_test(turn_context:TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if (results.status == DialogTurnStatus.Empty):
                options = PromptOptions(
                    prompt=MessageFactory.text("what is your budget ?")
                )
                await dialog_context.prompt(NumberPrompt.__name__, options)

            elif results.status == DialogTurnStatus.Complete:
                reply = results.result
                await turn_context.send_activity(str(reply))

            await conv_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        conv_state = ConversationState(MemoryStorage())

        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)
        
        dialogs.add(NumberPrompt(NumberPrompt.__name__))

        step1 = await adapter.test('Hello', 'what is your budget ?')
        step2 = await step1.send('Just 1200 dollars.')
        await step2.assert_reply("1200")





    async def test_date_prompt(self):
        async def exec_test(turn_context:TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if (results.status == DialogTurnStatus.Empty):
                options = PromptOptions(
                    prompt=MessageFactory.text("When you want to travel?")
                )
                await dialog_context.prompt(DateTimePrompt.__name__, options)

            elif results.status == DialogTurnStatus.Complete:
                reply = results.result
                await turn_context.send_activity(str(reply[-1].value))

            await conv_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        conv_state = ConversationState(MemoryStorage())

        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)
        
        dialogs.add(DateTimePrompt(DateTimePrompt.__name__))

        step1 = await adapter.test('Hello', 'When you want to travel?')
        # First test
        step2 = await step1.send('The 21 December 2023')
        await step2.assert_reply("2023-12-21")
        # Second test
        step1 = await adapter.test('Hello', 'When you want to travel?')
        step2 = await step1.send('The 25 June 2023')
        await step2.assert_reply("2023-06-25")

 
# on utilise le statement suivant lancer les tests lorsque le script est exécuté directement
if __name__ == '__main__':
    unittest.main(module="tests")