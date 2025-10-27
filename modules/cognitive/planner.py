import json
from modules.llm.lmstudio_client import LMStudioClient

class Planner:
    """
    Uses the LLM to create a structured, step-by-step plan to achieve a high-level goal.
    """
    def __init__(self):
        self.client = LMStudioClient()

    def create_plan(self, goal):
        """
        Generates a project plan in JSON format based on the user's goal.
        """
        system_prompt = """
You are an expert software architect. Your job is to break down a user's high-level software development goal into a series of clear, actionable tasks.

You MUST respond with ONLY a valid JSON array of task objects. Do not include any other text, explanations, or markdown fences around the JSON.

Each task object in the JSON array must have the following structure:
- "task_id": A short, descriptive ID for the task (e.g., "create_html_file").
- "type": The type of action to be performed. For now, always use "create_file".
- "description": A concise description of what the task entails.
- "file_path": The relative path where the file should be created (e.g., "src/index.html").
- "code_prompt": A detailed prompt for another AI to write the code for this specific file. This prompt should contain all necessary instructions, including technologies, libraries, and specific content requirements.
"""

        print("[STEP 2] Using AI to create a project build plan...")
        plan_str = self.client.query(
            prompt=f"Create a plan for the following goal: {goal}",
            system_prompt=system_prompt,
            temperature=0.2,
            is_json=True
        )

        try:
            plan = json.loads(plan_str)
            print("   -> Plan created successfully.")
            return plan
        except json.JSONDecodeError:
            print(f"Error: Failed to decode the JSON plan from the LLM response.")
            print(f"Received: {plan_str}")
            return None