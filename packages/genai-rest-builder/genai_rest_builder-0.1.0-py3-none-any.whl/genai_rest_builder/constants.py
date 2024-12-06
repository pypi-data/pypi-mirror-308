# constants.py

# Environment variable defaults
ENV_DEFAULTS = {
    "GENAI_SERVER_HOST": "localhost",
    "GENAI_SERVER_PORT": "8080"
}

# Common imports template
IMPORTS_TEMPLATE= """from {llm_import}
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Add required api keys or endpoint if required
"""

# Common chain template
CHAIN_TEMPLATE= """
# Initialize the LLM
llm = {llm_class}(
    {llm_params}
)

# Create the prompt template
prompt_template = \"\"\"
{prompt}
\"\"\"

# Create and export the chain
chain = ChatPromptTemplate.from_template(prompt_template) | llm | StrOutputParser()
"""

# Provider-specific configurations
PROVIDER_CONFIGS= {
    "aws": {
        "llm_import": "langchain_aws import ChatBedrockConverse",
        "llm_class": "ChatBedrockConverse",
        "llm_params_template": """model="{model_id}",
    temperature={temperature},
    max_tokens={max_tokens}""",
        "extra_imports": []
    },
    "azure": {
        "llm_import": "langchain_openai import AzureChatOpenAI",
        "llm_class": "AzureChatOpenAI",
        "llm_params_template": """azure_deployment="{model_id}",
    temperature={temperature},
    max_tokens={max_tokens},
    api_version=\"{api_version}\"""",
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
    "python-dotenv"
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
