#main application file : app.py


from http import HTTPStatus
from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import(
    BotFrameworkAdapterSettings,
    ConversationState,
    MemoryStorage,
    UserState,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity

from config import DefaultConfig
from dialogs import MainDialog
from bots import DialogAndWelcomeBot

from adapter_with_error_handler import AdapterWithErrorHandler

from dialogs.operations.createbooking_dialog import CreateBookingDialog
from dialogs.operations.help_dialog import HelpDialog
from dialogs.operations.completebooking_dialog import completeBookingDialog


CONFIG = DefaultConfig()

SETTINGS = BotFrameworkAdapterSettings(CONFIG.MS_APP_ID, CONFIG.MS_APP_PASSWORD)

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


#Listen for incoming requests on /api/messages.
async def messages(req: Request)-> Response:
    #Main bor message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)

    return Response(status = HTTPStatus.OK)


# python3.8 -m aiohttp.web -H 0.0.0.0 -P 8000 app:init_func
def init_func(argv):
    app = web.Application(middlewares=[aiohttp_error_middleware])
    app.router.add_post("/api/messages", messages)
    return app






if __name__ == "__main__":
    app = init_func(None)
    try:
        # Run app in production
        web.run_app(app, host='localhost', port=CONFIG.PORT)
    except Exception as error:
        raise error