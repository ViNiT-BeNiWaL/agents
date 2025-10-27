import os
import sys
import json

# --- START OF FIX ---
# Get the absolute path of the directory containing this script.
# Since this script is in the project root, this is the correct path.
project_root = os.path.dirname(os.path.abspath(__file__))
# Add the project root to the list of paths Python searches for modules.
sys.path.insert(0, project_root)
# --- END OF FIX ---

from modules.cognitive.planner import Planner
from core.agent import Agent


class Orchestrator:
    """
    The main orchestrator that manages the entire project generation process.
    """

    def __init__(self, project_name):
        # The root directory where all generated projects will be stored
        self.projects_root = "projects"
        self.project_name = project_name
        # The full path for the current project
        self.project_path = os.path.join(self.projects_root, self.project_name)
        # The path for the task queue file
        self.task_queue_path = os.path.join(self.project_path, "task_queue.json")

        # Create the specific project folder inside the 'projects' directory
        os.makedirs(self.project_path, exist_ok=True)
        print(f"--- Starting New Project: {self.project_name} ---")
        print(f"--- Project files will be saved in: {self.project_path} ---")

    def run(self, goal):
        """
        Runs the full pipeline: Plan -> Save Queue -> Execute
        """
        # 1. Create a plan
        planner = Planner()
        plan = planner.create_plan(goal)

        if not plan:
            print("--- Project failed: Could not create a valid plan. ---")
            return

        # 2. Save the plan to the task queue file
        try:
            with open(self.task_queue_path, 'w') as f:
                json.dump(plan, f, indent=2)
            print(f"   -> Plan saved to {self.task_queue_path}")
        except IOError as e:
            print(f"--- ERROR: Could not write task queue. Details: {e} ---")
            return

        # 3. Execute the plan
        agent = Agent(self.project_path)
        agent.run(plan)

        print("\n--- Project generation complete. ---")


if __name__ == '__main__':
    print("[STEP 1] Announcing Prerequisites...")
    print(" -> Ensure LM Studio is running with a model loaded and server started.")

    project_goal = "Create a simple, modern, and responsive personal portfolio website. It should have a home section with a short bio, a projects section to showcase work, and a contact section with a simple form. Use HTML and Tailwind CSS, all in a single index.html file."

    # The project name will be derived from the goal for directory creation
    project_name = "personal_portfolio_website"

    orchestrator = Orchestrator(project_name)
    orchestrator.run(project_goal)

