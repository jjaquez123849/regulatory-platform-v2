from enum import Enum


class AutomationOperator(str, Enum):

    EQUALS = "equals"

    NOT_EQUALS = "not_equals"

    CONTAINS = "contains"

    NOT_CONTAINS = "not_contains"

    GREATER_THAN = "greater_than"

    LESS_THAN = "less_than"

    GREATER_OR_EQUAL = "greater_or_equal"

    LESS_OR_EQUAL = "less_or_equal"

    IS_EMPTY = "is_empty"

    IS_NOT_EMPTY = "is_not_empty"

    STARTS_WITH = "starts_with"

    ENDS_WITH = "ends_with"

    IN_LIST = "in_list"

    NOT_IN_LIST = "not_in_list"

    REGEX = "regex"
