import json
import logging
import os
import time

import dotenv
from langchain_openai import OpenAIEmbeddings
import pinecone


dotenv.load_dotenv()
# Configure logging
logger = logging.getLogger(__name__)


class CareerVectorStore:
    def __init__(self):
        logger.info("Initializing Career Vector Store")
        try:
            # Initialize embeddings
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                openai_api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
                openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
                model="text-embedding-3-large",
                dimensions=3072,
            )

            self.index_name = os.getenv("PINECONE_INDEX", "career-builder-vector-index")
            self.pc = None
            self.index = None

            # Initialize Pinecone
            self._initialize_pinecone()
            logger.info("Career Vector Store initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Career Vector Store: {str(e)}")
            raise

    def _initialize_pinecone(self):
        """Initialize Pinecone using the new SDK"""
        logger.info(f"Initializing Pinecone with index: {self.index_name}")

        try:
            # Initialize Pinecone with new API
            self.pc = pinecone.Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

            # Check existing indexes
            existing_indexes = self.pc.list_indexes()
            index_names = (
                [idx.name for idx in existing_indexes.indexes]
                if hasattr(existing_indexes, "indexes")
                else []
            )

            if self.index_name in index_names:
                logger.info(f"Connecting to existing Pinecone index: {self.index_name}")
                self.index = self.pc.Index(self.index_name)

                # Verify dimension
                try:
                    stats = self.index.describe_index_stats()
                    current_dimension = (
                        stats.dimension if hasattr(stats, "dimension") else 3072
                    )
                    if current_dimension != 3072:
                        logger.warning(
                            f"Index dimension mismatch. Expected 3072, got {current_dimension}"
                        )
                except Exception as e:
                    logger.warning(f"Could not verify index dimension: {e}")
            else:
                logger.info(
                    f"Creating new Pinecone index: {self.index_name} with dimension 3072"
                )
                self.pc.create_index(
                    name=self.index_name,
                    dimension=3072,
                    metric="cosine",
                    spec=pinecone.ServerlessSpec(cloud="aws", region="us-east-1"),
                )
                time.sleep(10)
                self.index = self.pc.Index(self.index_name)
                logger.info("Pinecone index created successfully")

            logger.info("✅ Pinecone initialized successfully")

        except Exception as e:
            logger.error(f"Error setting up Pinecone: {str(e)}")
            raise

    def similarity_search(self, query, user_profile, k=3):
        """Simple search that returns success message"""
        logger.info("Pinecone connection test - search functionality")
        return "✅ Pinecone connection established successfully! Career data storage is ready."
