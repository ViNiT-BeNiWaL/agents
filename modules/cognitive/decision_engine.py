from modules.llm.lmstudio_client import LMStudioClient

class DecisionEngine:
    """
    The cognitive module of the agent. It uses an LLM to generate code.
    """
    def __init__(self):
        # Each decision engine gets its own LLM client
        self.llm_client = LMStudioClient()

    def generate_code(self, prompt):
        """
        Passes a code-generation task to the LM Studio client.
        """
        return self.llm_client.generate_code(prompt)