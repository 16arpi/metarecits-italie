import os
import sys
import jinja2
import json

from pprint import pprint
from pathlib import Path
from pydantic import BaseModel
from openai import OpenAI
from typing import List

class Action(BaseModel):
    description: str
    initiateurs: List[str]
    receveurs: List[str]
    justifications: List[str]
    moyens: List[str]
    opposants: List[str]

class Resultat(BaseModel):
    raisonnement: str
    actions: List[Action]

class Reasoning:


    def _to_json(self, obj: Resultat):
        actions = []
        for action in obj.actions:
            actions.append({
                "description": action.description,
                "initiateurs": action.initiateurs,
                "receveurs": action.receveurs,
                "justifications": action.justifications,
                "moyens": action.moyens,
                "opposants": action.opposants,
            })

        return {
            "raisonnement": obj.raisonnement,
            "actions": actions
        }

    def make_user_thinking_prompt(self, text, reason):
        template = jinja2.Template(reason)
        return template.render({
            "texte": text
        })

    def execute(self):
        messages = [
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": self.reason_prompt
                }
            ]

        print("Raisonnement...", file=sys.stderr)
        res = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0
        )

        messages += [{
            "role": "assistant",
            "content": res.choices[0].message.content
        }]

        print("Extraction...", file=sys.stderr)
        res = self.client.responses.parse(
            model="gpt-4o",
            input=messages,
            temperature=0,
            text_format=Resultat
        )

        return self._to_json(res.output_parsed)

    def __init__(self, text, system, reason, extract, model):
        self.text = text
        self.system_prompt = system
        self.reason_prompt = self.make_user_thinking_prompt(text, reason)
        self.extract_prompt = extract
        self.model = model

        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )


text = Path(sys.argv[1]).read_text()
prompt_system = Path(sys.argv[2]).read_text()
prompt_reason = Path(sys.argv[3]).read_text()
prompt_extract = Path(sys.argv[4]).read_text()

instance = Reasoning(text, prompt_system, prompt_reason, prompt_extract, None)
result = instance.execute()

sys.stdout.write(json.dumps(result, indent=True))
