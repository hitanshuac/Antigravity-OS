"""
Antigravity OS - Main Entrypoint
"""

import os
import sys
from dotenv import load_dotenv

from src.orchestrator.engine import ReActEngine
from src.orchestrator.llm import UniversalLLMClient

def main():
    load_dotenv()  # Load secrets from a local .env file if present
    
    # Enforce custom routing to Groq, OpenRouter, or NIM
    base_url = os.getenv("LLM_BASE_URL") 
    model = os.getenv("LLM_MODEL")

    if not base_url or not model:
        print("[!] ERROR: LLM_BASE_URL and LLM_MODEL must be explicitly set in your .env file.")
        print("We do not default to paid APIs like OpenAI.")
        sys.exit(1)

    # Auto-select the correct API key based on the provider URL
    if "groq.com" in base_url:
        api_key = os.getenv("GROQ_API_KEY")
    elif "openrouter.ai" in base_url:
        api_key = os.getenv("OPENROUTER_API_KEY")
    elif "nvidia.com" in base_url:
        api_key = os.getenv("NIM_API_KEY")
    else:
        api_key = os.getenv("LLM_API_KEY")

    if not api_key:
        print(f"[!] ERROR: No API key found for the selected provider ({base_url}).")
        print("Please check your .env file and ensure the correct API key is set.")
        sys.exit(1)

    # Get objective from CLI arguments, or default to a simple test
    objective = " ".join(sys.argv[1:])
    if not objective:
        objective = "Write a python script called hello.py that prints 'Antigravity OS is alive!'. Run the script to verify it works, then call task_complete."

    workspace = os.path.abspath(".")
    
    print("==================================================")
    print("[START] INITIALIZING ANTIGRAVITY OS")
    print(f"Workspace: {workspace}")
    print(f"Provider URL: {base_url}")
    print(f"Model: {model}")
    print(f"Objective: {objective}")
    print("==================================================\n")

    client = UniversalLLMClient(model=model, api_key=api_key, base_url=base_url)
    engine = ReActEngine(workspace_dir=workspace, llm_client=client, max_steps=15)
    
    result = engine.run_task(objective)
    
    print("\n==================================================")
    print("[END] FINAL RESULT")
    print("==================================================")
    print(result)

if __name__ == "__main__":
    main()
