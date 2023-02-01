#from http import HTTPStatus
from flask import Flask,request,Response
import asyncio

#from aiohttp.web import Request, Response, json_response
from botbuilder.core import(
    BotFrameworkAdapterSettings,
    ConversationState,
    MemoryStorage,
    UserState,
)
#from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity

from config import DefaultConfig
from dialogs import MainDialog
from bots import DialogAndWelcomeBot

from adapter_with_error_handler import AdapterWithErrorHandler

from dialogs.operations.createbooking_dialog import CreateBookingDialog
from dialogs.operations.help_dialog import HelpDialog
from dialogs.operations.completebooking_dialog import completeBookingDialog


CONFIG = DefaultConfig()

SETTINGS = BotFrameworkAdapterSettings("", "")

MEMORY = MemoryStorage()
USER_STATE = UserState(MEMORY)
CONVERSATION_STATE = ConversationState(MEMORY)

#create adapter
ADAPTER = AdapterWithErrorHandler(SETTINGS, CONVERSATION_STATE)

COMPLETEBOOKING_DIALOG = completeBookingDialog()
CREATEBOOKING_DIALOG = CreateBookingDialog(COMPLETEBOOKING_DIALOG)
HELP_DIALOG = HelpDialog()

DIALOG = MainDialog(CREATEBOOKING_DIALOG, HELP_DIALOG)
BOT = DialogAndWelcomeBot(CONVERSATION_STATE, USER_STATE, DIALOG)

 

app = Flask(__name__)
loop = asyncio.get_event_loop()
 

SETTINGS = BotFrameworkAdapterSettings("", "")
DAPTER = AdapterWithErrorHandler(SETTINGS, CONVERSATION_STATE)


BOT = DialogAndWelcomeBot(CONVERSATION_STATE, USER_STATE, DIALOG)



@app.route("/api/messages",methods=["POST"])
def messages():
    if "application/json" in request.headers["content-type"]:
      jsonmessage = request.json
    else:
      return Response(status=415)

    activity = Activity().deserialize(jsonmessage)

    async def turn_call(turn_context):
        await BOT.on_turn(turn_context)

    task = loop.create_task(ADAPTER.process_activity(activity,"",turn_call))
    loop.run_until_complete(task)

    return Response(status=200)


if __name__ == "__main__":
    app.run(host = "localhost", port = CONFIG.PORT)
     