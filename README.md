<h1 align="center">
	🦉 OWL: Optimized Workforce Learning for General Multi-Agent Assistance in Real-World Task Automation
</h1>


<div align="center">

[![Documentation][docs-image]][docs-url]
[![Discord][discord-image]][discord-url]
[![X][x-image]][x-url]
[![Reddit][reddit-image]][reddit-url]
[![Wechat][wechat-image]][wechat-url]
[![Wechat][owl-image]][owl-url]
[![Hugging Face][huggingface-image]][huggingface-url]
[![Star][star-image]][star-url]
[![Package License][package-license-image]][package-license-url]


</div>


<hr>

<div align="center">
<h4 align="center">

[中文阅读](https://github.com/camel-ai/owl/tree/main/README_zh.md) |
[Community](https://github.com/camel-ai/owl#community) |
[Installation](#️-installation) |
[Examples](https://github.com/camel-ai/owl/tree/main/owl) |
[Paper](https://arxiv.org/abs/2303.17760) |
[Citation](https://github.com/camel-ai/owl#citation) |
[Contributing](https://github.com/camel-ai/owl/graphs/contributors) |
[CAMEL-AI](https://www.camel-ai.org/)

</h4>

<div align="center" style="background-color: #f0f7ff; padding: 10px; border-radius: 5px; margin: 15px 0;">
  <h3 style="color: #1e88e5; margin: 0;">
    🏆 OWL achieves <span style="color: #d81b60; font-weight: bold; font-size: 1.2em;">58.18</span> average score on GAIA benchmark and ranks <span style="color: #d81b60; font-weight: bold; font-size: 1.2em;">🏅️ #1</span> among open-source frameworks! 🏆
  </h3>
</div>

<div align="center">

🦉 OWL is a cutting-edge framework for multi-agent collaboration that pushes the boundaries of task automation, built on top of the [CAMEL-AI Framework](https://github.com/camel-ai/camel).

<!-- OWL achieves **58.18** average score on [GAIA](https://huggingface.co/spaces/gaia-benchmark/leaderboard) benchmark and ranks 🏅️ #1 among open-source frameworks. -->

Our vision is to revolutionize how AI agents collaborate to solve real-world tasks. By leveraging dynamic agent interactions, OWL enables more natural, efficient, and robust task automation across diverse domains.

</div>

![](./assets/owl_architecture.png)

<br>


</div>

<!-- # Key Features -->
# 📋 Table of Contents

- [📋 Table of Contents](#-table-of-contents)
- [🔥 News](#-news)
- [🎬 Demo Video](#-demo-video)
- [✨️ Core Features](#️-core-features)
- [🛠️ Installation](#️-installation)
- [🚀 Quick Start](#-quick-start)
- [🧰 Toolkits and Capabilities](#-toolkits-and-capabilities)
  - [Model Context Protocol (MCP)](#model-context-protocol-mcp)
- [🌐 Web Interface](#-web-interface)
- [🧪 Experiments](#-experiments)
- [⏱️ Future Plans](#️-future-plans)
- [📄 License](#-license)
- [🖊️ Cite](#️-cite)
- [🤝 Contributing](#-contributing)
- [🔥 Community](#-community)
- [❓ FAQ](#-faq)
- [📚 Exploring CAMEL Dependency](#-exploring-camel-dependency)
- [⭐ Star History](#-star-history)

# 🔥 News


<div align="center" style="background-color: #fffacd; padding: 15px; border-radius: 10px; border: 2px solid #ffd700; margin: 20px 0;">
  <h3 style="color: #d81b60; margin: 0; font-size: 1.3em;">
    🌟🌟🌟 <b>COMMUNITY CALL FOR USE CASES!</b> 🌟🌟🌟
  </h3>
  <p style="font-size: 1.1em; margin: 10px 0;">
    We're inviting the community to contribute innovative use cases for OWL! <br>
    The <b>top ten submissions</b> will receive special community gifts and recognition.
  </p>
  <p>
    <a href="https://github.com/camel-ai/owl/tree/main/community_usecase/COMMUNITY_CALL_FOR_USE_CASES.md" style="background-color: #d81b60; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; font-weight: bold;">Learn More & Submit</a>
  </p>
  <p style="margin: 5px 0;">
    Submission deadline: <b>March 31, 2025</b>
  </p>
</div>

<div align="center" style="background-color: #e8f5e9; padding: 15px; border-radius: 10px; border: 2px solid #4caf50; margin: 20px 0;">
  <h3 style="color: #2e7d32; margin: 0; font-size: 1.3em;">
    🧩 <b>NEW: COMMUNITY AGENT CHALLENGES!</b> 🧩
  </h3>
  <p style="font-size: 1.1em; margin: 10px 0;">
    Showcase your creativity by designing unique challenges for AI agents! <br>
    Join our community and see your innovative ideas tackled by cutting-edge AI.
  </p>
  <p>
    <a href="https://github.com/camel-ai/owl/blob/main/community_challenges.md" style="background-color: #2e7d32; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; font-weight: bold;">View & Submit Challenges</a>
  </p>
</div>

<div style="background-color: #e3f2fd; padding: 12px; border-radius: 8px; border-left: 4px solid #1e88e5; margin: 10px 0;">
  <h4 style="color: #1e88e5; margin: 0 0 8px 0;">
    🎉 Latest Major Update - March 15, 2025
  </h4>
  <p style="margin: 0;">
    <b>Significant Improvements:</b>
    <ul style="margin: 5px 0 0 0; padding-left: 20px;">
      <li>Restructured web-based UI architecture for enhanced stability 🏗️</li>
      <li>Optimized OWL Agent execution mechanisms for better performance 🚀</li>
    </ul>
    <i>Try it now and experience the improved performance in your automation tasks!</i>
  </p>
</div>

- **[2025.03.27]**: Integrate SearxNGToolkit performing web searches using SearxNG search engine.
- **[2025.03.26]**: Enhanced Browser Toolkit with multi-browser support for "chrome", "msedge", and "chromium" channels.
- **[2025.03.25]**: Supported Gemini 2.5 Pro, added example run code
- **[2025.03.21]**: Integrated OpenRouter model platform, fix bug with Gemini tool calling.
- **[2025.03.20]**: Accept header in MCP Toolkit, support automatic playwright installation.
- **[2025.03.16]**: Support Bing search, Baidu search.
- **[2025.03.12]**: Added Bocha search in SearchToolkit, integrated Volcano Engine model platform, and enhanced Azure and OpenAI Compatible models with structured output and tool calling.
- **[2025.03.11]**: We added MCPToolkit, FileWriteToolkit, and TerminalToolkit to enhance OWL agents with MCP tool calling, file writing capabilities, and terminal command execution.
- **[2025.03.09]**: We added a web-based user interface that makes it easier to interact with the system.
- **[2025.03.07]**: We open-sourced the codebase of the 🦉 OWL project.
- **[2025.03.03]**: OWL achieved the #1 position among open-source frameworks on the GAIA benchmark with a score of 58.18.


# 🎬 Demo Video

https://github.com/user-attachments/assets/2a2a825d-39ea-45c5-9ba1-f9d58efbc372

https://private-user-images.githubusercontent.com/55657767/420212194-e813fc05-136a-485f-8df3-f10d9b4e63ec.mp4

This video demonstrates how to install OWL locally and showcases its capabilities as a cutting-edge framework for multi-agent collaboration: https://www.youtube.com/watch?v=8XlqVyAZOr8

# ✨️ Core Features

- **Online Search**: Support for multiple search engines (including Wikipedia, Google, DuckDuckGo, Baidu, Bocha, etc.) for real-time information retrieval and knowledge acquisition.
- **Multimodal Processing**: Support for handling internet or local videos, images, and audio data.
- **Browser Automation**: Utilize the Playwright framework for simulating browser interactions, including scrolling, clicking, input handling, downloading, navigation, and more.
- **Document Parsing**: Extract content from Word, Excel, PDF, and PowerPoint files, converting them into text or Markdown format.
- **Code Execution**: Write and execute Python code using interpreter.
- **Built-in Toolkits**: Access to a comprehensive set of built-in toolkits including:
  - **Model Context Protocol (MCP)**: A universal protocol layer that standardizes AI model interactions with various tools and data sources
  - **Core Toolkits**: ArxivToolkit, AudioAnalysisToolkit, CodeExecutionToolkit, DalleToolkit, DataCommonsToolkit, ExcelToolkit, GitHubToolkit, GoogleMapsToolkit, GoogleScholarToolkit, ImageAnalysisToolkit, MathToolkit, NetworkXToolkit, NotionToolkit, OpenAPIToolkit, RedditToolkit, SearchToolkit, SemanticScholarToolkit, SymPyToolkit, VideoAnalysisToolkit, WeatherToolkit, BrowserToolkit, and many more for specialized tasks

# 🛠️ Installation

## **Prerequisites**

### Install Python
Before installing OWL, ensure you have Python installed (version 3.10, 3.11, or 3.12 is supported):

```bash
# Check if Python is installed
python --version

# If not installed, download and install from https://www.python.org/downloads/
# For macOS users with Homebrew:
brew install python@3.10

# For Ubuntu/Debian:
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

## **Installation Options**

OWL supports multiple installation methods to fit your workflow preferences.

### Option 1: Using uv (Recommended)

```bash
# Clone github repo
git clone https://github.com/camel-ai/owl.git

# Change directory into project directory
cd owl

# Install uv if you don't have it already
pip install uv

# Create a virtual environment and install dependencies
uv venv .venv --python=3.10

# Activate the virtual environment
# For macOS/Linux
source .venv/bin/activate
# For Windows
.venv\Scripts\activate

# Install CAMEL with all dependencies
uv pip install -e .
```

### Option 2: Using venv and pip

```bash
# Clone github repo
git clone https://github.com/camel-ai/owl.git

# Change directory into project directory
cd owl

# Create a virtual environment
# For Python 3.10 (also works with 3.11, 3.12)
python3.10 -m venv .venv

# Activate the virtual environment
# For macOS/Linux
source .venv/bin/activate
# For Windows
.venv\Scripts\activate

# Install from requirements.txt
pip install -r requirements.txt --use-pep517
```

### Option 3: Using conda

```bash
# Clone github repo
git clone https://github.com/camel-ai/owl.git

# Change directory into project directory
cd owl

# Create a conda environment
conda create -n owl python=3.10

# Activate the conda environment
conda activate owl

# Option 1: Install as a package (recommended)
pip install -e .

# Option 2: Install from requirements.txt
pip install -r requirements.txt --use-pep517
```

### Option 4: Using Docker

#### **Using Pre-built Image (Recommended)**

```bash
# This option downloads a ready-to-use image from Docker Hub
# Fastest and recommended for most users
docker-compose up -d

# Run OWL inside the container
docker-compose exec owl bash
cd .. && source .venv/bin/activate
playwright install-deps
xvfb-python examples/run.py
```

#### **Building Image Locally**

```bash
# For users who need to customize the Docker image or cannot access Docker Hub:
# 1. Open docker-compose.yml
# 2. Comment out the "image: mugglejinx/owl:latest" line
# 3. Uncomment the "build:" section and its nested properties
# 4. Then run:
docker-compose up -d --build

# Run OWL inside the container
docker-compose exec owl bash
cd .. && source .venv/bin/activate
playwright install-deps
xvfb-python examples/run.py
```

#### **Using Convenience Scripts**

```bash
# Navigate to container directory
cd .container

# Make the script executable and build the Docker image
chmod +x build_docker.sh
./build_docker.sh

# Run OWL with your question
./run_in_docker.sh "your question"
```

## **Setup Environment Variables**

OWL requires various API keys to interact with different services.

### Setting Environment Variables Directly

You can set environment variables directly in your terminal:

- **macOS/Linux (Bash/Zsh)**:
  ```bash
  export OPENAI_API_KEY="your-openai-api-key-here"
  # Add other required API keys as needed
  ```

- **Windows (Command Prompt)**:
  ```batch
  set OPENAI_API_KEY=your-openai-api-key-here
  ```

- **Windows (PowerShell)**:
  ```powershell
  $env:OPENAI_API_KEY = "your-openai-api-key-here"
  ```

> **Note**: Environment variables set directly in the terminal will only persist for the current session.

### Alternative: Using a `.env` File

If you prefer using a `.env` file instead, you can:

1. **Copy and Rename the Template**:
   ```bash
   # For macOS/Linux
   cd owl
   cp .env_template .env
   
   # For Windows
   cd owl
   copy .env_template .env
   ```

   Alternatively, you can manually create a new file named `.env` in the owl directory and copy the contents from `.env_template`.

2. **Configure Your API Keys**:
   Open the `.env` file in your preferred text editor and insert your API keys in the corresponding fields.

> **Note**: For the minimal example (`examples/run_mini.py`), you only need to configure the LLM API key (e.g., `OPENAI_API_KEY`).

### **MCP Desktop Commander Setup**

If using MCP Desktop Commander within Docker, run:

```bash
npx -y @wonderwhy-er/desktop-commander setup --force-file-protocol
```

For more detailed Docker usage instructions, including cross-platform support, optimized configurations, and troubleshooting, please refer to [DOCKER_README.md](.container/DOCKER_README_en.md).

# 🚀 Quick Start

## Basic Usage

After installation and setting up your environment variables, you can start using OWL right away:

```bash
python examples/run.py
```

## Running with Different Models

### Model Requirements

- **Tool Calling**: OWL requires models with robust tool calling capabilities to interact with various toolkits. Models must be able to understand tool descriptions, generate appropriate tool calls, and process tool outputs.

- **Multimodal Understanding**: For tasks involving web interaction, image analysis, or video processing, models with multimodal capabilities are required to interpret visual content and context.

#### Supported Models

For information on configuring AI models, please refer to our [CAMEL models documentation](https://docs.camel-ai.org/key_modules/models.html#supported-model-platforms-in-camel).

> **Note**: For optimal performance, we strongly recommend using OpenAI models (GPT-4 or later versions). Our experiments show that other models may result in significantly lower performance on complex tasks and benchmarks, especially those requiring advanced multi-modal understanding and tool use.

OWL supports various LLM backends, though capabilities may vary depending on the model's tool calling and multimodal abilities. You can use the following scripts to run with different models:

```bash
# Run with Qwen model
python examples/run_qwen_zh.py

# Run with Deepseek model
python examples/run_deepseek_zh.py

# Run with other OpenAI-compatible models
python examples/run_openai_compatible_model.py

# Run with Gemini model
python examples/run_gemini.py

# Run with Azure OpenAI
python examples/run_azure_openai.py

# Run with Ollama
python examples/run_ollama.py
```

For a simpler version that only requires an LLM API key, you can try our minimal example:

```bash
python examples/run_mini.py
```

You can run OWL agent with your own task by modifying the `examples/run.py` script:

```python
# Define your own task
task = "Task description here."

society = construct_society(question)
answer, chat_history, token_count = run_society(society)

print(f"\033[94mAnswer: {answer}\033[0m")
```

For uploading files, simply provide the file path along with your question:

```python
# Task with a local file (e.g., file path: `tmp/example.docx`)
task = "What is in the given DOCX file? Here is the file path: tmp/example.docx"

society = construct_society(question)
answer, chat_history, token_count = run_society(society)
print(f"\033[94mAnswer: {answer}\033[0m")
```

OWL will then automatically invoke document-related tools to process the file and extract the answer.


### Example Tasks

Here are some tasks you can try with OWL:

- "Find the latest stock price for Apple Inc."
- "Analyze the sentiment of recent tweets about climate change"
- "Help me debug this Python code: [your code here]"
- "Summarize the main points from this research paper: [paper URL]"
- "Create a data visualization for this dataset: [dataset path]"

# 🧰 Toolkits and Capabilities

## Model Context Protocol (MCP)

A high-performance system for interacting with large language models (LLMs) and the MCP toolkit.

## Features

- Support for multiple LLM providers (Anthropic, Groq)
- MCP toolkit integration for enhanced capabilities
- Fallback implementation for when MCP toolkit is not available
- Asynchronous API for improved performance
- Comprehensive error handling and logging
- Response caching for faster repeated queries
- Configurable timeouts and retries
- Command-line interface for easy interaction
- Performance diagnosis and optimization tools

## Installation

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm (Node.js package manager)

### Python Dependencies

```bash
pip install anthropic openai python-dotenv requests beautifulsoup4 psutil
```

### MCP Server Dependencies

```bash
python install_mcp_servers.py
```

This will install the necessary MCP server dependencies and create the required configuration files.

## Environment Configuration

Create a `.env` file in the project root with the following variables:

```
ANTHROPIC_API_KEY=your_anthropic_api_key
GROQ_API_KEY=your_groq_api_key
```

## Project Structure

```
.
├── fast_mcp_router.py      # High-performance MCP router
├── mcp_toolkit.py          # MCP toolkit integration
├── test_mcp_toolkit.py     # Test script for MCP toolkit
├── install_mcp_servers.py  # MCP server installation script
├── example.py              # Example script
├── cli.py                  # Command-line interface
├── diagnose_performance.py # Performance diagnosis script
├── mcp/                    # MCP directory
│   ├── mcp_servers_config.json  # MCP server configuration
│   ├── fetch-server.js     # Fetch server startup script
│   ├── mcp-server.js       # MCP server startup script
│   ├── firecrawl-server.js # Firecrawl server startup script
│   ├── playwright-server.js # Playwright server startup script
│   ├── desktop-commander-server.js # Desktop commander server startup script
│   └── github-repo-server.js # GitHub repo server startup script
└── README.md               # This file
```

## Usage

### Command-Line Interface

The MCP system provides a command-line interface for easy interaction:

```bash
# Run a single query
python cli.py --query "What is the capital of France?"

# Run with MCP toolkit enabled
python cli.py --use-mcp --query "Find the latest news about artificial intelligence."

# Run in interactive mode
python cli.py --use-mcp

# Run with custom settings
python cli.py --model anthropic --user-role user --assistant-role assistant --language en --use-mcp --cache --timeout 60
```

### Basic Usage (Direct LLM Calls)

```python
import asyncio
from fast_mcp_router import FastMCPRouter

async def main():
    # Initialize the router with MCP toolkit disabled
    router = FastMCPRouter(
        model="anthropic",
        user_role_name="user",
        assistant_role_name="assistant",
        output_language="en",
        use_mcp=False
    )
    
    # Send a query
    response = await router.chat_with_mcp("What is the capital of France?")
    print(response)

# Run the main function
asyncio.run(main())
```

### Advanced Usage (MCP Toolkit Integration)

```python
import asyncio
import os
from fast_mcp_router import FastMCPRouter

async def main():
    # Set up the MCP path
    mcp_path = os.path.join(os.getcwd(), "mcp")
    
    # Initialize the router with MCP toolkit enabled
    router = FastMCPRouter(
        model="anthropic",
        user_role_name="user",
        assistant_role_name="assistant",
        output_language="en",
        mcp_path=mcp_path,
        use_mcp=True,
        cache_responses=True,
        timeout=60
    )
    
    # Send a query that uses the MCP toolkit
    response = await router.chat_with_mcp("Find the latest news about artificial intelligence.")
    print(response)

# Run the main function
asyncio.run(main())
```

## Testing

### Test MCP Toolkit Integration

```bash
python test_mcp_toolkit.py
```

This will run a series of tests to verify that the MCP toolkit integration is working correctly.

### Performance Diagnosis

```bash
python diagnose_performance.py
```

This will run a series of performance tests and generate a report with metrics such as response time, CPU usage, and memory usage. The results are saved to `performance_results.json`.

## Available MCP Features

The MCP toolkit provides the following features:

- **Fetch Server**: For fetching webpages and making HTTP requests
- **MCP Server**: Core MCP functionality
- **Firecrawl Server**: For web scraping and data extraction
- **Playwright Server**: For browser automation
- **Desktop Commander Server**: For executing system commands
- **GitHub Repo Server**: For interacting with GitHub repositories

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'owl.utils'**
   - This error occurs when the owl package is not installed or not in the Python path.
   - Solution: Install the owl package or add it to the Python path.

2. **MCP Toolkit Connection Issues**
   - This can happen if the MCP servers are not running or not properly configured.
   - Solution: Run `python install_mcp_servers.py` to reinstall the MCP servers.

3. **API Key Issues**
   - Make sure your API keys are correctly set in the `.env` file.
   - Solution: Check the `.env` file and ensure the API keys are valid.

4. **Timeout Issues**
   - If queries are timing out, try increasing the timeout value.
   - Solution: Set a higher timeout value when initializing the router.

5. **Performance Issues**
   - If you're experiencing slow response times or high resource usage, run the performance diagnosis script.
   - Solution: Use the performance diagnosis script to identify bottlenecks and optimize accordingly.

## License

This project is licensed under the MIT License.

# 🌐 Web Interface

<div align="center" style="background-color: #f0f7ff; padding: 15px; border-radius: 10px; border: 2px solid #1e88e5; margin: 20px 0;">
  <h3 style="color: #1e88e5; margin: 0;">
    🚀 Enhanced Web Interface Now Available!
  </h3>
  <p style="margin: 10px 0;">
    Experience improved system stability and optimized performance with our latest update.
    Start exploring the power of OWL through our user-friendly interface!
  </p>
</div>

## Starting the Web UI

```bash
# Start the Chinese version
python owl/webapp_zh.py

# Start the English version
python owl/webapp.py
```

## Features

- **Easy Model Selection**: Choose between different models (OpenAI, Qwen, DeepSeek, etc.)
- **Environment Variable Management**: Configure your API keys and other settings directly from the UI
- **Interactive Chat Interface**: Communicate with OWL agents through a user-friendly interface
- **Task History**: View the history and results of your interactions

The web interface is built using Gradio and runs locally on your machine. No data is sent to external servers beyond what's required for the model API calls you configure.

# 🧪 Experiments

To reproduce OWL's GAIA benchmark score of 58.18:

1. Switch to the `gaia58.18` branch:
   ```bash
   git checkout gaia58.18
   ```

2. Run the evaluation script:
   ```bash
   python run_gaia_roleplaying.py
   ```

This will execute the same configuration that achieved our top-ranking performance on the GAIA benchmark.

# ⏱️ Future Plans

We're continuously working to improve OWL. Here's what's on our roadmap:

- [ ] Write a technical blog post detailing our exploration and insights in multi-agent collaboration in real-world tasks
- [ ] Enhance the toolkit ecosystem with more specialized tools for domain-specific tasks
- [ ] Develop more sophisticated agent interaction patterns and communication protocols
- [ ] Improve performance on complex multi-step reasoning tasks

# 📄 License

The source code is licensed under Apache 2.0.

# 🖊️ Cite

If you find this repo useful, please cite:


```
@misc{owl2025,
  title        = {OWL: Optimized Workforce Learning for General Multi-Agent Assistance in Real-World Task Automation},
  author       = {{CAMEL-AI.org}},
  howpublished = {\url{https://github.com/camel-ai/owl}},
  note         = {Accessed: 2025-03-07},
  year         = {2025}
}
```

# 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

1. Read our [Contribution Guidelines](https://github.com/camel-ai/camel/blob/master/CONTRIBUTING.md)
2. Check [open issues](https://github.com/camel-ai/camel/issues) or create new ones
3. Submit pull requests with your improvements

**Current Issues Open for Contribution:**
- [#362](https://github.com/camel-ai/owl/issues/362)
- [#1945](https://github.com/camel-ai/camel/issues/1945)
- [#1925](https://github.com/camel-ai/camel/issues/1925)
- [#1915](https://github.com/camel-ai/camel/issues/1915)
- [#1970](https://github.com/camel-ai/camel/issues/1970)

To take on an issue, simply leave a comment stating your interest.

# 🔥 Community
Join us ([*Discord*](https://discord.camel-ai.org/) or [*WeChat*](https://ghli.org/camel/wechat.png)) in pushing the boundaries of finding the scaling laws of agents. 

Join us for further discussions!
<!-- ![](./assets/community.png) -->
![](./assets/community.jpg)

# ❓ FAQ

**Q: Why don't I see Chrome running locally after starting the example script?**

A: If OWL determines that a task can be completed using non-browser tools (such as search or code execution), the browser will not be launched. The browser window will only appear when OWL determines that browser-based interaction is necessary.

**Q: Which Python version should I use?**

A: OWL supports Python 3.10, 3.11, and 3.12. 

**Q: How can I contribute to the project?**

A: See our [Contributing](#-contributing) section for details on how to get involved. We welcome contributions of all kinds, from code improvements to documentation updates.

# 📚 Exploring CAMEL Dependency

OWL is built on top of the [CAMEL](https://github.com/camel-ai/camel) Framework, here's how you can explore the CAMEL source code and understand how it works with OWL:

## Accessing CAMEL Source Code

```bash
# Clone the CAMEL repository
git clone https://github.com/camel-ai/camel.git
cd camel
```

# ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=camel-ai/owl&type=Date)](https://star-history.com/#camel-ai/owl&Date)

## Performance Optimization

The MCP system includes tools for performance diagnosis and optimization:

1. **Performance Diagnosis**
   - Run `python diagnose_performance.py` to analyze system performance
   - Generates a report with metrics including response time, CPU usage, and memory usage
   - Results are saved to `performance_results.json`

2. **Performance Optimization**
   - Run `python optimize_performance.py` to optimize the system based on diagnosis results
   - Automatically adjusts settings like timeout and caching based on performance metrics
   - Calculates and reports performance improvements
   - Results are saved to `optimized_results.json`

3. **Optimization Features**
   - Dynamic timeout adjustment based on average response times
   - Response caching for frequently used queries
   - Memory usage optimization
   - CPU usage monitoring and optimization

4. **Performance Monitoring**
   - Real-time logging of performance metrics
   - Detailed performance reports
   - Improvement tracking over time

## MCP Server Setup and Troubleshooting

### Setting Up MCP Servers

The MCP system requires several Node.js servers to be running for full functionality. To set up and start the MCP servers:

1. Run the server setup script:
   ```bash
   python fix_mcp_servers.py
   ```

This script will:
- Create the necessary MCP directory structure
- Set up server configuration files
- Create server startup scripts
- Install required Node.js dependencies
- Start the MCP servers

### Server Configuration

The MCP servers are configured in `mcp/mcp_servers_config.json`. The default configuration includes:

- `fetch` server (port 3000): Handles web content fetching
- `mcp` server (port 3001): Core MCP functionality
- `firecrawl` server (port 3002): Web scraping capabilities
- `playwright` server (port 3003): Browser automation
- `desktop-commander` server (port 3004): System command execution
- `github-repo` server (port 3005): GitHub repository operations

### Troubleshooting MCP Servers

If you encounter issues with the MCP servers:

1. **Connection Refused Errors**
   - Run `python fix_mcp_servers.py` to check and fix server configuration
   - The script will automatically detect port conflicts and reassign ports if needed
   - Check the logs for specific error messages

2. **Server Startup Issues**
   - Ensure Node.js and npm are installed on your system
   - Check if the required ports are available
   - Verify that the MCP directory structure is correct

3. **Server Maintenance**
   - The servers can be stopped by pressing Ctrl+C in the terminal running `fix_mcp_servers.py`
   - To restart the servers, simply run the script again
   - The script will automatically handle server cleanup and restart

4. **Common Issues and Solutions**
   - If servers fail to start, check the Node.js version and update if necessary
   - For port conflicts, the script will automatically find alternative ports
   - If the MCP directory is corrupted, delete it and run the script again to recreate it


[docs-image]: https://img.shields.io/badge/Documentation-EB3ECC
[docs-url]: https://camel-ai.github.io/camel/index.html
[star-image]: https://img.shields.io/github/stars/camel-ai/owl?label=stars&logo=github&color=brightgreen
[star-url]: https://github.com/camel-ai/owl/stargazers
[package-license-image]: https://img.shields.io/badge/License-Apache_2.0-blue.svg
[package-license-url]: https://github.com/camel-ai/owl/blob/main/licenses/LICENSE

[colab-url]: https://colab.research.google.com/drive/1AzP33O8rnMW__7ocWJhVBXjKziJXPtim?usp=sharing
[colab-image]: https://colab.research.google.com/assets/colab-badge.svg
[huggingface-url]: https://huggingface.co/camel-ai
[huggingface-image]: https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-CAMEL--AI-ffc107?color=ffc107&logoColor=white
[discord-url]: https://discord.camel-ai.org/
[discord-image]: https://img.shields.io/discord/1082486657678311454?logo=discord&labelColor=%20%235462eb&logoColor=%20%23f5f5f5&color=%20%235462eb
[wechat-url]: https://ghli.org/camel/wechat.png
[wechat-image]: https://img.shields.io/badge/WeChat-CamelAIOrg-brightgreen?logo=wechat&logoColor=white
[x-url]: https://x.com/CamelAIOrg
[x-image]: https://img.shields.io/twitter/follow/CamelAIOrg?style=social
[twitter-image]: https://img.shields.io/twitter/follow/CamelAIOrg?style=social&color=brightgreen&logo=twitter
[reddit-url]: https://www.reddit.com/r/CamelAI/
[reddit-image]: https://img.shields.io/reddit/subreddit-subscribers/CamelAI?style=plastic&logo=reddit&label=r%2FCAMEL&labelColor=white
[ambassador-url]: https://www.camel-ai.org/community
[owl-url]: ./assets/qr_code.jpg
[owl-image]: https://img.shields.io/badge/WeChat-OWLProject-brightgreen?logo=wechat&logoColor=white

# OWL Tools

A collection of tools for fetching and processing various types of data, built on top of the OWL framework.

## Tools

### News Tool
- Fetch news articles from various sources
- Filter articles by keyword, source, and date
- Extract content and summarize articles
- Search for specific topics

### Weather Tool
- Get current weather conditions
- Fetch weather forecasts
- Check air quality
- Access historical weather data

### Stocks Tool
- Get real-time stock prices
- Fetch historical stock data
- Search for companies
- Get market summaries
- Access company information

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/owl-tools.git
cd owl-tools
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.template .env
# Edit .env with your API keys and settings
```

## Usage

### News Tool

```python
from tools.news import NewsClient

async def main():
    client = NewsClient()
    await client.initialize()
    
    try:
        # Fetch news articles
        response = await client.fetch_news("artificial intelligence", limit=10)
        
        # Filter articles
        filtered = await client.filter_news(
            response['articles'],
            keyword="machine learning",
            limit=5
        )
        
        # Print results
        for article in filtered:
            print(f"Title: {article['title']}")
            print(f"Source: {article['source']}")
            print(f"Link: {article['link']}")
            print("---")
    finally:
        await client.cleanup()

# Run the example
import asyncio
asyncio.run(main())
```

### Weather Tool

```python
from tools.weather import WeatherClient

async def main():
    client = WeatherClient(api_key="your_api_key")
    await client.initialize()
    
    try:
        # Get current weather
        weather = await client.get_current_weather("London")
        print(f"Temperature: {weather['temperature']}°C")
        print(f"Condition: {weather['condition']}")
        
        # Get forecast
        forecast = await client.get_forecast("London", days=3)
        for day in forecast['forecast']:
            print(f"Date: {day['date']}")
            print(f"Max Temp: {day['max_temp']}°C")
            print(f"Min Temp: {day['min_temp']}°C")
            print("---")
    finally:
        await client.cleanup()

# Run the example
import asyncio
asyncio.run(main())
```

### Stocks Tool

```python
from tools.stocks import StocksClient

async def main():
    client = StocksClient(api_key="your_api_key")
    await client.initialize()
    
    try:
        # Get stock price
        price = await client.get_stock_price("AAPL")
        print(f"Price: ${price['price']}")
        print(f"Change: {price['change_percent']}%")
        
        # Get company info
        info = await client.get_company_info("AAPL")
        print(f"Company: {info['name']}")
        print(f"Sector: {info['sector']}")
        print(f"Industry: {info['industry']}")
    finally:
        await client.cleanup()

# Run the example
import asyncio
asyncio.run(main())
```

## Project Structure

```
owl-tools/
├── tools/
│   ├── common/
│   │   ├── __init__.py
│   │   └── base_client.py
│   ├── news/
│   │   ├── __init__.py
│   │   ├── news_client.py
│   │   └── test_news.py
│   ├── weather/
│   │   ├── __init__.py
│   │   └── weather_client.py
│   ├── stocks/
│   │   ├── __init__.py
│   │   └── stocks_client.py
│   └── __init__.py
├── requirements.txt
├── README.md
└── .env
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
