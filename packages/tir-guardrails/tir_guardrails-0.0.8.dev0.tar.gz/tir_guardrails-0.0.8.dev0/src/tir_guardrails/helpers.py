from tir_guardrails.constants import E2E_TIR_ACCESS_TOKEN


def get_default_headers() -> dict:
    return {
        "Authorization": "Bearer " + E2E_TIR_ACCESS_TOKEN,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
