import importlib.util
import sys
import os
from src.local_log.log import logger  # Your custom logger


class CrewFactory:
    """
    A factory class to centralize the creation and management of different Crew types.
    It can dynamically discover and register crew classes from the 'crews' directory.
    """

    _crews = {}  # Private dictionary to store registered crew classes

    @classmethod
    def register_crew(cls, name, crew_class):
        if not hasattr(crew_class, "run") or not callable(getattr(crew_class, "run")):
            logger.log(
                "warning",
                f"Class '{crew_class.__name__}' does not have a 'run' method. Not registering.",
            )
            return

        if name in cls._crews:
            logger.log("warning", f"Crew '{name}' is already registered. Overwriting.")
        cls._crews[name] = crew_class

    @classmethod
    def get_crew(cls, name, payload):
        crew_class = cls._crews.get(name)
        if not crew_class:
            logger.log("error", f"Crew '{name}' not found in registry.")
            return None

        try:
            instance = crew_class(payload)
            logger.log("info", f"Instantiated crew '{name}' successfully.")
            return instance
        except Exception as e:
            logger.log("error", f"Error instantiating crew '{name}': {e}")
            return None

    @classmethod
    def list_available_crews(cls):
        crew_list = list(cls._crews.keys())
        logger.log("debug", f"Available crews: {crew_list}")
        return crew_list

    @classmethod
    def _discover_crews_from_directory(cls, directory_path, base_package_path=""):
        if not os.path.isdir(directory_path):
            logger.log("error", f"Directory '{directory_path}' not found.")
            return

        for root, _, files in os.walk(directory_path):
            relative_path = os.path.relpath(root, directory_path)

            current_package_path = (
                base_package_path
                if relative_path == "."
                else os.path.join(base_package_path, relative_path).replace(os.sep, ".")
            )

            for filename in files:
                if filename.endswith(".py") and filename != "__init__.py":
                    module_name = filename[:-3]
                    full_module_name = (
                        f"{current_package_path}.{module_name}"
                        if current_package_path
                        else module_name
                    )
                    file_path = os.path.join(root, filename)

                    try:
                        spec = importlib.util.spec_from_file_location(
                            full_module_name, file_path
                        )
                        if spec is None:
                            logger.log(
                                "warning",
                                f"Could not create spec for {full_module_name} at {file_path}",
                            )
                            continue

                        module = importlib.util.module_from_spec(spec)
                        sys.modules[full_module_name] = module
                        if spec.loader:
                            spec.loader.exec_module(module)
                        else:
                            logger.log(
                                "error",
                                f"Spec loader is None for module: {full_module_name}",
                            )
                            continue

                        for attribute_name in dir(module):
                            attribute = getattr(module, attribute_name)
                            crew_id = (
                                    f"{current_package_path.replace('.', '_')}_{attribute_name.replace('Crew', '').lower()}"
                                    if current_package_path
                                    else attribute_name.replace("Crew", "").lower()
                                )
                            if (
                                isinstance(attribute, type)
                                and attribute_name.endswith("Crew")
                                and attribute.__module__ == full_module_name
                            ):
                                crew_id = (
                                    f"{current_package_path.replace('.', '_')}_{attribute_name.replace('Crew', '').lower()}"
                                    if current_package_path
                                    else attribute_name.replace("Crew", "").lower()
                                )

                                # Optional: crew_id = getattr(attribute, '_id', crew_id)
                                cls.register_crew(crew_id, attribute)

                    except Exception as e:
                        logger.log(
                            "error",
                            f"Error importing {full_module_name} from {file_path}: {e}",
                        )

    @classmethod
    def initialize(cls):
        """
        Automatically discovers and registers all crews from the 'crews' directory
        relative to the project root (2 levels up from this file).
        """
        try:
            current_dir = os.path.dirname(__file__)
            project_root = os.path.dirname(current_dir)
            crews_directory = os.path.join(project_root, "crews")
           
            cls._discover_crews_from_directory(crews_directory)

        except Exception as e:
            logger.log("error", f"Failed to initialize CrewFactory: {e}")
