from modules.action.file_manager import FileManager

class Agent:
    """
    The core agent that processes a queue of tasks.
    """
    def __init__(self, project_path):
        self.project_path = project_path
        # The decision engine is simple for now, we just map task types to handlers
        self.action_handlers = {
            "create_file": FileManager(project_path).create_file
        }

    def run(self, task_queue):
        """
        Executes all tasks in the provided queue.
        """
        if not task_queue:
            print("Task queue is empty. Nothing to do.")
            return

        print("\n[STEP 3] Starting agent to execute tasks...")
        for task in task_queue:
            task_type = task.get("type")
            handler = self.action_handlers.get(task_type)

            if handler:
                handler(task)
            else:
                print(f"   -> WARNING: No handler found for task type '{task_type}'. Skipping.")