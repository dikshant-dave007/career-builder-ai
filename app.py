import logging
import os

from dotenv import load_dotenv
import streamlit as st

from src.chat_engine import CareerChatEngine
from src.market_insights import MarketInsightEngine
from src.newsletter_generator import NewsletterGenerator


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Custom CSS for enhanced UI
st.markdown(
    """
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .profile-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 5px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 5px solid #9c27b0;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
        text-align: center;
        border: 1px solid #e0e0e0;
    }
    .feature-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
        border-left: 4px solid #ff6b6b;
    }
    .quick-action-btn {
        width: 100%;
        margin: 5px 0;
    }
    .stButton button {
        border-radius: 10px;
    }
    .stTextArea textarea {
        border-radius: 10px;
    }
    .stSelectbox select {
        border-radius: 10px;
    }
</style>
""",
    unsafe_allow_html=True,
)


class CareerBuilderAI:
    def __init__(self):
        logger.info("Initializing CareerBuilder AI Application")
        try:
            self.chat_engine = CareerChatEngine()
            self.market_insights = MarketInsightEngine()
            self.newsletter_gen = NewsletterGenerator()
            logger.info("All components initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize application components: {str(e)}")
            raise

    def initialize_session_state(self):
        logger.info("Initializing session state")
        if "messages" not in st.session_state:
            st.session_state.messages = []
            logger.debug("Initialized messages list")
        if "user_profile" not in st.session_state:
            st.session_state.user_profile = {
                "interests": "",
                "skills": "",
                "experience": "",
                "goals": "",
            }
            logger.debug("Initialized user profile")
        if "chat_started" not in st.session_state:
            st.session_state.chat_started = False

    def render_sidebar(self):
        logger.debug("Rendering sidebar components")
        with st.sidebar:
            # Enhanced Header
            st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
            st.markdown("### 👤 Career Profile")
            st.markdown("</div>", unsafe_allow_html=True)

            # Profile completion indicator
            profile_complete = self.is_profile_complete()
            if profile_complete:
                st.success("✅ Profile Complete!")
            else:
                st.warning("⚠️ Complete your profile to start chatting")

            # User Profile Form with better styling
            with st.container():
                st.session_state.user_profile["interests"] = st.text_area(
                    "🎯 Career Interests*",
                    value=st.session_state.user_profile["interests"],
                    placeholder="e.g., AI, Web Development, Data Science, Marketing...",
                    help="What fields or technologies interest you?",
                )

                st.session_state.user_profile["skills"] = st.text_area(
                    "🛠️ Current Skills*",
                    value=st.session_state.user_profile["skills"],
                    placeholder="e.g., Python, JavaScript, SQL, Project Management...",
                    help="List your current skills and technologies",
                )

                st.session_state.user_profile["experience"] = st.selectbox(
                    "📊 Experience Level*",
                    ["Student", "Entry-level", "Mid-level", "Senior", "Executive"],
                    help="Select your current career level",
                )

                st.session_state.user_profile["goals"] = st.text_area(
                    "🎯 Career Goals*",
                    value=st.session_state.user_profile["goals"],
                    placeholder="e.g., Become a ML Engineer, Transition to Management, Start a tech career...",
                    help="What are your career aspirations?",
                )

            st.markdown("---")

            # Newsletter Section
            st.markdown("### 📧 Career Newsletter")
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write("Get personalized career insights")
            with col2:
                if st.button("📥 Generate", key="newsletter_btn"):
                    logger.info("User triggered newsletter generation")
                    self.generate_newsletter()

            st.markdown("---")

            # Session Metrics
            st.markdown("### 📊 Session Stats")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Messages", len(st.session_state.messages))
            with col2:
                st.metric(
                    "Status", "Active" if st.session_state.chat_started else "Ready"
                )

            st.markdown("---")

            # Quick Actions
            st.markdown("### ⚡ Quick Actions")
            if st.button("🔄 Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.chat_started = False
                st.rerun()

            if st.button("💡 Sample Questions", use_container_width=True):
                self.show_sample_questions()

    def is_profile_complete(self):
        """Check if user profile is complete"""
        profile = st.session_state.user_profile
        return all([profile["interests"], profile["skills"], profile["goals"]])

    def show_sample_questions(self):
        """Display sample questions in the main area"""
        st.session_state.show_samples = True

    def generate_newsletter(self):
        logger.info("Starting newsletter generation process")
        with st.spinner("📊 Generating your personalized career newsletter..."):
            try:
                newsletter = self.newsletter_gen.generate_newsletter(
                    st.session_state.user_profile
                )

                # Success message and download button
                st.success("✅ Newsletter generated successfully!")

                st.download_button(
                    "📥 Download Newsletter",
                    newsletter,
                    file_name="career_newsletter.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
                logger.info("Newsletter generated successfully")
            except Exception as e:
                logger.error(f"Failed to generate newsletter: {str(e)}")
                st.error("❌ Failed to generate newsletter. Please try again.")

    def render_chat_interface(self):
        logger.debug("Rendering main chat interface")

        # Enhanced Header
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(
                "<div class='main-header'>🚀 CareerBuilder AI</div>",
                unsafe_allow_html=True,
            )
            st.markdown("### Your Personal Career Guidance Assistant")
        with col2:
            st.metric(
                "Profile", "Complete" if self.is_profile_complete() else "Incomplete"
            )
        with col3:
            st.metric(
                "Active Chats",
                len([m for m in st.session_state.messages if m["role"] == "user"]),
            )

        st.markdown("---")

        # Feature showcase for new users
        if not st.session_state.messages and not st.session_state.chat_started:
            self.render_feature_showcase()

        # Sample questions panel
        if hasattr(st.session_state, "show_samples") and st.session_state.show_samples:
            self.render_sample_questions()

        # Chat messages with enhanced styling
        st.markdown("### 💬 Career Conversation")
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(
                    f"""
                <div class='user-message'>
                    <strong>👤 You:</strong><br>
                    {message["content"]}
                </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                <div class='assistant-message'>
                    <strong>🤖 CareerBot:</strong><br>
                    {message["content"]}
                </div>
                """,
                    unsafe_allow_html=True,
                )

        # Quick action buttons
        if self.is_profile_complete():
            st.markdown("**💡 Quick questions:**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("🎯 Career Match", use_container_width=True):
                    self.handle_quick_question(
                        "What career paths best match my skills and interests?"
                    )
            with col2:
                if st.button("📚 Skill Roadmap", use_container_width=True):
                    self.handle_quick_question(
                        "Can you create a learning roadmap for my career goals?"
                    )
            with col3:
                if st.button("💼 Market Trends", use_container_width=True):
                    self.handle_quick_question(
                        "What are the current job market trends in my field?"
                    )
            with col4:
                if st.button("🛠️ Skill Gaps", use_container_width=True):
                    self.handle_quick_question(
                        "What skills should I learn to achieve my career goals?"
                    )

        # Chat input
        if prompt := st.chat_input(
            "Ask about career paths, skills, market trends, or learning roadmaps..."
        ):
            self.handle_user_input(prompt)

    def render_feature_showcase(self):
        """Show feature cards for first-time users"""
        st.markdown("### 🎯 How I Can Help You")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                """
            <div class='feature-card'>
                <h4>🔍 Career Discovery</h4>
                <p>Find perfect career paths that align with your unique profile</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
            <div class='feature-card'>
                <h4>📚 Learning Roadmaps</h4>
                <p>Get step-by-step guidance on skills and learning paths</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                """
            <div class='feature-card'>
                <h4>💼 Market Intelligence</h4>
                <p>Stay updated with latest job trends and opportunities</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

    def render_sample_questions(self):
        """Display sample questions panel"""
        st.markdown("### 💡 Try These Questions")

        sample_questions = [
            "What career paths match my current skills and interests?",
            "How can I transition into data science from my current role?",
            "What are the most in-demand skills in tech right now?",
            "Can you suggest a learning path for web development?",
            "What certifications would help advance my career?",
            "How should I prepare for technical interviews?",
            "What are the career growth opportunities in AI/ML?",
        ]

        for i, question in enumerate(sample_questions):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{i+1}. {question}**")
            with col2:
                if st.button("Ask", key=f"ask_{i}"):
                    self.handle_quick_question(question)

        if st.button("Close Samples"):
            st.session_state.show_samples = False
            st.rerun()

        st.markdown("---")

    def handle_quick_question(self, question):
        """Handle quick question button clicks"""
        self.handle_user_input(question)

    def handle_user_input(self, prompt):
        """Process user input and generate response"""
        logger.info(f"User input received: {prompt[:50]}...")

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.chat_started = True

        # Remove sample questions panel if active
        if hasattr(st.session_state, "show_samples"):
            st.session_state.show_samples = False

        # Generate AI response
        with st.spinner("🤖 Analyzing your career query..."):
            try:
                response = self.chat_engine.generate_response(
                    prompt,
                    st.session_state.messages,
                    st.session_state.user_profile,
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
                logger.info("AI response generated successfully")
                st.rerun()
            except Exception as e:
                error_msg = "❌ Sorry, I encountered an error. Please try again."
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )
                logger.error(f"Error generating AI response: {str(e)}")
                st.rerun()


def main():
    logger.info("Starting CareerBuilder AI Application")
    st.set_page_config(
        page_title="CareerBuilder AI",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    try:
        # Initialize app
        app = CareerBuilderAI()
        app.initialize_session_state()
        app.render_sidebar()
        app.render_chat_interface()
        logger.info("Application started successfully")
    except Exception as e:
        logger.critical(f"Failed to start application: {str(e)}")
        st.error("❌ Application failed to start. Please check the configuration.")


if __name__ == "__main__":
    main()
