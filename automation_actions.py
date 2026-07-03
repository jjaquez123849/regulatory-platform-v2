from enum import Enum


class AutomationAction(str, Enum):

    CREATE_RECORD = "create_record"

    UPDATE_RECORD = "update_record"

    CREATE_PERSON = "create_person"

    CREATE_REQUEST_ITEM = "create_request_item"

    CREATE_TASK = "create_task"

    COMPLETE_TASK = "complete_task"

    SEND_NOTIFICATION = "send_notification"

    CHANGE_STATE = "change_state"

    EXECUTE_AI = "execute_ai"

    EXECUTE_EXTRACTION = "execute_extraction"

    EXECUTE_QUALITY = "execute_quality"

    CREATE_OBSERVATION = "create_observation"

    CREATE_DOCUMENT = "create_document"

    APPLY_EXTRACTION = "apply_extraction"

    EXECUTE_AUTOMATION = "execute_automation"

    WAIT = "wait"

    CALL_WEBHOOK = "call_webhook"

    PYTHON_FUNCTION = "python_function"
