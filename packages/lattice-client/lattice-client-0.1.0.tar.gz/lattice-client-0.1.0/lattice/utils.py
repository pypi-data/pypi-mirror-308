import base64
import json
import re
from uuid import uuid4


def generate_id():
    return str(uuid4())


def render_snake_case_to_camel_case(match):
    return match.group()[0] + match.group()[2].upper()


def snake_case_to_camel_case(data):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_key = re.sub(r"[a-z]_[a-z]", render_snake_case_to_camel_case, key)
            new_dict[new_key] = snake_case_to_camel_case(value)
        return new_dict
    if isinstance(data, (list, tuple)):
        for i in range(len(data)):
            data[i] = snake_case_to_camel_case(data[i])
        return data
    return data


first_cap_re = re.compile("(.)([A-Z][a-z]+)")
all_cap_re = re.compile("([a-z0-9])([A-Z])")


def parse_camel_case_to_snake_case(name):
    s1 = first_cap_re.sub(r"\1_\2", name)
    return all_cap_re.sub(r"\1_\2", s1).lower()


def camel_case_to_snake_case(data):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_key = parse_camel_case_to_snake_case(key)
            new_dict[new_key] = camel_case_to_snake_case(value)
        return new_dict
    if isinstance(data, (list, tuple)):
        for i in range(len(data)):
            data[i] = camel_case_to_snake_case(data[i])
        return data
    return data


def create_token_string(method: str, value: str):
    try:
        token_bytes = json.dumps(
            {
                "tenant_id": "lattice",
                "method": method,
                "value": value,
                "scope": "all",
            }
        ).encode("utf-8")
        return base64.b64encode(token_bytes).decode("utf-8")
    except Exception as error:
        raise ValueError("Failed to create token string") from error


def create_token_header(api_key: str):
    try:
        return f"Bearer {create_token_string('token', api_key)}"
    except Exception as error:
        raise ValueError("Failed to create token header") from error


def create_access_token_header(access_token: str):
    try:
        return f"Bearer {create_token_string('access-token', access_token)}"
    except Exception as error:
        raise ValueError("Failed to create access token header") from error
