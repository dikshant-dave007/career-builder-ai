import logging
import os

import dotenv
from langchain_community.chat_models import AzureChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from src.vector_store import CareerVectorStore


dotenv.load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


class SimpleConversationMemory:
    def __init__(self, k=10):
        self.k = k
        self.messages = []

    def add_message(self, message, is_user=True):
        if is_user:
            self.messages.append(HumanMessage(content=message))
        else:
            self.messages.append(AIMessage(content=message))

        # Keep only last k messages
        if len(self.messages) > self.k:
            self.messages = self.messages[-self.k :]

    def get_conversation_history(self):
        history_text = ""
        for msg in self.messages:
            if isinstance(msg, HumanMessage):
                history_text += f"Human: {msg.content}\n"
            else:
                history_text += f"AI: {msg.content}\n"
        return history_text.strip()

    def load_memory_variables(self, inputs):
        return {"history": self.get_conversation_history()}


class CareerChatEngine:
    def __init__(self):
        logger.info("Initializing Career Chat Engine")
        try:
            self.llm = self._initialize_llm()
            self.vector_store = CareerVectorStore()
            self.memory = SimpleConversationMemory(k=10)
            self.prompt = self._create_career_prompt_template()
            logger.info("Career Chat Engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Career Chat Engine: {str(e)}")
            raise

    def _initialize_llm(self):
        logger.debug("Initializing Azure OpenAI LLM")
        try:
            deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")
            if not deployment_name:
                raise ValueError(
                    "AZURE_DEPLOYMENT_NAME environment variable is required"
                )

            llm = AzureChatOpenAI(
                deployment_name=deployment_name,
                openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
                temperature=0.3,
            )
            logger.info(
                f"Azure OpenAI LLM initialized with deployment: {deployment_name}"
            )
            return llm
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI LLM: {str(e)}")
            raise

    def _create_career_prompt_template(self):
        logger.debug("Creating career prompt template")
        return PromptTemplate(
            input_variables=["history", "input", "user_profile", "career_context"],
            template="""
            You are CareerBuilder AI, an expert career guidance assistant. Your role is to provide personalized, data-driven career advice.

            USER PROFILE:
            {user_profile}

            RELEVANT CAREER CONTEXT:
            {career_context}

            CONVERSATION HISTORY:
            {history}

            CURRENT QUERY: {input}

            Provide comprehensive, actionable career guidance including:
            1. Role recommendations based on the user's profile and goals
            2. Required skills and a step-by-step learning roadmap
            3. Current market trends and opportunities
            4. Practical next steps and resources
            5. Salary insights and career progression paths

            Focus on being specific, encouraging, and providing data-driven insights.
            Always relate your advice to the user's stated interests, skills, and goals.
            """,
        )

    def generate_response(self, user_input, chat_history, user_profile):
        logger.info(f"Generating response for user query: {user_input[:100]}...")
        try:
            # Add user message to memory
            self.memory.add_message(user_input, is_user=True)

            # Get relevant career context from vector store
            logger.debug("Searching for relevant career context")
            career_context = self.vector_store.similarity_search(
                user_input, user_profile, k=3
            )
            logger.debug(
                f"Found career context with {len(career_context.splitlines())} lines"
            )

            # Format user profile for context
            profile_text = f"""
            Interests: {user_profile['interests']}
            Skills: {user_profile['skills']}
            Experience Level: {user_profile['experience']}
            Career Goals: {user_profile['goals']}
            """

            # Create the chain
            chain = (
                {
                    "input": RunnablePassthrough(),
                    "history": lambda x: self.memory.load_memory_variables({})[
                        "history"
                    ],
                    "user_profile": lambda x: profile_text,
                    "career_context": lambda x: career_context,
                }
                | self.prompt
                | self.llm
                | StrOutputParser()
            )

            logger.debug("Generating AI response using chain")
            response = chain.invoke({"input": user_input})

            # Add AI response to memory
            self.memory.add_message(response, is_user=False)

            logger.info("AI response generated successfully")
            return response

        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            raise
