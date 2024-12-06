import importlib
import requests
from http import HTTPStatus

from tir_guardrails.constants import (ConfigKeys, VALIDATOR_MODULE_NAMES,
                                      GUARDRAILS_BASE_URL, THOR_GUARDRAILS_FETCH_URL,
                                      THOR_AUTH_TOKEN)
from tir_guardrails.helpers import get_default_headers


class Guard:
    def __init__(self, guardrails_config: dict = None, guardrails_id: int = None):
        if guardrails_config is None:
            if guardrails_id is None:
                raise ValueError("Either 'guardrails_config' or 'guardrails_id' must be provided")
            is_valid, result = self.__fetch_guardrails_config(guardrails_id)
            if is_valid:
                guardrails_config = result
            else:
                # TODO raise error 
                print(result)

        self.guardrails_config = guardrails_config
        self.block_message = guardrails_config.get(ConfigKeys.BLOCK_MESSAGE.value, "Prompt is Blocked by Guardrails")
        self.validators: list = []
        module_name = "tir_guardrails.{}.validator"
        for validator_name in self.guardrails_config.keys():
            validator_config = self.guardrails_config.get(validator_name, None)
            if validator_name in VALIDATOR_MODULE_NAMES and validator_config:
                module = importlib.import_module(module_name.format(validator_name))
                validator_class = getattr(module, "Validator")
                validator = validator_class(validator_config)
                self.validators.append(validator)

    def __fetch_guardrails_config(self, guardrails_id):
        # headers = get_default_headers()
        # fetch_url = GUARDRAILS_BASE_URL + guardrails_id + "/"
        # TODO REMOVE HARDCODED
        headers = {
                "Authorization": "Bearer " + THOR_AUTH_TOKEN,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        response = requests.request('GET', THOR_GUARDRAILS_FETCH_URL.format(guardrails_id=guardrails_id), headers=headers)
        res_json = response.json()
        if response.ok and response.status_code == HTTPStatus.OK:
            return True, res_json["data"]
        return False, res_json

    def validate(self, messages=None, prompt=None):
        if (messages or prompt) is None:
            raise ValueError("Either 'messages' or 'prompt' must be provided.")
        validation_passed = True
        is_messages = True if messages else False

        latest_validated_input = messages if is_messages else prompt
        validation_messages = {}
        for validator in self.validators:
            kwargs = {"messages" if is_messages else "prompt": latest_validated_input}
            result = validator.validate(**kwargs)
            validation_passed = validation_passed and result["validation_passed"]
            latest_validated_input = result["validated_output"]
            validation_message = result.get("validation_message", None)
            if validation_message:
                validation_messages[validator.name] = validation_message

        if validation_passed:
            return {
                "status": "success",
                "validation_passed": validation_passed,
                "validated_output": latest_validated_input,
                "validation_messages": validation_messages
            }

        return {
            "status": "error",
            "validation_passed": validation_passed,
            "validated_output": latest_validated_input,
            "validation_messages": validation_messages
        }
