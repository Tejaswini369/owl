import os
import anthropic
import openai
from dotenv import load_dotenv
from pathlib import Path
from typing import List, Optional, Dict, Any, Union
import asyncio
import sys
import json
import logging
from camel.toolkits import MCPToolkit, FunctionTool, SearchToolkit
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.agents import ChatAgent
from camel.messages.base import BaseMessage
from camel.logger import set_log_level
from owl.toolkits.news_toolkit import NewsToolkit

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import NewsToolkit after adding the current directory to sys.path
from owl.toolkits.news_toolkit import NewsToolkit

# Load the .env file
load_dotenv()

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import owl.utils, provide fallback if not available
try:
    from owl.utils.enhanced_role_playing import OwlRolePlaying, arun_society
    OWL_AVAILABLE = True
    logger.info("Successfully imported owl.utils.enhanced_role_playing")
except ImportError:
    logger.warning("owl.utils.enhanced_role_playing not found. Using fallback implementation.")
    OWL_AVAILABLE = False
    
    # Fallback implementation for OwlRolePlaying and arun_society
    class OwlRolePlaying:
        def __init__(self, task_prompt, with_task_specify, user_role_name, user_agent_kwargs, 
                     assistant_role_name, assistant_agent_kwargs, output_language=None):
            self.task_prompt = task_prompt
            self.with_task_specify = with_task_specify
            self.user_role_name = user_role_name
            self.user_agent_kwargs = user_agent_kwargs
            self.assistant_role_name = assistant_role_name
            self.assistant_agent_kwargs = assistant_agent_kwargs
            self.output_language = output_language
    
    async def arun_society(society):
        # Simple fallback implementation
        logger.info("Using fallback implementation for arun_society")
        return f"Response to: {society.task_prompt}", [], 0

