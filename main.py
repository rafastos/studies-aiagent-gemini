import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    if len(sys.argv) < 2:
        print("Usage: python main.py '<your prompt here>'")
        sys.exit(1)
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    verbose = "--verbose" in sys.argv
    max_iterations = 20
    iteration_count = 0
    
    try:
        while iteration_count < max_iterations:
            iteration_count += 1
            
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                )
            )
            
            if verbose:
                print(f"[Iteration {iteration_count}/{max_iterations}]")
                
            for candidate in response.candidates:
                messages.append(candidate.content)
            
            if response.function_calls:
                text_content = ""
                for candidate in response.candidates:
                    for part in candidate.content.parts:
                        if hasattr(part, 'text') and part.text:
                            text_content += part.text
                
                if text_content and verbose:
                    print(f"Model reasoning: {text_content}")
                
                function_responses = []
                
                for function_call in response.function_calls:
                    function_result = call_function(function_call, verbose=verbose)
                    function_responses.append(function_result)
                
                for function_response in function_responses:
                    messages.append(function_response)
                    
            elif response.text:
                if verbose:
                    prompt_tokens = response.usage_metadata.prompt_token_count
                    response_tokens = response.usage_metadata.candidates_token_count
                    print(f"User prompt: {user_prompt}")
                    print(f"Prompt tokens: {prompt_tokens}")
                    print(f"Response tokens: {response_tokens}")
                    print(f"Final response: {response.text}")
                else:
                    print(response.text)
                break
            else:
                print("Warning: Response contained neither text nor function calls")
                break
        
        if iteration_count >= max_iterations:
            print(f"Warning: Reached maximum iterations ({max_iterations}). The conversation may be incomplete.")
            
    except Exception as e:
        print(f"Error during conversation: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
    