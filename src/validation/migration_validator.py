import os
import json
from src.local_log.log import logger


class MigrationValidator:
    def __init__(self, MigrationDirection, SourceVersion, TargetVersion, payload):
        SchemaPath = os.path.join(os.path.dirname(__file__), "..", "schemas", "framework_migration_schema.json")
        SchemaPath = os.path.abspath(SchemaPath)

        with open(SchemaPath) as f:
            self.schema = json.load(f)

        self.MigrationDirection = MigrationDirection
        self.SourceVersion = SourceVersion
        self.TargetVersion = TargetVersion
        self.payload = payload

    def log_and_append_error(self, errors, loc, msg, error_type):
        logger.log("error", msg)
        errors.append({
            "loc": [loc],
            "msg": msg,
            "type": error_type,
        })

    def get_nested_schema(self):
        """
        Traverse and retrieve the nested schema based on migration direction, source and target version.
        Returns a tuple: (validation_rules, errors)
        """
        errors = []

        if self.MigrationDirection not in self.schema:
            self.log_and_append_error(
                errors,
                "Migration Direction",
                f"Migration direction '{self.MigrationDirection}' not declared",
                "declaration_error"
            )
            return None, errors

        direction_schema = self.schema[self.MigrationDirection]

        if self.SourceVersion not in direction_schema:
            self.log_and_append_error(
                errors,
                "Source Version",
                f"Source version '{self.SourceVersion}' not declared for '{self.MigrationDirection}'",
                "declaration_error"
            )
            return None, errors

        source_schema = direction_schema[self.SourceVersion]

        if self.TargetVersion not in source_schema:
            self.log_and_append_error(
                errors,
                "Target Version",
                f"Target version '{self.TargetVersion}' not declared for source '{self.SourceVersion}'",
                "declaration_error"
            )
            return None, errors

        return source_schema[self.TargetVersion], errors

    def validate_payload(self, validation_rules):
        """
        Validate the payload against the provided validation rules.
        Returns a list of error messages.
        """
        errors = []
        for key, message in validation_rules.items():
            if not self.payload.get(key):
                self.log_and_append_error(errors, key, message, "value_error")
        return errors

    def run(self):
        if self.payload is None or not isinstance(self.payload, dict):
            return {
                "success": False,
                "message": [
                    {
                        "loc": ["Input"],
                        "msg": "Input payload is missing",
                        "type": "value_error",
                    }
                ]
            }

        validation_rules, schema_errors = self.get_nested_schema()

        if schema_errors:
            return {"success": False, "message": schema_errors}

        payload_errors = self.validate_payload(validation_rules)

        if payload_errors:
            return {"success": False, "message": payload_errors}

        logger.log("info", "Payload validated successfully")
        return {"success": True}
