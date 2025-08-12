import os
import subprocess
import sys
from google.genai import types
from functions.config import EXEC_TIMEOUT

def run_python_file(working_directory, file_path, args=[]):
    
    abs_working_dir = os.path.abspath(working_directory)
    
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not full_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        #Note we use sys.executable here to ensure that the version of python used to execute
        # this subprocess is the SAME VERSION that is used to invoke this function call
        # i.e in venvs like when using uv, we execute the subprocess with the same python executable
        #we used to run this script.
        result = subprocess.run(args=[sys.executable, full_path] + args, timeout=EXEC_TIMEOUT,
                            capture_output=True, text = True,
                            cwd=abs_working_dir)
    except Exception as e:
        return f'Error: executing Python file: {e}'
    
    
    output = []
    #Stripping trailing whitespace and inserting one newline char to standardise output whitespace.
    if result.stdout:
          output.append(f'STDOUT:\n{result.stdout.rstrip()}')
          
    if result.stderr:
        output.append(f'STDERR:\n{result.stderr.rstrip()}')
    
    if not output:
        output.append("No output produced.")
    
    if result.returncode != 0:
        output.append(f'Process exited with code {result.returncode}')
    
    return "\n".join(output)

#Function declaration/schema for LLM
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file (.py) using subprocess with the provided args. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file to be run, relative to the working directory. Must be provided.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The arguments to be supplied to the python file being run. Optional, so you may run a file with no args.",
                items=types.Schema(type=types.Type.STRING), #defines the types that can be in arg list
                nullable=True
            )
        },
        required = ["file_path"],
    ),
)