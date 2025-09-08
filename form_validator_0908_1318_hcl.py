# 代码生成时间: 2025-09-08 13:18:47
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Form Data Validator
"""
from falcon import HTTPBadRequest, HTTPInternalServerError
from falcon.validate import QueryParameter, QueryParameters, BodyJSON


class FormFieldValidator:
    """
    A simple form field validator class.
    Validates required fields and ensures field values are not empty.
    """
    def __init__(self):
        self.required_fields = []
        self.validators = {}\

    def add_field(self, field_name, required=True, validator=None):
        """
        Adds a field to the validator.
        Args:
            field_name (str): The name of the field to validate.
            required (bool): Whether the field is required.
            validator (callable): A function to validate the field's value.
        """
        self.required_fields.append(field_name) if required else None
        self.validators[field_name] = validator

    def validate(self, data):
        """
        Validates the provided data against the required fields and validators.
        Args:
            data (dict): The data to validate.
        Returns:
            dict: A dictionary with the validated fields.
        Raises:
            HTTPBadRequest: If any required field is missing or invalid.
        """
        validated_data = {}
        for field in self.required_fields:
            if field not in data:
                raise HTTPBadRequest(f"Missing required field: {field}", "Field is required but not provided.")
            if not data[field]:
                raise HTTPBadRequest(f"Invalid field value for {field}: empty value.", "Field value cannot be empty.")
            if self.validators.get(field) and not self.validators[field](data[field]):
                raise HTTPBadRequest(f"Invalid field value for {field}: {data[field]}", "Field value did not pass validation.")
            validated_data[field] = data[field]

        for field, validator in self.validators.items():
            if field not in self.required_fields and field in data:
                if not validator(data[field]):
                    raise HTTPBadRequest(f"Invalid field value for {field}: {data[field]}", "Optional field value did not pass validation.")
                validated_data[field] = data[field]

        return validated_data


def validate_email(email):
    """
    Validates an email address.
    Args:
        email (str): The email address to validate.
    Returns:
        bool: True if valid, False otherwise.
    """
    import re
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))


def validate_password(password):
    "