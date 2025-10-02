def get_files_info(working_directory, directory="."):
    import os
    full_path = os.path.join(working_directory, directory)
    abs_full_path = os.path.abspath(full_path)
    abs_working_dir = os.path.abspath(working_directory)
    
    if not abs_full_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory.'
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory.'
    
    directory_contents = os.listdir(full_path)
    result_lines = []
    
    for item in directory_contents:
        item_path = os.path.join(full_path, item)
        is_dir = os.path.isdir(item_path)
        
        try:
            if is_dir:
                file_size = os.path.getsize(item_path)
            else:
                file_size = os.path.getsize(item_path)
        except OSError:
            file_size = 0
        
        result_lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
    
    return "\n".join(result_lines)

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)