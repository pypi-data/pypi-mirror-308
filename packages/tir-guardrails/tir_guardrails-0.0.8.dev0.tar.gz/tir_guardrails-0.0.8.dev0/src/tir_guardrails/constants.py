from enum import Enum
import os

# For DEV
from dotenv import load_dotenv
load_dotenv()


class ValidatorModules(Enum):
    WORD_FILTER = "word_filter"
    PROFANITY_FILTER = "profanity_filter"
    PII_FILTER = "pii_filter"
    PHRASE_FILTER = "phrase_filter"
    HARMFUL_CONTENT = "harmful_content"


VALIDATOR_MODULE_NAMES = [i.value for i in ValidatorModules]


class ConfigKeys(Enum):
    VALIDATOR_TYPE = 'validator_type'
    SERVED_MODEL = "served_model"
    MODEL = "model"
    BLOCKED_CATEGORIES = "blocked_categories"
    CATEGORY_LEVELS = "category_levels"
    CONFIG = "config"
    ENTITIES = "entities"
    LIB_NAME = "lib_name"
    WORDLIST = "wordlist"
    PHRASESLIST = "pharseslist"
    WORDLIST_FILE = "wordlist_file"
    WHITELIST_WORDS = "whitelist_words"
    OVERWRITE_WORDLIST = "overwrite_wordlist"
    PROMPT_TEMPLATE = "prompt_template"
    THRESHOLD = "threshold"
    NAME = "name"
    DESCRIPTION = "description"
    BLOCK_MESSAGE = "block_message"


class ValidatorTypes(Enum):
    EMBEDDINGS = "embedding"
    GUARD = "guard"
    LLM = "llm"
    ALGO = "algo"
    PRESIDIO = "presidio"
    LIB = "lib"
    CLASSIFIER = "classifier"


class LibTypes(Enum):
    BETTER_PROFANITY = "better-profanity"
    ALT_PROFANITY_CHECK = "alt-profanity-check"
    FUZZYSEARCH = "fuzzysearch"


class GenAIModels(Enum):
    E5_MISTRAL_7B_INSTRUCT = "e5-mistral-7b-instruct"
    LLAMA_GUARD_3_8B = "llama_guard_3_8b"
    LLAMA3_2_3B_INSTRUCT = "llama3_2_3b_instruct"


E2E_TIR_TEAM_ID = os.environ.get("E2E_TIR_TEAM_ID")
E2E_TIR_PROJECT_ID = os.environ.get("E2E_TIR_PROJECT_ID")
E2E_TIR_API_KEY = os.environ.get("E2E_TIR_API_KEY")
E2E_TIR_ACCESS_TOKEN = os.environ.get("E2E_TIR_ACCESS_TOKEN")
E2E_BASE_URL = os.environ.get("E2E_BASE_URL", "https://api.e2enetworks.com/myaccount/api/v1/teams/{E2E_TIR_TEAM_ID}/projects/{E2E_TIR_PROJECT_ID}")

OPENAI_BASE_URL = f"https://infer.e2enetworks.net/project/p-{E2E_TIR_PROJECT_ID}" + "/genai/{model}/v1"
OPENAI_API_KEY = E2E_TIR_ACCESS_TOKEN
GUARDRAILS_BASE_URL = f"{E2E_BASE_URL}/guardrails"
GUARDRAILS_FETCH_URL = GUARDRAILS_BASE_URL + "/{guardrails_id}/" + f"?apikey={E2E_TIR_API_KEY}"

THOR_GUARDRAILS_FETCH_URL = "https://api-thor.e2enetworks.net/myaccount/api/v1/gpu/teams/517/projects/1017/guardrails/{guardrails_id}/?apikey=3764aec5-d60c-45f1-977c-246203279218&active_iam=176"
THOR_AUTH_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJGSjg2R2NGM2pUYk5MT2NvNE52WmtVQ0lVbWZZQ3FvcXRPUWVNZmJoTmxFIn0.eyJleHAiOjE3NDE2OTkyOTgsImlhdCI6MTcxMDE2MzI5OCwianRpIjoiMDVhZmQ5MDItZjlhMi00ZTAwLTlmODEtYTc0NWZlYzBlMjVmIiwiaXNzIjoiaHR0cDovLzE3Mi4xNi4yMzEuMTM6ODA4MC9hdXRoL3JlYWxtcy9hcGltYW4iLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiMGMxYjhiNmMtYTE2Yi00YzU2LTg0Y2EtOWI2ZjI3YTNkNjU2IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiYXBpbWFudWkiLCJzZXNzaW9uX3N0YXRlIjoiODdmOWU5ODEtNjA5NC00ZThhLTg2NzEtZDU1NTI0Njc2MzkwIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwOi8vMTcyLjE2LjIzMS4xMzo4MDgwIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIiwiYXBpdXNlciIsImRlZmF1bHQtcm9sZXMtYXBpbWFuIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwic2lkIjoiODdmOWU5ODEtNjA5NC00ZThhLTg2NzEtZDU1NTI0Njc2MzkwIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoiYXRoYXJ2YSIsInByaW1hcnlfZW1haWwiOiJhdGhhcnZhLnBha2FkZSt0aG9yQGUyZW5ldHdvcmtzLmNvbSIsImlzX3ByaW1hcnlfY29udGFjdCI6dHJ1ZSwicHJlZmVycmVkX3VzZXJuYW1lIjoiYXRoYXJ2YS5wYWthZGUrdGhvckBlMmVuZXR3b3Jrcy5jb20iLCJnaXZlbl9uYW1lIjoiYXRoYXJ2YSIsImZhbWlseV9uYW1lIjoiIiwiZW1haWwiOiJhdGhhcnZhLnBha2FkZSt0aG9yQGUyZW5ldHdvcmtzLmNvbSJ9.d41V14Tpjy_7m6vhDqhSxKFivwc139OXcJA35bNdQ3pfDVj29tphTF9qJ-GoV0wvt2IMKeatO6oxZZEEQXMPfuUIMN19lDy1ffGRXuezsMWpffz3AN7sBSpH9DxG-1NZa48_Rfp1uEYYn0fOre8p0FuqcH1hnkROhHyf6S4mKmM"
