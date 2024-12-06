import re

from openai import OpenAI

from tir_guardrails.constants import (ConfigKeys, ValidatorTypes, GenAIModels,
                                      ValidatorModules, OPENAI_BASE_URL, OPENAI_API_KEY)
from tir_guardrails.harmful_content.prompt_template import GUARD_CHAT_TEMP, GUARD_COMP_TEMP


class Validator:
    def __init__(self, config: dict):
        self.name = ValidatorModules.HARMFUL_CONTENT.value
        self.validator_type = ValidatorTypes(config.get(ConfigKeys.VALIDATOR_TYPE.value))
        self.served_model = GenAIModels(config.get(ConfigKeys.SERVED_MODEL.value))
        self.extra: dict = config.get(ConfigKeys.CONFIG.value)

        if ValidatorTypes.GUARD == self.validator_type:
            self.blocked_categories: list[dict] = self.extra.get(ConfigKeys.BLOCKED_CATEGORIES.value)
            self.client = OpenAI(
                api_key=OPENAI_API_KEY,
                base_url=OPENAI_BASE_URL.format(model=self.served_model.value)
            )
        elif ValidatorTypes.LLM == self.validator_type:
            raise NotImplementedError

    def validate(self, messages=None, prompt=None):
        if (messages or prompt) is None:
            raise ValueError("Either 'messages' or 'prompt' must be provided.")

        if ValidatorTypes.GUARD == self.validator_type:
            return self.__validate_guard(messages=messages, prompt=prompt)

    def get_prompt(self, messages=None, prompt=None):
        if (messages or prompt) is None:
            raise ValueError("Either 'messages' or 'prompt' must be provided.")

        if ValidatorTypes.GUARD == self.validator_type:
            category_pompt: str = "\n"
            for category in self.blocked_categories:
                category_pompt = category_pompt + category.get("name")
                des = category.get('description', None)
                if des:
                    category_pompt = category_pompt + f" {des}"
                category_pompt = category_pompt + "\n"

            conv_prompt: str = ""
            if messages:
                for i, msg in enumerate(messages):
                    if i % 2 == 0:
                        conv_prompt = conv_prompt + "User: "
                    else:
                        conv_prompt = conv_prompt + "Agent: "
                    content = msg.get('content')
                    if type(content) is str:
                        conv_prompt = conv_prompt + content
                    else:
                        raise NotImplementedError
                    conv_prompt = conv_prompt + "\n\n"

                return GUARD_CHAT_TEMP.format(
                    role="User" if (len(messages) % 2) == 1 else "Agent",
                    blocked_categories=category_pompt,
                    conversation=conv_prompt
                )
            elif prompt:
                conv_prompt = conv_prompt + prompt + "\n\n"
                return GUARD_COMP_TEMP.format(
                    blocked_categories=category_pompt,
                    conversation=conv_prompt
                )

    def __validate_guard(self, messages=None, prompt=None):
        guard_prompt = self.get_prompt(messages=messages, prompt=prompt)
        if self.validator_type == ValidatorTypes.GUARD:
            try:
                completion = self.client.completions.create(
                    model=self.served_model.value,
                    prompt=guard_prompt
                )
                model_response = completion.choices[0].text
                validation_passed, categories_found = self.__parse_model_response(model_response)
                response = {
                    "status": "success",
                    "validation_passed": validation_passed,
                    "validated_output": prompt if prompt else messages
                }
                if not validation_passed:
                    response["validation_message"] = "Following unsafe content categories found " + ",".join(categories_found)
                return response
            except Exception as e:
                # TODO Logging
                print(e)
                return {
                    "status": "error",
                    "validation_message": f"Following error occured {str(e)}",
                    "validation_passed": False,
                    "validated_output": prompt if prompt else messages
                }

    def __parse_model_response(self, model_response: str):
        chunks = [item for item in model_response.strip(' ').split("\n") if item]
        regex = r"^S([1-9]|[1-4][0-9])$"
        cat_keys_found = [chunk for chunk in chunks if re.search(regex, chunk)]
        is_safe = True if chunks[0] == "safe" else False
        categories_found = []
        for category in self.blocked_categories:
            for cat_key_found in cat_keys_found:
                if category.get("name").startswith(f"{cat_key_found}:"):
                    categories_found.append(category.get("name"))
        return is_safe, categories_found
