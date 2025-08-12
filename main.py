import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file


def main():

    #System prompt to the model/LLM. Note that this is guidance to the model on how to 
    # assist the user, frames the conversation, and comes before the user prompt.
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    
    # args[0] is always the name of the script. args[1] is the first CL argument supplied
    verbose = "--verbose" in sys.argv
    args = []
    
    #Collect non --flag args from 1st element (avoid script)
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg) 
    
    user_prompt = " ".join(args)
    
    #If no prompt supplied, throw error
    if not args:
        print("No prompt supplied! Please supply a prompt.")
        print('Example usage: python main.py "your prompt here"')
        sys.exit(1)   
    
    #Set types.Content so we can supply roles and keep track of conversation
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    #For loading .env into sys environment variables
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    #The google genai client
    client = genai.Client(api_key=api_key)
    
    #List of available function declarations/schema for the model
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )
    
    #Choose model and submit supplied prompt to client to get response
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )
    
    if verbose:
        print(f"\nUser prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    #Check the function calls made by the LLM and print them out, else print the response text.
    if response.function_calls:
        for function_call in response.function_calls:
            args_string = function_call.args if function_call.args else ''
            print(f"Calling function: {function_call.name}({args_string})")
    elif response.text:
        print("\nRESPONSE: " + response.text)
    

if __name__ == "__main__":
    main()
