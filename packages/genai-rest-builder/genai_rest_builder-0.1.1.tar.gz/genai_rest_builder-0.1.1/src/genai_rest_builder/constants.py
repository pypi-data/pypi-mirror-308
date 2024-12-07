# constants.py

# Copyright (c) 2024 Biprajeet Kar

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# Environment variable defaults
ENV_DEFAULTS = {
    "GENAI_SERVER_HOST": "localhost",
    "GENAI_SERVER_PORT": "8080"
}

UTILS_TEMPLATE = """# utils.py
import yaml
from pathlib import Path

def get_service_config(service_name):
    yaml_path = Path(__file__).parent.parent / "prompt_service.yaml"
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)

    for service in config['PromptServices']:
        if service_name in service:
            return service[service_name]
    raise ValueError(f"Service {service_name} not found in configuration")
"""

# Common imports template
IMPORTS_TEMPLATE = """from {llm_import}
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .utils import get_service_config

# Add required api keys or endpoint if required
"""

# Common chain template
CHAIN_TEMPLATE = """
# Get service configuration
service_config = get_service_config("{service_name}")

# Initialize the LLM
llm = {llm_class}(
    {llm_params}
)

# Create the prompt template
prompt_template = service_config['prompt']

# Create and export the chain
chain = ChatPromptTemplate.from_template(prompt_template) | llm | StrOutputParser()
"""

# Provider-specific configurations
PROVIDER_CONFIGS = {
    "aws": {
        "llm_import": "langchain_aws import ChatBedrockConverse",
        "llm_class": "ChatBedrockConverse",
        "llm_params_template": """model=service_config['model']['modelId'],
    temperature=service_config['model']['temperature'],
    max_tokens=service_config['model']['maxTokens']""",
        "extra_imports": []
    },
    "azure": {
        "llm_import": "langchain_openai import AzureChatOpenAI",
        "llm_class": "AzureChatOpenAI",
        "llm_params_template": """azure_deployment=service_config['model']['modelId'],
    temperature=service_config['model']['temperature'],
    max_tokens=service_config['model']['maxTokens'],
    api_version=service_config['model']['apiVersion']""",
        "extra_imports": ["import os"]
    }
}

# Add this at the end of constants.py

# Base requirements that are always needed
BASE_REQUIREMENTS = [
    "langchain",
    "fastapi",
    "uvicorn",
    "langserve",
    "sse_starlette",
    "python-dotenv",
    "pyyaml"
]

# Provider-specific requirements
PROVIDER_REQUIREMENTS = {
    "aws": ["langchain-aws"],
    "azure": ["langchain-openai"]
}

SERVE_APP_TEMPLATE = '''from fastapi import FastAPI
from langserve import add_routes

{imports}

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app=FastAPI(title="App Server",version="1.0",description="GenAI app")

{routes}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app=app, 
        host=os.getenv("GENAI_SERVER_HOST", "localhost"),
        port=int(os.getenv("GENAI_SERVER_PORT", 8080))
    )
'''

IMPORT_CHAIN_TEMPLATE = "from {chain_file} import chain as {chain_var}"
ADD_ROUTE_TEMPLATE = '''add_routes(
    app,
    {chain_var},
    path="/{path}"
)'''
