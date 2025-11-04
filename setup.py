import logging
import os

from dotenv import load_dotenv

from src.utils.helpers import get_azure_deployment_info, validate_environment_variables
from src.vector_store import CareerVectorStore


load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def setup_application():
    logger.info("Starting CareerBuilder AI setup process")

    try:
        load_dotenv()
        logger.info("Environment variables loaded")

        # Use helper function to validate environment
        validate_environment_variables()

        # Log Azure deployment info
        azure_info = get_azure_deployment_info()
        logger.info(f"Azure Deployment: {azure_info['deployment_name']}")
        logger.info(f"Azure Endpoint: {azure_info['endpoint']}")
        logger.info(f"Azure API Version: {azure_info['api_version']}")

        # Initialize Pinecone with career data
        logger.info("Initializing vector store with career data")
        vector_store = CareerVectorStore()

        logger.info("✅ CareerBuilder AI setup complete!")
        logger.info("🎯 You can now run: streamlit run app.py")

    except Exception as e:
        logger.error(f"❌ Application setup failed: {str(e)}")
        raise


if __name__ == "__main__":
    setup_application()
