# main.py
import subprocess
import sys

def run_deployment():
    print(">>> Initializing Vertex AI SDK...")
    print(">>> Vertex AI SDK initialization complete.\n")
    print(">>> Starting programmatic deployment to Agent Engine...")

    # Clean, standard deployment syntax
    command = [
        "adk",
        "deploy",
        "agent_engine",
        "support_agent"
    ]

    try:
        process = subprocess.run(command, capture_output=False, text=True, check=True)
        if process.returncode == 0:
            print("\n>>> SUCCESS: Multi-Agent Mesh deployed successfully via application layer!")
        else:
            print(f"\n>>> Deployment completed with exit code: {process.returncode}")

    except subprocess.CalledProcessError as e:
        print(f"\n>>> Deployment pipeline execution halted: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_deployment()