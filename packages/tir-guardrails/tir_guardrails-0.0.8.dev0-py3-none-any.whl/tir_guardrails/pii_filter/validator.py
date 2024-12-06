from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

from tir_guardrails.constants import (ConfigKeys, ValidatorTypes,
                                      ValidatorModules)


class Validator:
    def __init__(self, config: dict):
        self.name = ValidatorModules.PII_FILTER.value
        self.validator_type = ValidatorTypes(config.get(ConfigKeys.VALIDATOR_TYPE.value))
        self.entities: dict = {}

        for entity in config.get(ConfigKeys.ENTITIES.value):
            self.entities[entity.get("type")] = entity.get("behavior")

        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def validate(self, messages=None, prompt=None):
        if (messages or prompt) is None:
            raise ValueError("Either 'messages' or 'prompt' must be provided.")
        text = messages[-1]["content"] if messages else prompt
        analyzer_output = self.analyzer.analyze(
            text=text,
            entities=list(self.entities.keys()),
            language='en'
        )
        analyzer_filtered_output = []
        for item in analyzer_output:
            if self.entities[item.entity_type] == "block":
                # TODO Return block messages in validated output
                return {
                    "status": "error",
                    "validation_passed": False,
                    "validated_output": messages if messages else prompt,
                    "validation_message": "Blocked Entity found in the conversation",
                }
            else:
                analyzer_filtered_output.append(item)
        anonymizer_output = self.anonymizer.anonymize(
            text=text,
            analyzer_results=analyzer_filtered_output
        )
        if messages:
            messages[-1]["content"] = anonymizer_output.text
            return {
                "status": "success",
                "validation_passed": True,
                "validated_output": messages
            }

        return {
            "status": "success",
            "validation_passed": True,
            "validated_output": anonymizer_output.text
        }
