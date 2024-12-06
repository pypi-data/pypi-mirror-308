from fuzzysearch import find_near_matches

from tir_guardrails.constants import (ConfigKeys, ValidatorTypes,
                                      LibTypes, ValidatorModules)


class Validator:
    def __init__(self, config: dict):
        self.name = ValidatorModules.PHRASE_FILTER.value
        self.validator_type = ValidatorTypes(config.get(ConfigKeys.VALIDATOR_TYPE.value))
        self.lib_name = LibTypes(config.get(ConfigKeys.LIB_NAME.value, None))
        self.pharseslist = config.get(ConfigKeys.PHRASESLIST.value, None)

    def validate(self, messages=None, prompt=None):
        if (messages or prompt) is None:
            raise ValueError("Either 'messages' or 'prompt' must be provided.")
        if self.lib_name is LibTypes.FUZZYSEARCH:
            return self.__validate_fuzzysearch(messages=messages, prompt=prompt)

    def __validate_fuzzysearch(self, messages=None, prompt=None):
        text = messages[-1]["content"] if messages else prompt
        spaceless_text = text.replace(" ", "").lower()
        matched_phrases = []
        for phrase in self.pharseslist:
            spaceless_phrase = phrase.replace(" ", "").lower()
            matches = find_near_matches(spaceless_phrase, spaceless_text, max_l_dist=1)
            if len(matches) >= 1:
                matched_phrases.append(phrase)

        if len(matched_phrases) >= 1:
            return {
                "status": "error",
                "validation_passed": False,
                "validation_message": f"Following blocked phrases found {', '.join(matched_phrases)}",
                "validated_output": prompt if prompt else messages
            }
        return {
            "status": "success",
            "validation_passed": True,
            "validated_output": prompt if prompt else messages
        }
