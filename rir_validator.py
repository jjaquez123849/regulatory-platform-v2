from jsonschema import Draft202012Validator

from app.rir.rir_1_0_schema import RIR_1_0_SCHEMA


def validate_rir(rir: dict) -> dict:
    validator = Draft202012Validator(RIR_1_0_SCHEMA)

    errors = sorted(
        validator.iter_errors(rir),
        key=lambda error: error.path,
    )

    if not errors:
        return {
            "is_valid": True,
            "errors": [],
        }

    return {
        "is_valid": False,
        "errors": [
            {
                "path": ".".join(str(part) for part in error.path),
                "message": error.message,
            }
            for error in errors
        ],
    }
