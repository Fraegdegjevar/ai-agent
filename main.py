import os
import sys
from dotenv import load_dotenv
from google import genai

def main():
    
    #Collect command-line arguments supplied when script called
    # args[0] is always the name of the script. args[1] is the first CL argument supplied
    args = sys.argv[1:]
    
    #If no prompt supplied, throw error
    if not args:
        print("No prompt supplied! Please supply a prompt.")
        print('Example usage: python main.py "your prompt here"')
        sys.exit(1)
    
    #For loading .env into sys environment variables
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    #The google genai client
    client = genai.Client(api_key=api_key)
    
    print(f"Submitting prompt: {args[1]}")
    
    #Choose model and submit supplied prompt to client to get response
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=args[1]
        )
    
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
