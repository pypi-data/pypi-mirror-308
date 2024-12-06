from langchain_groq import ChatGroq
import json
import re



class DocumentAnalyzer:
    """A class to analyze documents and extract question-answer pairs in JSON format."""

    def __init__(self, api_key, model_name="llama-3.1-70b-versatile"):
        """
        Initializes the DocumentAnalyzer with an LLM model.
        
        Parameters:
        api_key: API key for Langchain groq.
        """
        self.llm = ChatGroq(groq_api_key=api_key, model_name=model_name)

    # def generate_prompt(self, text_chunk):
    #     """Generates a prompt for analyzing a chunk of text."""
    #     return f"""
    #         Analyze the text: {text_chunk}

    #         Extract key information and formulate a list of question-answer pairs in JSON format. 

    #         **Example:** 

    #         "question": "What is formed when dilute sulphuric acid is added to zinc granules?",
    #         "answer": "Change in state, change in colour, evolution of a gas, change in temperature."
    #     """

    def analyze_documents(self, prompt ,documents,step_num=10):
        """
        Analyzes the documents and extracts question-answer pairs in JSON format.

        Parameters:
        documents (list): List of document objects with page content.

        Returns:
        list: A list of extracted question-answer pairs in JSON format.
        """
        json_data_list = []

        for i in range(8, len(documents), step_num):
            # Create a chunk of text from 10 consecutive documents
            text_chunk = [documents[i + k].page_content for k in range(10)]
            # prompt = self.generate_prompt(text_chunk)

            # Invoke the LLM with the generated prompt and extract the JSON response
            input_text = self.llm.invoke(prompt).content
            json_data_list.append(self.extract_json_from_text(input_text))

        return json_data_list

    def extract_json_from_text(self,input_text):

        """
        Extract JSON content from text enclosed within triple backticks and return it as a Python object.

        Args:
        input_text (str): The input text containing JSON content within triple backticks.

        Returns:
        dict or list: Parsed JSON data as a Python object if extraction is successful.
        None: If JSON content is not found or parsing fails.
        """
        # Regex pattern to find JSON content within triple backticks
        json_pattern = r'```(.*?)```'
        match = re.search(json_pattern, input_text, re.DOTALL)

        if match:
            json_str = match.group(1).strip()  # Extract JSON string and remove extra whitespace
            try:
                json_data = json.loads(json_str)
                return json_data
            except json.JSONDecodeError:
                print("Failed to parse JSON from the extracted string.")
                return None
        else:
            print("No JSON content found in the text.")
            return None

 