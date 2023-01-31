# Flight Booking Bot with Application Insights

Flight Booking Bot with Application Insights.

This bot has been created using [Bot Framework](https://dev.botframework.com), it shows how to:

- Use [LUIS](https://www.luis.ai) to implement core AI capabilities
- Implement a multi-turn conversation using Dialogs
- Handle user interruptions for such things as `Help`
- Prompt for and validate requests for information from the user
- Use [Application Insights](https://docs.microsoft.com/azure/azure-monitor/app/cloudservices) to monitor the bot

## Prerequisites

This sample **requires** prerequisites in order to run.

### Overview

This bot uses [LUIS](https://www.luis.ai), an AI based cognitive service, to implement language understanding
and [Application Insights](https://docs.microsoft.com/azure/azure-monitor/app/cloudservices), an extensible Application Performance Management (APM) service for web developers on multiple platforms.


#### LUIS portal account:

You should already have a LUIS account with either https://luis.ai, https://eu.luis.ai, or https://au.luis.ai. To determine where to create a LUIS account, consider where you will deploy your LUIS applications, and then place them in [the corresponding region][LUIS-Authoring-Regions].

After you've created your account, you need your [Authoring Key][LUIS-AKey] and a LUIS application ID.

  [LUIS-Authoring-Regions]: https://docs.microsoft.com/azure/cognitive-services/luis/luis-reference-regions#luis-authoring-regions]
  [LUIS-AKey]: https://docs.microsoft.com/azure/cognitive-services/luis/luis-concept-keys#authoring-key


### Create a LUIS Application to enable language understanding

LUIS language model setup, training, and application configuration steps can be found [here](https://docs.microsoft.com/azure/bot-service/bot-builder-howto-v4-luis?view=azure-bot-service-4.0&tabs=cs).


### Add Application Insights service to enable the bot monitoring

Application Insights resource creation steps can be found [here](https://docs.microsoft.com/azure/azure-monitor/app/create-new-resource).

You must include the instrumentation key in the `config.py` file, as well is in the designated field in your Azure Bot resource.

### Add Activity and Personal Information logging for Application Insights
To log activity and personal information in azure application insight, we include in the dialog files the following code which uses the opencensus-ext-azure library.

The required code is as follows:
```python
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=<YOURInstrumentationKey>'))
logger.setLevel(logging.DEBUG)
```

## To try thye bot application

- Clone the repository
```bash
git clone https://github.com/rocchdi/ChatBot-book-flight
```
- In a terminal, navigate to `ChatBot-book-flight` folder
- Activate your desired virtual environment
- In the terminal, type `pip install -r requirements.txt`
- Run your bot with `python app.py`

## Testing the bot using Bot Framework Emulator

[Bot Framework Emulator](https://github.com/microsoft/botframework-emulator) is a desktop application that allows bot developers to test and debug their bots on localhost or running remotely through a tunnel.

- Install the latest Bot Framework Emulator from [here](https://github.com/Microsoft/BotFramework-Emulator/releases)

### Connect to the bot using Bot Framework Emulator

- Launch Bot Framework Emulator
- File -> Open Bot
- Enter a Bot URL of `http://localhost:3978/api/messages`

## Deploy the bot to Azure

To learn more about deploying a bot to Azure, see [Deploy your bot to Azure](https://aka.ms/azuredeployment) for a complete list of deployment instructions.

## Further reading

- [Bot Framework Documentation](https://docs.botframework.com)
- [Language Understanding using LUIS](https://docs.microsoft.com/en-us/azure/cognitive-services/luis/)
- [Application insights Overview](https://docs.microsoft.com/azure/azure-monitor/app/app-insights-overview)
- [Getting Started with Application Insights](https://github.com/Microsoft/ApplicationInsights-aspnetcore/wiki/Getting-Started-with-Application-Insights-for-ASP.NET-Core)
