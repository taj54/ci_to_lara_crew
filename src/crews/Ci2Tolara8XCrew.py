import sys
import warnings

from datetime import datetime

from base_crews.CiToLaraCrew import CiToLaraCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
class Ci2Tolara8XCrew():
    def __init__(self,payload):
        """
        Initialize the Ci2Tolara8XCrew class.
        This class is designed to run the CiToLaraCrew with specific inputs.
        """
        self.inputs = {
            'topic': 'AI LLMs',
            'current_year': str(datetime.now().year)
        }
        self.description = payload.get('topic', 'AI LLMs')
        

    def run(self):
        """
        Run the crew.
        """
        try:
            CiToLaraCrew().crew().kickoff(inputs=self.inputs)
        except Exception as e:
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
    #         CiToLaraCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    #     except Exception as e:
    #         raise Exception(f"An error occurred while training the crew: {e}")

    # def replay(self):
    #     """
    #     Replay the crew execution from a specific task.
    #     """
    #     try:
    #         CiToLaraCrew().crew().replay(task_id=sys.argv[1])

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
    #         CiToLaraCrew().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    #     except Exception as e:
    #         raise Exception(f"An error occurred while testing the crew: {e}")