class MCPLLMRouter:
    def __init__(
        self,
        model: str = 'anthropic',
        mcp_config_path: Optional[str] = None,
        user_role_name: str = "user",
        assistant_role_name: str = "assistant",
        output_language: Optional[str] = None,
        mcp_path: Optional[str] = None,
        github_token: Optional[str] = None,
        github_owner: Optional[str] = None,
        github_repo: Optional[str] = None,
        github_branch: Optional[str] = None,
        use_mcp: bool = True,
        cache_responses: bool = True,
        timeout: int = 30,  # Reduced default timeout
        initialize_servers: bool = False  # New parameter to control server initialization
    ):
        """Initialize MCP LLM Router with enhanced error handling and configuration."""
        logger.info(f"Initializing MCPLLMRouter with model: {model}, use_mcp: {use_mcp}")
        self.model = model
        self.use_mcp = use_mcp
        self.cache_responses = cache_responses
        self.timeout = timeout
        self.initialize_servers = initialize_servers
        self.response_cache = {} if cache_responses else None
        
        # Use absolute path for MCP directory
        self.mcp_path = mcp_path or os.path.abspath(os.path.join(os.path.dirname(__file__), "mcp"))
        self.mcp_config_path = mcp_config_path or os.path.join(os.path.dirname(__file__), "mcp_servers_config.json")
        self.mcp_toolkit = None
        self.user_role_name = user_role_name
        self.assistant_role_name = assistant_role_name
        self.output_language = output_language
        
        # GitHub configuration
        self.github_token = github_token or os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
        self.github_owner = github_owner or os.getenv("GITHUB_OWNER")
        self.github_repo = github_repo or os.getenv("GITHUB_REPO")
        self.github_branch = github_branch or os.getenv("GITHUB_BRANCH")

        # Initialize API clients
        self._initialize_api_clients()

        # Add MCP path to system path if using MCP
        if self.use_mcp and self.mcp_path not in sys.path:
            sys.path.append(self.mcp_path)
            logger.info(f"Added MCP path to system path: {self.mcp_path}")

        # Initialize NewsToolkit
        self.news_toolkit = NewsToolkit()

    def _initialize_api_clients(self):
        """Initialize API clients with error handling."""
        try:
            # Load API keys
            anthropic_key = os.getenv("ANTHROPIC_API_KEY")
            groq_key = os.getenv("GROQ_API_KEY")

            if not anthropic_key and not groq_key:
                raise ValueError("No API keys found. Please set ANTHROPIC_API_KEY or GROQ_API_KEY in .env file")

            # Initialize Anthropic client
            if anthropic_key:
                logger.info("Initializing Anthropic client...")
                self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
                logger.info("Anthropic client initialized successfully")

            # Initialize Groq client
            if groq_key:
                logger.info("Initializing Groq client...")
                self.openai_client = openai
                self.openai_client.api_key = groq_key
                self.openai_client.api_base = "https://api.groq.com/openai/v1"
                logger.info("Groq client initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing API clients: {str(e)}", exc_info=True)
            raise

    async def initialize_mcp(self):
        """Initialize MCP toolkit with enhanced error handling and server configuration."""
        if not self.use_mcp:
            logger.info("MCP toolkit initialization skipped (use_mcp=False)")
            return
            
        try:
            logger.info("Creating MCP configuration...")
            # Create MCP configuration
            mcp_config = self._create_mcp_config()
            
            logger.info("Saving MCP configuration...")
            # Save configuration
            self._save_mcp_config(mcp_config)
            
            logger.info("Initializing MCP toolkit...")
            # Initialize toolkit with timeout
            self.mcp_toolkit = MCPToolkit(config_path=str(self.mcp_config_path))
            
            if self.initialize_servers:
                logger.info("Connecting to MCP toolkit...")
                try:
                    # Use asyncio.wait_for instead of asyncio.timeout for compatibility
                    await asyncio.wait_for(self.mcp_toolkit.connect(), timeout=self.timeout)
                    logger.info("MCP toolkit initialized and connected successfully")
                except asyncio.TimeoutError:
                    logger.warning("MCP toolkit connection timed out, continuing without server initialization")
            else:
                logger.info("Skipping server initialization as requested")
            
        except Exception as e:
            logger.error(f"Error initializing MCP: {str(e)}", exc_info=True)
            raise

    def _create_mcp_config(self) -> Dict[str, Any]:
        """Create MCP configuration with required servers."""
        logger.info("Creating MCP configuration with required servers...")
        config = {
            "mcpServers": {
                "fetch": {
                    "command": "python",
                    "args": ["-m", "mcp.server.fetch"]
                },
                "web": {
                    "command": "python",
                    "args": ["-m", "mcp.server.web"]
                },
                "github": {
                    "command": "python",
                    "args": ["-m", "mcp.server.github"]
                }
            }
        }

        # Add GitHub repo server if credentials are available
        if all([self.github_token, self.github_owner, self.github_repo]):
            config["mcpServers"]["github-repo"] = {
                "command": "node",
                "args": [os.path.join(os.path.dirname(__file__), "mcp_github_repo", "build", "index.js")]
            }
            logger.info("GitHub repo server added to MCP configuration")

        return config

    def _save_mcp_config(self, config: Dict[str, Any]):
        """Save MCP configuration to file."""
        try:
            logger.info(f"Saving MCP configuration to {self.mcp_config_path}...")
            with open(self.mcp_config_path, 'w') as f:
                json.dump(config, f, indent=4)
            logger.info(f"MCP configuration saved to {self.mcp_config_path}")
        except Exception as e:
            logger.error(f"Error saving MCP configuration: {str(e)}", exc_info=True)
            raise

    async def cleanup_mcp(self):
        """Cleanup MCP toolkit connections with error handling."""
        if self.mcp_toolkit and self.use_mcp:
            try:
                logger.info("Disconnecting MCP toolkit...")
                await self.mcp_toolkit.disconnect()
                logger.info("MCP toolkit disconnected successfully")
            except Exception as e:
                logger.error(f"Error disconnecting MCP toolkit: {str(e)}", exc_info=True)

    def _create_models(self) -> Dict[str, Any]:
        """Create models for the conversation with error handling."""
        try:
            logger.info("Creating models for conversation...")
            
            # Check which API keys are available
            anthropic_key = os.getenv("ANTHROPIC_API_KEY")
            groq_key = os.getenv("GROQ_API_KEY")
            openai_key = os.getenv("OPENAI_API_KEY")
            
            # Determine which model platform to use
            if self.model == "anthropic" and anthropic_key:
                platform = ModelPlatformType.ANTHROPIC
                model_type = ModelType.CLAUDE_3_OPUS
                logger.info("Using Anthropic Claude 3 Opus model")
            elif self.model == "groq" and groq_key:
                platform = ModelPlatformType.GROQ
                model_type = ModelType.QWEN_2_5_32B
                logger.info("Using Groq Qwen 2.5 32B model")
            elif openai_key:
                platform = ModelPlatformType.OPENAI
                model_type = ModelType.GPT_4O
                logger.info("Using OpenAI GPT-4 model")
            else:
                # Fallback to direct API calls if no compatible model is available
                logger.warning("No compatible model found, will use direct API calls")
                return None
                
            return {
                "user": ModelFactory.create(
                    model_platform=platform,
                    model_type=model_type,
                    model_config_dict={"temperature": 0},
                ),
                "assistant": ModelFactory.create(
                    model_platform=platform,
                    model_type=model_type,
                    model_config_dict={"temperature": 0},
                ),
            }
        except Exception as e:
            logger.error(f"Error creating models: {str(e)}", exc_info=True)
            return None

    async def chat_with_mcp(self, prompt, use_owl=True):
        """
        Chat with the MCP LLM Router.
        
        Args:
            prompt: The user's prompt
            use_owl: Whether to use OWL for role-playing
            
        Returns:
            The model's response
        """
        try:
            # Check if this is a news-related query
            if "news" in prompt.lower() or "latest" in prompt.lower() or "recent" in prompt.lower():
                logger.info("Detected news query, using NewsToolkit...")
                # Create a new instance of NewsToolkit for each query to avoid state issues
                news_toolkit = NewsToolkit()
                # Set the appropriate LLM client based on the model
                if self.model == "anthropic":
                    news_toolkit.llm_client = self.anthropic_client
                elif self.model == "groq":
                    news_toolkit.llm_client = self.openai_client
                else:
                    # Fallback to direct API call for news queries
                    logger.info("Using direct API call for news query...")
                    return await self._direct_api_call(prompt)
                
                result = news_toolkit.process_news_query(prompt)
                return result["response"]
                
            # For other queries, use the standard approach
            if use_owl and OWL_AVAILABLE:
                logger.info("Using OWL for role-playing...")
                return await self._chat_with_owl(prompt)
            else:
                logger.info("Using direct API call...")
                return await self._direct_api_call(prompt)
                
        except Exception as e:
            logger.error(f"Error in chat_with_mcp: {str(e)}", exc_info=True)
            return f"An error occurred: {str(e)}"
            
    async def _chat_with_owl(self, prompt: str) -> str:
        """
        Chat with the OWL role-playing system.
        
        Args:
            prompt: The user's prompt
            
        Returns:
            The model's response
        """
        try:
            # Create models for the conversation
            models = self._create_models()
            if not models:
                logger.warning("Could not create models for OWL, falling back to direct API call")
                return await self._direct_api_call(prompt)
                
            # Create the role-playing society
            society = OwlRolePlaying(
                task_prompt=prompt,
                with_task_specify=False,
                user_role_name=self.user_role_name,
                user_agent_kwargs={"model": models["user"]},
                assistant_role_name=self.assistant_role_name,
                assistant_agent_kwargs={"model": models["assistant"]},
                output_language=self.output_language
            )
            
            try:
                # Run the society
                response, _, _ = await arun_society(society)
                
                # Clean up any trailing whitespace in the response
                if response and isinstance(response, str):
                    # Remove trailing whitespace and normalize line endings
                    response = response.rstrip()
                    response = response.replace('\r\n', '\n')
                    
                return response
            except Exception as e:
                # Check if the error is related to whitespace
                if "trailing whitespace" in str(e) or "whitespace" in str(e):
                    logger.warning(f"Whitespace error in OWL response: {str(e)}")
                    # Try to extract the response from the error message if possible
                    if hasattr(e, 'response') and e.response:
                        return e.response.rstrip()
                    # Fall back to direct API call
                    logger.info("Falling back to direct API call due to whitespace error")
                    return await self._direct_api_call(prompt)
                else:
                    raise
            
        except Exception as e:
            logger.error(f"Error in OWL chat: {str(e)}", exc_info=True)
            # Fallback to direct API call
            logger.info("Falling back to direct API call due to OWL error")
            return await self._direct_api_call(prompt)

    async def _direct_api_call(self, prompt: str) -> str:
        """Make a direct API call to the LLM provider."""
        try:
            # Check which API keys are available
            anthropic_key = os.getenv("ANTHROPIC_API_KEY")
            groq_key = os.getenv("GROQ_API_KEY")
            openai_key = os.getenv("OPENAI_API_KEY")
            
            # Use the appropriate API based on available keys and model preference
            if self.model == "anthropic" and anthropic_key:
                logger.info("Using Anthropic API for direct call")
                response = self.anthropic_client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=1024,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.content[0].text.rstrip()
            elif self.model == "groq" and groq_key:
                logger.info("Using Groq API for direct call")
                response = self.openai_client.ChatCompletion.create(
                    model="qwen-2-5-32b",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response['choices'][0]['message']['content'].rstrip()
            elif openai_key:
                logger.info("Using OpenAI API for direct call")
                openai.api_key = openai_key
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response['choices'][0]['message']['content'].rstrip()
            else:
                logger.error("No API keys available for direct calls")
                return "Error: No API keys available. Please set ANTHROPIC_API_KEY, GROQ_API_KEY, or OPENAI_API_KEY in your environment variables."
                
        except Exception as e:
            logger.error(f"Error in direct API call: {str(e)}", exc_info=True)
            return f"Error making API call: {str(e)}"

    async def __aenter__(self):
        """Async context manager entry."""
        logger.info("Entering async context manager...")
        if self.use_mcp:
            await self.initialize_mcp()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        logger.info("Exiting async context manager...")
        if self.use_mcp:
            await self.cleanup_mcp()

    async def _chat_with_mcp_toolkit(self, prompt: str) -> str:
        """Enhanced MCP toolkit interaction with news fetching and web content capabilities."""
        try:
            # Check if response is in cache
            if self.cache_responses and prompt in self.response_cache:
                logger.info("Returning cached response")
                return self.response_cache[prompt]

            # Detect if this is a news-related query
            news_keywords = ["news", "latest", "recent", "update", "current events"]
            is_news_query = any(keyword in prompt.lower() for keyword in news_keywords)

            if is_news_query:
                logger.info("Detected news-related query, using news fetching capabilities")
                try:
                    # Use asyncio.wait_for instead of asyncio.timeout
                    async def get_news():
                        news_toolkit = NewsToolkit()
                        return news_toolkit.get_news(prompt)
                    
                    news_results = await asyncio.wait_for(get_news(), timeout=self.timeout)
                    if news_results:
                        response = self._format_news_response(news_results)
                        if self.cache_responses:
                            self.response_cache[prompt] = response
                        return response
                except asyncio.TimeoutError:
                    logger.warning("News fetching timed out, falling back to direct response")
                    return "I apologize, but I'm having trouble fetching the latest news at the moment. Please try again later."

            # Use MCP toolkit for other queries
            logger.info("Using MCP toolkit for query")
            
            # Combine MCP tools with search tools
            mcp_tools = [*self.mcp_toolkit.get_tools()]
            search_toolkit = SearchToolkit()
            search_tools = [
                search_toolkit.search_google,
                search_toolkit.search_duckduckgo,
                search_toolkit.search_wiki
            ]
            all_tools = [*mcp_tools, *search_tools]
            
            # Create chat agents with combined tools
            user_agent = ChatAgent(
                model_name=self.model,
                role_name=self.user_role_name,
                tools=all_tools
            )
            assistant_agent = ChatAgent(
                model_name=self.model,
                role_name=self.assistant_role_name,
                tools=all_tools
            )

            # Process the conversation with timeout
            try:
                # Use asyncio.wait_for instead of asyncio.timeout
                async def process_conversation():
                    user_message = BaseMessage(role=self.user_role_name, content=prompt)
                    assistant_response = await assistant_agent.step(user_message)
                    return assistant_response.content
                
                response = await asyncio.wait_for(process_conversation(), timeout=self.timeout)
                if self.cache_responses:
                    self.response_cache[prompt] = response
                return response
            except asyncio.TimeoutError:
                logger.warning("Chat processing timed out")
                return "I apologize, but the request is taking longer than expected. Please try again."

        except Exception as e:
            logger.error(f"Error in MCP toolkit interaction: {str(e)}", exc_info=True)
            return f"Error processing request: {str(e)}"

    def _format_news_response(self, news_results: List[Dict[str, str]]) -> str:
        """Format news results into a readable response."""
        if not news_results:
            return "I couldn't find any relevant news articles at the moment."

        response = "Here are the latest relevant news articles:\n\n"
        for i, article in enumerate(news_results, 1):
            response += f"{i}. {article['title']}\n"
            response += f"   Published: {article['published']}\n"
            response += f"   Link: {article['link']}\n\n"
        
        return response

# Example usage
async def main():
    """Example usage of MCPLLMRouter with news fetching capabilities."""
    try:
        # Check for API keys
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        groq_key = os.getenv("GROQ_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if not any([anthropic_key, groq_key, openai_key]):
            print("\nERROR: No API keys found. Please set at least one of the following environment variables:")
            print("  - ANTHROPIC_API_KEY")
            print("  - GROQ_API_KEY")
            print("  - OPENAI_API_KEY")
            print("\nYou can set these in your .env file or directly in your environment.")
            return
            
        # Determine which model to use based on available API keys
        model = "anthropic"  # Default
        if anthropic_key:
            model = "anthropic"
        elif groq_key:
            model = "groq"
        elif openai_key:
            model = "openai"
            
        print(f"\nUsing {model} model for this session.")
        
        router = MCPLLMRouter(
            model=model,
            use_mcp=True,
            cache_responses=True,
            timeout=30,  # Reduced timeout
            initialize_servers=False  # Don't initialize servers by default
        )

        # Initialize MCP
        await router.initialize_mcp()

        # Test news fetching
        news_query = "What is breaking news today?"
        print(f"\nTesting news query: {news_query}")
        response = await router.chat_with_mcp(news_query)
        print("\nNews Query Response:")
        print(response)

        # Test general query
        general_query = "What are the taxation policies in the United States in 2025?"
        print(f"\nTesting general query: {general_query}")
        response = await router.chat_with_mcp(general_query)
        print("\nGeneral Query Response:")
        print(response)

    except Exception as e:
        print(f"\nERROR: {str(e)}")
        print("\nIf you're seeing API key errors, please make sure you have set the appropriate API keys in your environment.")
        print("You can set these in your .env file or directly in your environment.")
    finally:
        if 'router' in locals():
            await router.cleanup_mcp()

if __name__ == "__main__":
    asyncio.run(main())