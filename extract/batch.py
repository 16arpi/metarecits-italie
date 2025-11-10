from jinja2 import Template
from pydantic import BaseModel
from typing import List
from openai import OpenAI

import pandas as pd
import os
from hashlib import md5
import json

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

class Response(BaseModel):
    subject: List[str]
    object: List[str]
    sender: List[str]
    receiver: List[str]
    helper: List[str]
    opponent: List[str]

SYSTEM_PROMPT = Template(
    """
    Your are a actantial model annotator. According to the Actantial Model by Greimas with the actant label set ["Sender", " Receiver", "Subject", "Object", "Helper", "Opponent"], the actants are defined as follows:
    * Subject: The character who carries out the action and desires the Object.
    * Object: The character or thing that is desired.
    * Sender: The character who initiates the action and communicates the Object.
    * Receiver: The character who receives the action or the Object.
    * Helper: The character who assists the Subject in achieving its goal.
    * Opponent: The character who opposes the Subject in achieving its goal.
    Based on this Actantial Model and the actant label set, please recognize the actants in the texts given by the user.
    """
)

USER_PROMPT = Template(
    """
    Text content: {{ text }}

    Question: What are the main actants in the text? Provide the answer in the following JSON format: {"Actant Label": ["Actant Name"]}. If there is no corresponding actant, return the following empty list: {"Actant Label": []}.
    """
)

def format(texte):
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT.render()
        },
        {
            "role": "user",
            "content": USER_PROMPT.render({
                "text": texte
            })
        }
    ]

def perform(texte):
    completion = client.chat.completions.parse(
        model="gpt-4o",
        messages=format(texte),
        temperature=0,
        response_format=Response,
    )

    return completion.choices[0].message.parsed

def batch(
    text,
    system_prompt=SYSTEM_PROMPT,
    user_prompt=USER_PROMPT,
    model="gpt-4o",
    response_format=Response,
    temperature=0,
    max_completion_tokens=2048,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    store=False):

    id = md5(text.encode("utf-8")).hexdigest()[:6]

    serialized = response_format.model_json_schema()
    serialized["additionalProperties"] = False

    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "extraction",
            "strict": True,
            "schema": serialized,
        }
    }

    messages = [
        {
            "role": "system",
            "content": system_prompt.render()
        },
        {
            "role": "user",
            "content": user_prompt.render({
                "text": text
            })
        }
    ]

    body = {
        "model": model,
        "messages": messages,
        "response_format": schema,
        "temperature": temperature,
        "max_completion_tokens": max_completion_tokens,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
        "store": store
    }

    req = {
        "custom_id": f"request-{id}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": body
    }

    return json.dumps(req)


df = pd.read_csv("./csv/dataset.csv")
texte = df["text"].iloc[0]

print(batch(texte))
