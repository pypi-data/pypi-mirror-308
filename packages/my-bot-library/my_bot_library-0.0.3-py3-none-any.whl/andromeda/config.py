#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import os
import yaml


def read_db_yaml_file():
    # Path to your YAML file
    file_pth = "/opt/app/bootstrap/secrets/secret"
    db_config = {}
    try:
        with open(file_pth, "r") as file:
            db_config = yaml.safe_load(file)
    except FileNotFoundError as e:
        raise Exception("db File not found") from e
    return db_config


def read_bot_yaml_file():
    # Path to your YAML file
    file_path = "/opt/app/bootstrap/config.yaml"
    config = {}
    try:
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)
    except FileNotFoundError as e:
        raise Exception("bot File not found") from e
    return config


# Reading the bot configuration
config_value = read_bot_yaml_file()
config_db = config_value.get("channelbotdb", {})
host = config_db.get("host")
db_name = config_db.get("database")
port = config_db.get("port")
login_url = config_value.get("loginUrl")
api_url = config_value.get("apiUrl")
graphql_url = config_value.get("graphqlUrl")

# Reading the Secrets from secrets
db_conf = read_db_yaml_file()
db_config = db_conf.get("channelbotdb", {})
username = db_config.get("user")
password = db_config.get("password")

# Slack credentials
slack_cred = config_value.get("slack", {})
slack_client_id = slack_cred.get("clientId")
slack_app_secret = db_conf.get("slack", {}).get("applicationSecret")
slack_token = db_conf.get("slack", {}).get("slackToken")
slack_secret = db_conf.get("slack", {}).get("slackSecret")

# Teams credentials
teams_cred = config_value.get("teams", {})
teams_app_id = teams_cred.get("applicationId")
teams_tenant_id = teams_cred.get("tenantId")
teams_app_secret = db_conf.get("teams", {}).get("applicationSecret")


class DefaultConfig:
    """Bot Configuration"""

    PORT = 3978

    LOGIN_URL = os.environ.get("LoginUrl", login_url)
    API_URL = os.environ.get("ApiUrl", api_url)
    GRAPHQL_URL = os.environ.get("GraphqlUrl", graphql_url)
    REDIRECT_URL = os.environ.get(
        "RedirectUrl", config_value.get("redirectUrl"))
    DB_USER = os.environ.get("DBUser", username)
    DB_PASSWORD = os.environ.get("DBPassword", password)
    DB_HOST = os.environ.get("DBHost", host)
    DB_NAME = os.environ.get("DBName", db_name)

    # Use an environment variable or flag to choose Slack or Teams config
    BOT_PLATFORM = os.environ.get("BOT_PLATFORM", "slack").lower()

    if slack_client_id:
        # Slack Configuration
        CLIENT_ID = os.environ.get("SlackClientId", slack_client_id)
        SLACK_TOKEN = os.environ.get("SlackToken", slack_token)
        SLACK_SECRET = os.environ.get("SlackSecret", slack_secret)

        APP_SECRET = os.environ.get("APPSecret", slack_app_secret)
        APP_CLIENT = os.environ.get("APPClient", slack_client_id)

    elif teams_app_id:
        # Teams Configuration
        APP_ID = os.environ.get("MicrosoftAppId", teams_app_id)
        APP_PASSWORD = os.environ.get("MicrosoftAppPassword", teams_app_secret)
        TENANT_ID = os.environ.get("Tenant_id", teams_tenant_id)

    else:
        raise ValueError(f"Unsupported BOT_PLATFORM: {BOT_PLATFORM}")
