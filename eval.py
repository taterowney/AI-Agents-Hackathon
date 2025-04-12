import re
import openai

def call_reasoning_model(prompt: str, delimiters: list[tuple[str, str]], model_name: str = "my_model"):
    """
    Calls a locally hosted vLLM model via OpenAI's Python library on port 8000.

    Parameters:
    -----------
    prompt : str
        The prompt (or question) to send to the model.
    delimiters : list of (str, str)
        A list of (start, end) delimiter pairs used to extract text from the model's output.
        Example: [("<code>", "</code>"), ("<answer>", "</answer>")]
    model_name : str
        The name of the model. Adjust this to match how you have vLLM configured.

    Returns:
    --------
    output_text : str
        The raw text response from the model.
    extracted_contents : dict
        A dictionary where the key is the (start_delim, end_delim) pair,
        and the value is a list of all text segments found between those delimiters.
    """

    # Point the OpenAI client to your locally hosted vLLM server
    openai.api_base = "http://localhost:8000/v1"
    openai.api_key = "unused_api_key"  # vLLM doesn't verify API keys by default

    # Create completion (for chat-based model, you could use openai.ChatCompletion.create)
    response = openai.Completion.create(
        model=model_name,
        prompt=prompt,
        max_tokens=256,
        temperature=0.7
    )

    # Grab the text from the completion
    output_text = response.choices[0].text

    # Extract content found between each pair of delimiters
    extracted_contents = {}
    for (start_delim, end_delim) in delimiters:
        pattern = re.compile(re.escape(start_delim) + r'(.*?)' + re.escape(end_delim), re.DOTALL)
        matches = pattern.findall(output_text)
        extracted_contents[(start_delim, end_delim)] = matches

    return output_text, extracted_contents

if __name__ == "__main__":
    pass