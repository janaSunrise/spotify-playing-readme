boolean_values = ("yes", "true", "1")


def parse_boolean(arg: str) -> bool:
    return arg.lower() in boolean_values
