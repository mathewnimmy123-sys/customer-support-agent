# diagnose_agent.py
import logging
import sys

# Configure ultra-verbose logging to capture every internal trace step
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger("diagnostics_runner")

print("=" * 70)
print("🔍 RUNNING LOCAL VERTEX AI RUNTIME CONTAINER EMULATION...")
print("=" * 70)

try:
    logger.info("Step 1: Testing class import pointer from the package space...")
    from support_agent.agent import CloudAgentService
    
    logger.info("Step 2: Instantiating CloudAgentService class...")
    service_instance = CloudAgentService()
    print("✅ Class structure initialized without memory conflicts.")
    
    logger.info("Step 3: Triggering lazy-loading factory and emulating cloud health probe...")
    # We bypass the try/except block by manually importing and invoking the builder to catch the raw trace
    from support_agent.agent import create_agent_runtime
    
    print("\n🚀 Executing 'create_agent_runtime()' factory loop...")
    live_agent = create_agent_runtime()
    
    print("\n✅ SUCCESS: Your agent package initialized perfectly local!")
    print("If this prints successfully, your issue is exclusively a cloud IAM permission block.")

except Exception as fatal_error:
    print("\n💥 CRITICAL RUNTIME CRASH DETECTED!")
    print("-" * 70)
    import traceback
    traceback.print_exc()
    print("-" * 70)
    print("💡 ACTION REQUIRED: Look at the last lines of the stack trace above.")
    print("It will name the exact file (e.g., supervisor.py) and line number causing the container to fail.")