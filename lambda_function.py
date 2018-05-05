from __future__ import print_function
import json
import logging
import os
import time
from base64 import b64decode
from urllib2 import Request, urlopen, URLError, HTTPError


hookURL = os.environ['hookURL']
slackChannel = os.environ['slackChannel']
orgName = os.environ['orgName']
orgIcon = os.environ['orgIcon']
hiveURL = os.environ['hiveURL']
caseURL = hiveURL + "/index.html#/case/"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def add_object(title,value,short):

    object = {"title": title,"value": value,"short": short}
    return object


def process_event(event):

    logger.info("Processing event: %s", event)
    fields = []
    titleLink = False

    if "Delete" not in event['operation']:

        if event['objectType'] == "case":
            objectType = "Case"
            caseId = event['object']['caseId']
            fields.append(add_object("Case #",caseId,True))
            titleLink = caseURL + event['objectId'] + "/details"
        elif event['objectType'] == "case_task":
            objectType = "Task"
            titleLink = caseURL + event['rootId'] + "/tasks/" + event['objectId']
        else:
            caseId = "none"

        if event['operation'] == "Creation":
            operation = "created"
        elif event['operation'] == "Delete":
            operation = "deleted"
        elif event['operation'] == "Update":
            operation = "updated"
        else:
            operation = event['operation']

        if "description" in event['object']:
            description = event['object']['description'] # create/update
            fields.append(add_object("Description",description,False))
        elif "message" in event['object']:
            description = event['object']['message']
            fields.append(add_object("Description",description,False))
        else:
            description = "none"

        if "status" in event['object']:
            status = event['object']['status']
            fields.append(add_object("Status",status,True))
        else:
            status = "none"

        if "title" in event['object']:
            title = event['object']['title']
            fields.append(add_object("Title",title,True))
        else:
            title = "none"

        if "owner" in event['object']:
            owner = event['object']['owner']
            fields.append(add_object("Owner",owner,True))
        else:
            owner = "none"

        if "tlp" in event['object']:
            tlp = event['object']['tlp']
            fields.append(add_object("TLP",tlp,True))
        else:
            tlp = "none"

        if "createdBy" in event['object']:
            createdBy = event['object']['createdBy']
            fields.append(add_object("Created By",createdBy,True))
        else:
            createdBy = "none"

        if "Update" in event['operation']:
            updatedBy = event['object']['updatedBy']
            fields.append(add_object("Updated By",updatedBy,True))
        else:
            updatedBy = owner

        if "updatedAt" in event['object']:
            timestamp = event['object']['updatedAt']
        else:
            timestamp = int(time.time())

        if not titleLink: # if we haven't set it based on object type
            titleLink = hiveURL

        activity = "A " + str(objectType) + " has been " + operation + "."

        attachments = [
                {
                    "fallback": description,
                    "pretext": activity,
                    "author_name": (str(updatedBy)),
                    "title": (str(title)),
                    "title_link": titleLink,
                    "color": "danger",
                    "fields": fields,
                    "footer": orgName,
                    "footer_icon": orgIcon,
                    "ts": timestamp
                }
            ]

        send_to_slack(event,attachments)


def send_to_slack(event,attachments):

    slack_message = {
        'channel': slackChannel,
        'attachments': attachments
    }

    req = Request(hookURL, json.dumps(slack_message))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)


def lambda_handler(event, context):
    hive_event = json.loads(event['body'])
    process_event(hive_event)
