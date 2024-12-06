from transformers import pipeline

from tir_guardrails.constants import (ConfigKeys, ValidatorTypes, ValidatorModules)


class Validator:
    def __init__(self, config: dict):
        self.name = ValidatorModules.WORD_FILTER.value
        self.validator_type = ValidatorTypes(config.get(ConfigKeys.VALIDATOR_TYPE.value))
        self.wordlist = config.get(ConfigKeys.WORDLIST.value, None)
        self.extra: dict = config.get(ConfigKeys.CONFIG.value)

        if self.validator_type is ValidatorTypes.CLASSIFIER:
            self.model = self.extra.get(ConfigKeys.MODEL.value)
            self.threshold = self.extra.get(ConfigKeys.THRESHOLD.value)
            self.pipe = pipeline(model=self.model)
        elif self.validator_type is ValidatorTypes.ALGO:
            raise NotImplementedError()

    def validate(self, messages=None, prompt=None):
        if (messages or prompt) is None:
            raise ValueError("Either 'messages' or 'prompt' must be provided.")

        if self.validator_type is ValidatorTypes.CLASSIFIER:
            return self.__validate_classifier(messages=messages, prompt=prompt)

    def __validate_classifier(self, messages=None, prompt=None):
        text = messages[-1]["content"] if messages else prompt
        predictions = self.pipe(text, candidate_labels=self.wordlist, multi_label=True)
        scores = predictions['scores']

        for score in scores:
            if score > self.threshold:
                return {
                    "status": "error",
                    "validation_message": "Blocked Word Found",
                    "validation_passed": False,
                    "validated_output": messages if messages else prompt
                }
        return {
            "status": "success",
            "validation_passed": True,
            "validated_output": messages if messages else prompt
        }
