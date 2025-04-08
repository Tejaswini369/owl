from setuptools import setup, find_packages

setup(
    name="owl",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "anthropic",
        "openai",
        "python-dotenv",
        "feedparser",
        "camel-ai",
    ],
    author="OWL Team",
    description="OWL - A framework for building AI agents with toolkits",
    keywords="ai, agents, toolkits, llm",
    python_requires=">=3.8",
) 