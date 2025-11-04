from datetime import datetime
import json
import logging
import os

from langchain_community.chat_models import AzureChatOpenAI

from src.market_insights import MarketInsightEngine


# Configure logging
logger = logging.getLogger(__name__)


class NewsletterGenerator:
    def __init__(self):
        logger.info("Initializing Newsletter Generator")
        try:
            deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")
            if not deployment_name:
                raise ValueError(
                    "AZURE_DEPLOYMENT_NAME environment variable is required"
                )

            self.llm = AzureChatOpenAI(
                deployment_name=deployment_name,
                openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
                temperature=0.7,
            )
            self.market_insights = MarketInsightEngine()
            logger.info(
                f"Newsletter Generator initialized with deployment: {deployment_name}"
            )
        except Exception as e:
            logger.error(f"Failed to initialize Newsletter Generator: {str(e)}")
            raise

    def generate_newsletter(self, user_profile):
        """Generate personalized career newsletter"""
        logger.info("Starting newsletter generation")

        try:
            # Get relevant news and trends
            logger.debug("Fetching market insights and news")
            news_articles = self.market_insights.get_tech_news()
            trends = self.market_insights.get_industry_trends("technology")

            logger.debug(
                f"Retrieved {len(news_articles)} news articles and {len(trends)} trends"
            )

            newsletter_prompt = f"""
            Create a personalized career development newsletter for a professional with this profile:

            INTERESTS: {user_profile['interests']}
            SKILLS: {user_profile['skills']}
            EXPERIENCE: {user_profile['experience']}
            GOALS: {user_profile['goals']}

            LATEST INDUSTRY NEWS:
            {json.dumps(news_articles, indent=2)}

            MARKET TRENDS:
            {chr(10).join(trends)}

            Please generate a comprehensive newsletter that includes:
            1. Personalized greeting
            2. Key industry updates relevant to their profile
            3. Skill development recommendations
            4. Job market insights
            5. Learning resources and next steps
            6. Motivational career advice

            Format it professionally with clear sections and actionable insights.
            Make it engaging and personalized to the user's specific interests and goals.
            Include specific course recommendations, tools to learn, and practical steps.
            """

            logger.debug("Generating newsletter content using LLM")
            response = self.llm.invoke(newsletter_prompt)
            logger.info("Newsletter generated successfully")

            return response.content

        except Exception as e:
            logger.error(f"Failed to generate newsletter: {str(e)}")
            raise
