def run_python_file(working_directory, file_path, args=[]):
    import os
    import sys
    import subprocess

    full_path = os.path.join(working_directory, file_path)
    abs_full_path = os.path.abspath(full_path)
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_full_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            [sys.executable, full_path] + args,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.stdout == '' and result.stderr == '':
            output = 'No output produced.'
        else:
            output_parts = []
            if result.stdout:
                output_parts.append(f'STDOUT:\n{result.stdout.strip()}')
            if result.stderr:
                output_parts.append(f'STDERR:\n{result.stderr.strip()}')
            output = '\n\n'.join(output_parts)
        
        if result.returncode != 0:
            output += f'\n\nProcess exited with code {result.returncode}'
        
        return output
        
    except subprocess.TimeoutExpired:
        return f'Error: Python file "{file_path}" execution timed out after 30 seconds.'
    except subprocess.CalledProcessError as e:
        return f'Error: Python file "{file_path}" failed with exit code {e.returncode}.'
    except Exception as e:
        return f'Error: executing Python file "{file_path}": {str(e)}'
    
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file. The working directory is injected automatically by the tool runtime; only provide file_path and optional args.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the Python file.",
            ),
        },
    ),
)