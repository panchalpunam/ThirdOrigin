import json
from typing import List, Optional, Union, Dict, Any

class JsonValidator:
    def __init__(self):
        pass

    def validate_schema(self, json_file: str, schema_file: str) -> bool:
        """
        Validate a JSON file against a given schema file.

        :param json_file: Path to the JSON file to be validated
        :type json_file: str
        :param schema_file: Path to the schema file for validation
        :type schema_file: str
        :return: True if validation succeeds, False otherwise
        :rtype: bool
        """
        try:
            with open(json_file, 'r') as f_json, open(schema_file, 'r') as f_schema:
                json_data = json.load(f_json)
                schema_data = json.load(f_schema)
                
                if self.validate_required_fields(json_data, schema_data) and \
                        self.validate_at_least_one_of(json_data, schema_data) and \
                        self.validate_either_one_or_another(json_data, schema_data) and \
                        self.validate_mutually_exclusive(json_data, schema_data) and \
                        self.validate_field_values(json_data, schema_data):
                    return True
                else:
                    return False
        except Exception as e:
            print(f"Error during validation: {e}")
            return False

    def validate_required_fields(self, json_data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """
        Validate required fields.

        :param json_data: JSON data to be validated
        :type json_data: Dict[str, Any]
        :param schema: Schema for validation
        :type schema: Dict[str, Any]
        :return: True if validation succeeds, False otherwise
        :rtype: bool
        """
        required_fields = schema.get("required_fields", [])
        missing_fields = [field for field in required_fields if field not in json_data]

        if missing_fields:
            
            missing_fields_message = ", ".join([f"'{field}'" for field in missing_fields])
            print(f"Required fields {missing_fields_message} are missing.")
            return False

        return True

    def validate_at_least_one_of(self, json_data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """
        Validate at least one of many fields.

        :param json_data: JSON data to be validated
        :type json_data: Dict[str, Any]
        :param schema: Schema for validation
        :type schema: Dict[str, Any]
        :return: True if validation succeeds, False otherwise
        :rtype: bool
        """
        one_of_fields = schema.get("one_of_fields", [])
        present_fields = [field for field in one_of_fields if field in json_data]
        if not present_fields:
            print("At least one of the fields(home phone or cell phone or work phone) should be present.")
            return False
        return True

    def validate_either_one_or_another(self, json_data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """
        Validate either one field or another field.

        :param json_data: JSON data to be validated
        :type json_data: Dict[str, Any]
        :param schema: Schema for validation
        :type schema: Dict[str, Any]
        :return: True if validation succeeds, False otherwise
        :rtype: bool
        """
        either_fields = schema.get("either_fields", [])
        present_either_fields = [field for field in either_fields if field in json_data]
        if len(present_either_fields) != 1:
            print("Either one field or another field (Birth date or govt id ) should be present.")
            return False
        return True

    def validate_mutually_exclusive(self, json_data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """
        Validate mutually exclusive fields.

        :param json_data: JSON data to be validated
        :type json_data: Dict[str, Any]
        :param schema: Schema for validation
        :type schema: Dict[str, Any]
        :return: True if validation succeeds, False otherwise
        :rtype: bool
        """
        exclusive_fields = schema.get("mutually_exclusive_fields", {})
        
        for field, exclusive_field in exclusive_fields.items():
            if field in json_data and exclusive_field in json_data:
                print(f"Fields '{field}' and '{exclusive_field}' are mutually exclusive. if one phone no is present another should not be present")
                return False
        return True

    def validate_field_values(self, json_data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """
        Validate field values to be one of a set of values.

        :param json_data: JSON data to be validated
        :type json_data: Dict[str, Any]
        :param schema: Schema for validation
        :type schema: Dict[str, Any]
        :return: True if validation succeeds, False otherwise
        :rtype: bool
        """
        field_values = schema.get("field_values", {})
        for field, allowed_values in field_values.items():
            if field in json_data and json_data[field] not in allowed_values:
                print(f"Invalid value '{json_data[field]}' for field '{field}'. day can have only one of SU,MO,TU,WE,TH,FR,SA")
                return False
        return True


validator = JsonValidator()
result = validator.validate_schema("test.json", "schema.json")
print(result)
