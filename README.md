# AI Agent with Gemini Tool Calling

A small command-line AI coding agent built in Python using Google Gemini function calling.

The agent runs in a loop, decides which tool to call, executes sandboxed file/code operations, and then returns a final natural-language answer.

## What this project does

- Accepts a user prompt from the terminal
- Uses Gemini to plan tool calls step by step
- Supports 4 core tools:
	- list files
	- read file content
	- write file content
	- run Python files
- Restricts tool access to a configured working directory for safety
- Stops after a maximum number of iterations to avoid infinite loops

By default, the tool working directory is:

- ./calculator

That means file operations are sandboxed to the calculator project unless you change configuration.

## Tech stack

- Python 3.13+
- google-genai
- python-dotenv
- uv (recommended for dependency and environment management)

## Project structure

Main agent files:

- main.py: CLI entrypoint and model interaction loop
- call_function.py: tool registry and function dispatch
- prompts.py: system prompt for model behavior
- config.py: runtime constants (working directory, max chars, max iterations)

Tool implementations:

- functions/get_files_info.py
- functions/get_file_content.py
- functions/write_file_content.py
- functions/run_python.py

Sample target codebase (sandboxed working directory):

- calculator/main.py
- calculator/pkg/calculator.py
- calculator/pkg/render.py
- calculator/tests.py

## Prerequisites

1. Python 3.13 or newer
2. A Gemini API key
3. uv installed (optional but recommended)

## Setup

1. Clone the repository
2. Create and sync dependencies
3. Configure environment variables

Example setup using uv:

```bash
uv sync
```

Set your API key in .env:

```env
GEMINI_API_KEY=your_api_key_here
```

If you do not use .env, export it in your shell before running:

```bash
export GEMINI_API_KEY="your_api_key_here"
```

## Running the agent

Basic usage:

```bash
uv run main.py "how does the calculator render results to the console?"
```

Verbose mode (shows token usage, tool calls, and intermediate behavior):

```bash
uv run main.py "list files, then read main.py and summarize it" --verbose
```

## How the loop works

1. Sends your prompt plus conversation history to Gemini
2. If Gemini requests tool calls, the agent executes them
3. Appends tool results back into conversation history
4. Repeats until Gemini returns a final text response
5. Exits early if it exceeds MAX_ITERS

## Tool behavior and constraints

All tools enforce path safety by checking that target paths stay inside the configured working directory.

### get_files_info

- Lists files and directories in a relative path
- Returns size and directory flag for each entry

### get_file_content

- Reads text file content
- Truncates output at MAX_CHARS (configurable)

### write_file

- Writes or overwrites a file
- Creates parent directories when needed
- Rejects writes outside the working directory

### run_python_file

- Executes Python files in the sandbox
- Accepts optional CLI args
- Returns STDOUT, STDERR, and non-zero exit code information

## Configuration

Edit config.py:

- WORKING_DIR: sandbox root for all tool calls (default: ./calculator)
- MAX_CHARS: file read truncation limit (default: 10000)
- MAX_ITERS: conversation loop cap (default: 20)

## Running tests

Calculator tests:

```bash
uv run calculator/tests.py
```

Tool behavior tests/helpers:

```bash
uv run test_get_files_info.py
uv run test_get_file_content.py
uv run test_write_file.py
uv run test_run_python_file.py
```

## Common troubleshooting

### GEMINI_API_KEY environment variable not set

- Ensure .env exists and contains GEMINI_API_KEY
- Or export GEMINI_API_KEY in your shell before running

### Maximum iterations reached

- The model may be stuck in planning/tool-calling loops
- Improve prompt clarity
- Inspect with --verbose
- Increase MAX_ITERS cautiously if needed

### Unknown function errors

- Confirm function name is registered in call_function.py
- Confirm schema declaration is included in available_functions

## Notes

- This project is intentionally small and educational
- It is a good base for adding:
	- diff-aware editing
	- richer test execution strategies
	- improved error classification
	- model/provider abstraction
