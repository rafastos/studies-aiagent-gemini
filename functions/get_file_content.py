def get_file_content(working_directory, file_path):
    import os
    import sys
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    import config
    full_path = os.path.join(working_directory, file_path)
    abs_full_path = os.path.abspath(full_path)
    abs_working_dir = os.path.abspath(working_directory)
    
    if not abs_full_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory.'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(full_path, 'r') as f:
            content = f.read(config.MAX_CHARS + 1)
        
        if len(content) > config.MAX_CHARS:
            truncated_content = content[:config.MAX_CHARS]
            truncated_content += f'\n[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'
            return truncated_content
        else:
            return content
    except Exception as e:
        return f'Error: reading file "{file_path}": {str(e)}'
    
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to retrieve content from, relative to the working directory.",
            ),
        },
    ),
)