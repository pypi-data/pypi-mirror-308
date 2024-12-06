from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="prompt_studio_python",
    version="0.1.1",
    author="PromptStudio",
    author_email="support@promptstudio.dev",
    description="Python SDK for PromptStudio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/promptstudio/promptstudio-python-sdk",
    packages=find_packages(),
    package_dir={"prompt_studio_python": "prompt_studio_python"},
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.104.0",
        "httpx>=0.25.0",
        "pydantic>=2.4.2",
        "google-generativeai>=0.3.0",
        "anthropic>=0.5.0",
        "openai>=1.3.0",
        "python-jose[cryptography]>=3.3.0",
        "diskcache>=5.6.3",
        "aiohttp>=3.8.0",
        "click>=8.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
    },
    project_urls={
        "Bug Tracker": "https://github.com/promptstudio/promptstudio-python-sdk/issues",
        "Documentation": "https://docs.promptstudio.dev",
        "Source Code": "https://github.com/promptstudio/promptstudio-python-sdk",
    },
    entry_points={
        "console_scripts": [
            "promptstudio=promptstudio.cli:main",
        ],
    },
)
