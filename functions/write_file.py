import os
from google.genai import types

def write_file(working_directory, file_path, content):
    
    abs_working_dir = os.path.abspath(working_directory)
    
    target_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    
    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(target_path, "w") as f:
            f.write(content)
            f.close()
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
    
#Function declaration/schema for LLM
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes (or overwrites) a file at the file_path with content. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to be written/overwritten, relative to the working directory. Must be provided.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file. Must be provided.",
            )
        },
        required = ["file_path", "content"],
    ),
)