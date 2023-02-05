# Configuratio#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os
import sys
from dotenv import load_dotenv

# Load the environment variables from the .env file only when running locally
if not "AZURE_FUNCTION_APP_NAME" in os.environ:
    load_dotenv()


class DefaultConfig:
    """Configuration for the bot."""

    PORT = 3978
    MS_APP_ID = os.environ.get("MicrosoftAppId", "")
    MS_APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    APP_ID = os.environ.get("LuisAppId", "")
    APP_PREDICTION_KEY = os.environ.get("LuisAPIKey", "")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "")
    ENDPOINT_PREDICTION_URL = os.environ.get("ENDPOINT_PREDICTION_URL", "")
    LUIS_APP_URL = os.environ.get("LUIS_APP_URL", "")
    INSIGHT_INSTRUMENT_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", ""
    )
    APPINSIGHTS_INSTRUMENTATION = os.environ.get(
        "AppInsightsInstrumentation", ""
    )