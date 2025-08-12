from google.genai import types
from callable_functions import *
def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    
    # The function call object from the response stores the function name as a string, 
    # but the args as a dict. Unpacking the dictionary with **
    
    #First ensure working_directory is added to the args dict
    args = function_call.args
    args["working_directory"] = "./calculator"
    
    #Ensure the model is trying to call one of the functions we have exposed to it
    valid_function_name = False
    for schema in available_functions.function_declarations:
        if function_call.name == schema.name:
            valid_function_name = True
            break
    
    if valid_function_name:
        function_result = eval(f'{function_call.name}(**{args})')
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Unknown function: {function_call.name}"},
                )
            ],
        )