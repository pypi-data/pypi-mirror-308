
class PromptGenerator:
    """A class to generate prompts for analyzing text and extracting question-answer pairs."""
    
    def __init__(self):
        # Example template for question-answer extraction
        self.template = """
            Analyze the text: {text}
            Extract key information and formulate a list of question-answer pairs in JSON format.
            Example:
            "question": "What is formed when dilute sulphuric acid is added to zinc granules?",
            "answer": "Change in state, change in colour, evolution of a gas, change in temperature."
        """
    
    def generate_prompt(self, text):
        """Generates a prompt by injecting the specified text into the template."""
        return self.template.format(text=text)
