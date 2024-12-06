#!/usr/bin/env python3
from os import environ
from okta.client import Client as OktaClient


try:
    okta_token = environ["OKTA_TOKEN"]
except KeyError:
    print("OKTA_TOKEN environment variable not set")
    exit(1)

okta_url: str = f"https://hingehealth-wf.okta.com"
okta_client = OktaClient({"orgUrl": okta_url, "token": okta_token})
