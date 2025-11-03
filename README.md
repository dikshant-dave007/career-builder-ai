# CareerBuilder AI - AI-Powered Career Guidance Chatbot

## Overview
CareerBuilder AI is an intelligent career guidance chatbot that provides personalized career advice, skill roadmaps, and market insights using advanced AI technologies. Built with LangChain and Azure OpenAI, it serves as a 24/7 career mentor for students and professionals seeking data-driven career guidance.

## Features
- **AI Career Conversations** - Natural language interactions about career paths
- **Personalized Role Matching** - AI-driven career recommendations based on user profiles
- **Skill Gap Analysis** - Identify and bridge skill deficiencies
- **Learning Roadmaps** - Step-by-step guidance for career transitions
- **Market Trend Integration** - Real-time industry insights and job market data
- **Interactive Chat Interface** - Streamlit-based web application
- **User Profile Management** - Personalized experience based on interests and skills
- **AI-Generated Newsletters** - Weekly personalized career updates
- **Semantic Search** - Vector-based role and skill matching using Pinecone

## Technology Stack
- **Backend Framework**: Python, LangChain
- **AI Models**: Azure OpenAI GPT-4
- **Vector Database**: Pinecone
- **Web Framework**: Streamlit
- **Additional Libraries**: Newspaper3k, Tiktoken, Pydantic, Requests

## Installation

### Prerequisites
- Python 3.8 or higher
- Azure OpenAI API access
- Pinecone account
- NewsAPI key (optional)

### Step-by-Step Setup
1. Clone the repository
```text
git clone https://github.com/yourusername/CareerBuilder-AI.git
cd CareerBuilder-AI
```

2. Create virtual environment
```text
python -m venv career_ai_env
source career_ai_env/bin/activate
```

3. Install dependencies
```text
pip install -r requirements.txt
```

### Environment Configuration
Create a `.env` file in the root directory with the following variables:

```text
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint_here
AZURE_OPENAI_API_VERSION=2023-12-01-preview
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment_here
NEWS_API_KEY=your_newsapi_key_here
```

4. Initialize the Application
```text
python setup.py
```

5. Launch the Application
```text
streamlit run app.py
```
The application will open in your default browser at http://localhost:8501.

## Configuration

### Azure OpenAI Setup
1. Create an Azure OpenAI resource through Azure Portal
2. Deploy GPT-4 model in your resource
3. Obtain API key and endpoint from Azure Portal
4. Update the environment variables in your `.env` file

### Pinecone Configuration
1. Sign up for a free account at pinecone.io
2. Create a new index with dimension 1536 and cosine metric
3. Copy your API key and environment from the dashboard
4. Add them to your `.env` file

### Optional: NewsAPI Setup
1. Register for a free API key at newsapi.org
2. Add the key to your `.env` file to enable market news features

## Usage Guide

### Setting Up Your Profile
Navigate to the sidebar in the application and complete your user profile:
- Career Interests: Specify your areas of interest (e.g., AI, Web Development, Data Science)
- Current Skills: List your existing technical and soft skills
- Experience Level: Select from Student, Entry-level, Mid-level, Senior, or Executive
- Career Goals: Define your short-term and long-term career objectives

### Career Conversations
Start asking career-related questions in the chat interface. Example questions include:
- "What career path suits my skills in Python and data analysis?"
- "How can I transition from web development to AI engineering?"
- "What are the emerging trends in cloud computing careers?"
- "What skills do I need to become a machine learning engineer?"

### Getting Personalized Recommendations
The AI will provide:
- Tailored role suggestions based on your profile
- Detailed skill roadmaps with learning resources
- Market insights relevant to your interests
- Practical next steps for career advancement

### Newsletter Generation
Click the "Generate Newsletter" button in the sidebar to receive:
- AI-curated career updates specific to your interests
- Learning opportunities and course recommendations
- Industry trends and job market insights
- Downloadable newsletter in markdown format

## Project Structure
```text
CareerBuilder-AI/
├── app.py
├── requirements.txt
├── setup.py
├── .env.example
├── src/
│   ├── chat_engine.py
│   ├── vector_store.py
│   ├── market_insights.py
│   ├── newsletter_generator.py
│   └── utils/
│       └── helpers.py
├── data/
│   └── sample_roles.json
└── templates/
    └── index.html
```

## API Integration
The application integrates with multiple APIs:
- Azure OpenAI API for AI-powered conversations
- Pinecone API for vector-based semantic search
- NewsAPI for market trend data (optional)
- Custom career data processing pipelines

## Troubleshooting

### Common Issues and Solutions

#### Module Import Errors
Ensure all dependencies are properly installed and your virtual environment is activated. Run `pip install -r requirements.txt` to verify all packages are installed.

#### API Connection Issues
Verify that all API keys in your `.env` file are correct and have not expired. Check that your Azure OpenAI resource is properly deployed and accessible.

#### Slow Response Times
Check your internet connection and API rate limits. The application performance may vary based on API provider load and your network conditions.

#### PDF Processing Failures
Ensure uploaded PDFs contain extractable text (not scanned images) and are under the size limit of 10MB.

### Getting Support
For additional help:
- Check the application logs for detailed error messages
- Verify your environment variables are correctly set
- Ensure all prerequisite services are properly configured
- Contact support through the project's GitHub issues page

## License
This project is licensed under the MIT License. See the LICENSE file for complete details.

## Contributing
We welcome contributions from the community. Please follow these steps:
1. Fork the repository
2. Create a feature branch for your changes
3. Ensure your code follows project standards
4. Submit a pull request with a clear description of your changes

## Acknowledgments
- LangChain for providing excellent AI orchestration framework
- Azure OpenAI for powerful language model capabilities
- Pinecone for scalable vector database infrastructure
- Streamlit for enabling rapid web application development
- The open-source community for various supporting libraries" 
