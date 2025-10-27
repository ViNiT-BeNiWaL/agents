import os
from modules.llm.lmstudio_client import LMStudioClient

class FileManager:
    """
    Handles file creation operations based on tasks from the plan.
    """
    def __init__(self, project_path):
        self.project_path = project_path
        self.client = LMStudioClient()

    def create_file(self, task):
        """
        Creates a file with AI-generated code.
        """
        file_path = os.path.join(self.project_path, task['file_path'])
        code_prompt = task['code_prompt']

        print(f"\n[TASK] Creating file: {task['file_path']}...")

        # Ensure the directory for the file exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        system_prompt = "You are an expert AI programmer. You write clean, efficient, and complete code based on the user's request. Only output the raw code for the requested file, without any surrounding text, explanations, or markdown code blocks."

        generated_code = self.client.query(
            prompt=code_prompt,
            system_prompt=system_prompt,
            temperature=0.3
        )

        if "Error:" in generated_code:
            print(f"   -> FAILED to generate code for {task['file_path']}.")
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(generated_code)
            print(f"   -> SUCCESS: Saved {task['file_path']}")
        except IOError as e:
            print(f"   -> ERROR: Could not write to file {file_path}. Details: {e}")