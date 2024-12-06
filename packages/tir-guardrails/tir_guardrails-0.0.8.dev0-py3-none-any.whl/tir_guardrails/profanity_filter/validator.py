import re

from better_profanity import profanity
from openai import OpenAI
from profanity_check import predict

from tir_guardrails.constants import (ConfigKeys, ValidatorTypes, ValidatorModules,
                                      LibTypes, GenAIModels, OPENAI_BASE_URL, OPENAI_API_KEY)


class Validator:
    def __init__(self, config: dict):
        self.name = ValidatorModules.PROFANITY_FILTER.value
        self.validator_type = ValidatorTypes(config.get(ConfigKeys.VALIDATOR_TYPE.value))
        self.extra: dict = config.get(ConfigKeys.CONFIG.value)

        if self.validator_type is ValidatorTypes.LIB:
            self.lib_name = LibTypes(self.extra.get(ConfigKeys.LIB_NAME.value))
            if self.lib_name == LibTypes.BETTER_PROFANITY:
                self.wordlist = self.extra.get(ConfigKeys.WORDLIST.value, None)
                self.wordlist_file = self.extra.get(ConfigKeys.WORDLIST_FILE.value, None)
                self.overwrite_wordlist = self.extra.get(ConfigKeys.OVERWRITE_WORDLIST.value, False)
                self.whitelist_words = self.extra.get(ConfigKeys.WHITELIST_WORDS.value, None)
                params = {}
                if self.whitelist_words:
                    params["whitelist_words"] = self.whitelist_words

                if self.wordlist_file:
                    if self.wordlist:
                        raise ValueError("Only one should be present either 'wordlist' or 'wordlist_file'")
                    profanity.load_censor_words_from_file(self.wordlist_file, **params)
                elif self.wordlist:
                    if self.overwrite_wordlist:
                        profanity.load_censor_words(self.wordlist, **params)
                    else:
                        profanity.load_censor_words(**params)
                        profanity.add_censor_words(self.wordlist)
                else:
                    profanity.load_censor_words(**params)

        elif self.validator_type is ValidatorTypes.LLM:
            self.served_model = GenAIModels(self.extra.get(ConfigKeys.SERVED_MODEL.value))
            self.prompt_template = self.extra.get(ConfigKeys.PROMPT_TEMPLATE.value)
            self.client = OpenAI(
                api_key=OPENAI_API_KEY,
                base_url=OPENAI_BASE_URL.format(model=self.served_model.value)
            )

    def validate(self, messages=None, prompt=None):
        if (messages or prompt) is None:
            raise ValueError("Either 'messages' or 'prompt' must be provided.")
        if self.validator_type == ValidatorTypes.LLM:
            return self.__validate_vllm(messages=messages, prompt=prompt)
        elif self.validator_type == ValidatorTypes.LIB:
            if self.lib_name == LibTypes.BETTER_PROFANITY:
                return self.__validate_better_profanity(messages=messages, prompt=prompt)
            elif self.lib_name == LibTypes.ALT_PROFANITY_CHECK:
                return self.__validate_alt_profanity_check(messages=messages, prompt=prompt)

    def __validate_vllm(self, messages=None, prompt=None):
        text = ""
        if messages:
            for i, msg in enumerate(messages):
                if i % 2 == 0:
                    text = text + "User: "
                else:
                    text = text + "Agent: "
                content = msg.get('content')
                if type(content) is str:
                    text = text + content + "\n"
                else:
                    raise NotImplementedError
        else:
            text = prompt
        prompt = self.prompt_template.format(text)
        try:
            completion = self.client.completions.create(
                model=self.served_model.value,
                prompt=prompt,
                max_tokens=3
            )
            model_response = completion.choices[0].text
            validation_passed = self.__parse_model_response(model_response)
            response = {
                "status": "success",
                "validation_passed": validation_passed,
                "validated_output": messages if messages else prompt
            }
            if not validation_passed:
                response["validation_message"] = "Conversation Contains Profane language"
            return response
        except Exception as e:
            # TODO Logging
            print(e)
            return {
                "status": "error",
                "validation_message": f"Following error occured {str(e)}",
                "validation_passed": False,
                "validated_output": messages if messages else prompt
            }

    def __validate_better_profanity(self, messages=None, prompt=None):
        text = messages[-1]["content"] if messages else prompt
        is_profane = profanity.contains_profanity(text)
        if is_profane:
            return {
                "status": "error",
                "validation_message": "Profane Language found",
                "validation_passed": False,
                "validated_output": messages if messages else prompt
            }
        return {
            "status": "success",
            "validation_passed": True,
            "validated_output": messages if messages else prompt
        }

    def __validate_alt_profanity_check(self, messages=None, prompt=None):
        text = messages[-1]["content"] if messages else prompt
        is_profane = int(predict([text])[0])
        if is_profane:
            return {
                "status": "error",
                "validation_message": "Profane Language found",
                "validation_passed": False,
                "validated_output": messages if messages else prompt
            }
        return {
            "status": "success",
            "validation_passed": True,
            "validated_output": messages if messages else prompt
        }

    def __parse_model_response(self, model_response):
        chunks = [item for item in model_response.replace("\n", " ").split(" ") if item]
        no_regex = r"(?i)no"
        check_no = [chunk for chunk in chunks if re.search(no_regex, chunk)]
        if len(check_no) >= 1:
            return True
        return False
