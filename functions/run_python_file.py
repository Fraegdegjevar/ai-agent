import os
import subprocess
import sys
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
    