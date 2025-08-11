import os
from functions.config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    
    target_path = os.path.join(abs_working_dir, file_path)
    
    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_path, "r") as f:
            #Read max chars + 1 so we know whether the file was > MAX_CHARS
            # in length and can add in the truncation text
            file_content_string = f.read(MAX_CHARS + 1)
            f.close()
        
        trunc_text = f'[...File "{target_path}" truncated at {MAX_CHARS} characters]'
        
        if len(file_content_string) > MAX_CHARS:
            file_content_string = file_content_string[:MAX_CHARS + 1] + trunc_text
        
        return file_content_string
    except Exception as e:
        return f'Error: {e}'

        