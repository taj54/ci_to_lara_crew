import json
from local_log.log import logger


class Validate:

    def __init__(self,ModuleName, APIVersion, EndpointName, Payload):
        with open("functionInputValidation.json") as f:
            self.InputValidation = json.load(f)
            self.ModuleName = ModuleName
            self.APIVersion = APIVersion
            self.EndpointName = EndpointName
            self.Payload = Payload

    def run(self):
        if self.Payload is None:
            missing_payload_error = {
                "loc": ["Input"],
                "msg": "Input payload is missing",
                "type": "value_error",
            }
            return {"success": False, "message": [missing_payload_error]} # Return as a list for consistency
        else:
            missing_inputs_errors = []

            module_names_list = list(self.InputValidation.keys())
            if self.ModuleName not in module_names_list:
                module_undeclared_error = {
                    "loc": ["Module Name"],
                    "msg": f"Module Name '{self.ModuleName}' not declared",
                    "type": "declaration_error", # Changed to declaration_error for clarity
                }
                # logger.LogIt("error", f"Module Name not declared - {self.ModuleName}") # Uncomment if logger is available
                missing_inputs_errors.append(module_undeclared_error)
            else:
                self.InputValidation = self.InputValidation.get(self.ModuleName, {})
                api_version_names_list = list(self.InputValidation.keys())
                if self.APIVersion not in api_version_names_list:
                    api_version_undeclared_error = {
                        "loc": ["API Version"],
                        "msg": f"API Version '{self.APIVersion}' not declared for module '{self.ModuleName}'",
                        "type": "declaration_error",
                    }
                    # logger.LogIt("error", f"API Version not declared - {self.APIVersion}") # Uncomment if logger is available
                    missing_inputs_errors.append(api_version_undeclared_error)
                else:
                    self.InputValidation = self.InputValidation.get(
                        self.APIVersion, {}
                    )
                    endpoint_names_list = list(self.InputValidation.keys())
                    if self.EndpointName not in endpoint_names_list:
                        endpoint_undeclared_error = {
                            "loc": ["Endpoint Name"],
                            "msg": f"Endpoint Name '{self.EndpointName}' not declared for API version '{self.APIVersion}'",
                            "type": "declaration_error",
                        }
                        # logger.LogIt("error", f"Endpoint Name not declared - {self.EndpointName}") # Uncomment if logger is available
                        missing_inputs_errors.append(endpoint_undeclared_error)

                    else:
                        required_inputs = self.InputValidation.get(self.EndpointName, {})
                        for key, message in required_inputs.items():
                            if self.Payload.get(key) is None or self.Payload.get(key) == "":
                                missing_inputs_errors.append(
                                    {"loc": [key], "msg": message, "type": "value_error"}
                                )

            if len(missing_inputs_errors) > 0:
                return {"success": False, "message": missing_inputs_errors}

            return {"success": True}
