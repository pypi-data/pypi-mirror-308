from langchain_groq import ChatGroq
import json
import re
from langchain_groq import ChatGroq
import re
import csv
import io



class DocumentAnalyzer:
    """A class to analyze documents and extract data in various formats."""

    def __init__(self, api_key, model_name="llama-3.1-70b-versatile"):
        """
        Initializes the DocumentAnalyzer with an LLM model.
        
        Parameters:
        api_key: API key for Langchain groq.
        model_name: The name of the model to use.
        """
        self.llm = ChatGroq(groq_api_key=api_key, model_name=model_name)

    def extract_eval_data(self, documents, data_type="json", step_num=10):
        """
        Analyzes the documents and extracts data in the specified format.

        Parameters:
        documents (list): List of document objects with page content.
        data_type (str): The type of data to extract. Supports "json" or "csv".
        step_num (int): Step size to iterate through documents. Defaults to 10.

        Returns:
        list: A list of extracted data in the specified format.
        """
        data_list = []

        for i in range(8, len(documents), step_num):
            # Create a chunk of text from step_num consecutive documents
            text_chunk = documents[i]

            prompt = self.generate_prompt(text_chunk, data_type)

            # Invoke the LLM with the generated prompt and process the response
            input_text = self.llm.invoke(prompt).content

            if data_type == "json":
                data_list.append(self.extract_json_from_text(input_text))
            elif data_type == "csv":
                data_list.append(self.extract_csv_from_text(input_text))
            else:
                print("Unsupported data type for extraction. Currently only 'json' and 'csv' are supported.")
                return None

        return data_list

    def generate_prompt(self, text_chunk, data_type):
        """Generates a prompt for analyzing a chunk of text based on the specified data type."""
        if data_type == "json":
            return f"""
                Analyze the text: {text_chunk}

                Extract key information and formulate a list of question-answer pairs in JSON format.

                **Example:**

                "question": "What is formed when dilute sulphuric acid is added to zinc granules?",
                "answer": "Change in state, change in colour, evolution of a gas, change in temperature."
            """
        elif data_type == "csv":
            return f"""
                Analyze the text: {text_chunk}

                Extract key information and formulate a list of question-answer pairs in CSV format.

                **Example:**
                question,answer
                What is formed when dilute sulphuric acid is added to zinc granules?,Change in state, change in colour, evolution of a gas, change in temperature.
            """
        else:
            raise ValueError("Currently, only 'json' and 'csv' data types are supported for prompt generation.")

    def extract_json_from_text(self, input_text):
        """
        Extract JSON content from text enclosed within triple backticks and return it as a Python object.

        Args:
        input_text (str): The input text containing JSON content within triple backticks.

        Returns:
        dict or list: Parsed JSON data as a Python object if extraction is successful.
        None: If JSON content is not found or parsing fails.
        """
        json_pattern = r'```(.*?)```'
        match = re.search(json_pattern, input_text, re.DOTALL)

        if match:
            json_str = match.group(1).strip()
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                print("Failed to parse JSON from the extracted string.")
                return None
        else:
            print("No JSON content found in the text.")
            return None

    def extract_csv_from_text(self, input_text):
        """
        Extract CSV content from text enclosed within triple backticks and return it as a list of dictionaries.

        Args:
        input_text (str): The input text containing CSV content within triple backticks.

        Returns:
        list of dict: Parsed CSV data as a list of dictionaries if extraction is successful.
        None: If CSV content is not found or parsing fails.
        """
        csv_pattern = r'```(.*?)```'
        match = re.search(csv_pattern, input_text, re.DOTALL)

        if match:
            csv_str = match.group(1).strip()
            try:
                csv_data = []
                csv_file = io.StringIO(csv_str)
                reader = csv.DictReader(csv_file)
                csv_data.extend(row for row in reader)
                return csv_data
            except Exception as e:
                print(f"Failed to parse CSV from the extracted string: {e}")
                return None
        else:
            print("No CSV content found in the text.")
            return None
