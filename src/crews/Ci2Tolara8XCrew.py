import sys

from datetime import datetime

from src.base_crews.Ci2ToLara8XCrewBase import Ci2ToLara8XCrewBase
from src.local_log.log import logger

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
class Ci2ToLara8XCrew():
    def __init__(self,payload):
        """
        Initialize the Ci2ToLara8XCrew class.
        This class is designed to run the Ci2ToLara8XCrewBase with specific inputs.
        """
        self.inputs = {
        'source_version': payload.get('source_version'),
        'target_version': payload.get('target_version'),
        'migration_code': payload.get('migration_code'),
        'model': payload.get('model'),
        }
        

    def run(self):
        """
        Run the crew.
        """
        try:
            Ci2ToLara8XCrewBase().crew().kickoff(inputs=self.inputs)
        except Exception as e:
            logger.log('error', f"An error occurred while running the crew: {e}")
            raise Exception(f"An error occurred while running the crew: {e}")


    # def train(self):
    #     """
    #     Train the crew for a given number of iterations.
    #     """
    #     inputs = {
    #         "topic": "AI LLMs",
    #         'current_year': str(datetime.now().year)
    #     }
    #     try:
    #         Ci2ToLara8XCrewBase().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    #     except Exception as e:
    #         raise Exception(f"An error occurred while training the crew: {e}")

    # def replay(self):
    #     """
    #     Replay the crew execution from a specific task.
    #     """
    #     try:
    #         Ci2ToLara8XCrewBase().crew().replay(task_id=sys.argv[1])

    #     except Exception as e:
    #         raise Exception(f"An error occurred while replaying the crew: {e}")

    # def test(self):
    #     """
    #     Test the crew execution and returns the results.
    #     """
    #     inputs = {
    #         "topic": "AI LLMs",
    #         "current_year": str(datetime.now().year)
    #     }
        
    #     try:
    #         Ci2ToLara8XCrewBase().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    #     except Exception as e:
    #         raise Exception(f"An error occurred while testing the crew: {e}")
