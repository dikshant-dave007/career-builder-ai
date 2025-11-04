import json
import logging
import os

from newspaper import Article
import requests


# Configure logging
logger = logging.getLogger(__name__)


class MarketInsightEngine:
    def __init__(self):
        logger.info("Initializing Market Insight Engine")
        self.news_api_key = os.getenv("NEWS_API_KEY")
        if not self.news_api_key:
            logger.info(
                "NEWS_API_KEY not found - using enhanced mock data for career insights"
            )

    def get_tech_news(self, domains="techcrunch.com,thenextweb.com", page_size=5):
        """Fetch latest technology and career news"""
        logger.info(f"Fetching tech news from domains: {domains}")

        if not self.news_api_key:
            logger.info(
                "No NEWS_API_KEY configured, using enhanced career-focused mock data"
            )
            return self._get_enhanced_mock_news()

        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "domains": domains,
                "apiKey": self.news_api_key,
                "pageSize": page_size,
                "sortBy": "publishedAt",
                "language": "en",
            }

            logger.debug("Making request to NewsAPI")
            response = requests.get(url, params=params)
            response.raise_for_status()

            articles = response.json().get("articles", [])
            logger.info(f"Retrieved {len(articles)} articles from NewsAPI")

            processed_articles = []
            for i, article in enumerate(articles[:3]):  # Process first 3 articles
                try:
                    logger.debug(
                        f"Processing article {i+1}: {article['title'][:50]}..."
                    )
                    news_article = Article(article["url"])
                    news_article.download()
                    news_article.parse()

                    processed_articles.append(
                        {
                            "title": article["title"],
                            "summary": (
                                news_article.text[:500] + "..."
                                if len(news_article.text) > 500
                                else news_article.text
                            ),
                            "url": article["url"],
                            "published_at": article["publishedAt"],
                        }
                    )
                    logger.debug(f"Successfully processed article {i+1}")
                except Exception as e:
                    logger.warning(
                        f"Failed to process article {i+1}, using fallback: {str(e)}"
                    )
                    # Fallback to description if parsing fails
                    processed_articles.append(
                        {
                            "title": article["title"],
                            "summary": article["description"] or article["title"],
                            "url": article["url"],
                            "published_at": article["publishedAt"],
                        }
                    )

            logger.info(f"Successfully processed {len(processed_articles)} articles")
            return processed_articles

        except Exception as e:
            logger.error(f"Failed to fetch news from NewsAPI: {str(e)}")
            return self._get_enhanced_mock_news()

    def _get_enhanced_mock_news(self):
        """Return enhanced mock career and tech news data"""
        logger.debug("Returning enhanced mock career news data")
        return [
            {
                "title": "AI and Machine Learning Job Market Booms with 25% Growth",
                "summary": "The demand for AI and machine learning professionals continues to surge, with companies across all industries seeking talent. Salaries for ML engineers have increased by 15% in the past year alone.",
                "url": "https://career-trends.example.com/ai-ml-growth-2024",
                "published_at": "2024-01-15T10:00:00Z",
            },
            {
                "title": "Remote Work Revolution: Tech Companies Embrace Global Talent",
                "summary": "Technology companies are increasingly adopting remote-first policies, opening up opportunities for professionals worldwide. This shift has led to a 40% increase in remote tech job postings.",
                "url": "https://career-trends.example.com/remote-work-tech",
                "published_at": "2024-01-14T15:30:00Z",
            },
            {
                "title": "Cloud Computing Certifications See Record Demand",
                "summary": "AWS, Azure, and Google Cloud certifications are becoming essential for cloud engineers, with certified professionals commanding 20-30% higher salaries. The cloud job market is expected to grow by 30% this year.",
                "url": "https://career-trends.example.com/cloud-certifications-demand",
                "published_at": "2024-01-13T09:15:00Z",
            },
            {
                "title": "Data Engineering Overtakes Traditional Data Science in Hiring",
                "summary": "Companies are prioritizing data engineering roles to build robust data infrastructure, with a 35% increase in data engineering positions compared to traditional data science roles.",
                "url": "https://career-trends.example.com/data-engineering-growth",
                "published_at": "2024-01-12T14:20:00Z",
            },
        ]

    def get_industry_trends(self, industry="technology"):
        """Get trends for specific industry"""
        logger.info(f"Fetching industry trends for: {industry}")
        try:
            trends = {
                "technology": [
                    "AI and Machine Learning roles growing at 25% annually with high salary premiums",
                    "Cloud computing skills in high demand across all sectors - AWS, Azure, GCP",
                    "Remote work opportunities increased by 40% in tech roles since 2020",
                    "Cybersecurity roles critical across industries with 30% growth expected",
                    "Full-stack developers remain most in-demand with JavaScript/React leading",
                    "Low-code/no-code platforms creating new developer roles and opportunities",
                ],
                "data_science": [
                    "MLOps becoming essential skill for data scientists moving to production",
                    "Data engineering roles growing 35% faster than pure data science positions",
                    "Real-time data processing and streaming skills increasingly valuable",
                    "Business analytics merging with data science in enterprise organizations",
                    "Python and SQL remain foundational skills with 95% of jobs requiring them",
                ],
                "software_development": [
                    "Full-stack JavaScript developers command highest starting salaries",
                    "Mobile app development shifting towards React Native and Flutter",
                    "DevSecOps integrating security into entire development lifecycle",
                    "Microservices and containerization becoming enterprise standards",
                    "TypeScript adoption growing rapidly in enterprise codebases",
                ],
            }

            industry_trends = trends.get(
                industry,
                ["Strong growth across all tech sectors with competitive salaries"],
            )
            logger.info(f"Found {len(industry_trends)} trends for {industry}")
            return industry_trends

        except Exception as e:
            logger.error(f"Error fetching industry trends: {str(e)}")
            return [
                "Technology sector continues to show strong growth with abundant opportunities"
            ]
