import os

def get_files_info(working_directory, directory = "."):
   
    #Get the absolute filepath for the working directory
    absolute_working_dir = os.path.abspath(working_directory)
    
    full_dir = os.path.abspath(os.path.join(working_directory, directory))
    #Ensure that the returned directory/path is INSIDE our working directory
    # as os.path.join will ignore the first argument (working_directory) if the second
    # argument is an absolute file path.
    if not full_dir.startswith(absolute_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if os.path.isdir(full_dir) is False:
        return f'Error: "{directory}" is not a directory'
    
    try:
        files_info = []
        for obj in os.listdir(full_dir):
        #print(obj)
            filepath = os.path.join(full_dir, obj)
            file_size = os.path.getsize(filepath)
            is_dir = os.path.isdir(filepath)
            files_info.append(
                f'- {obj}: file_size={file_size} bytes, is_dir={is_dir}'
            )
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"
        