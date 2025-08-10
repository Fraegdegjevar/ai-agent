import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    
    
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
    
    #Choose model and submit supplied prompt to client to get response
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages
        )
    
    if verbose:
        print(f"\nUser prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print("\n" + response.text)

if __name__ == "__main__":
    main()
