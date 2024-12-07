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

import yaml
import os
from typing import Dict, List, Set
from genai_rest_builder.constants import IMPORTS_TEMPLATE, CHAIN_TEMPLATE, PROVIDER_CONFIGS, BASE_REQUIREMENTS, PROVIDER_REQUIREMENTS, \
    SERVE_APP_TEMPLATE, IMPORT_CHAIN_TEMPLATE, ADD_ROUTE_TEMPLATE, ENV_DEFAULTS, UTILS_TEMPLATE


def create_utils_file():
    """
    Create the utils.py file in the service_chains directory
    """
    file_path = os.path.join("service_chains", "utils.py")
    try:
        with open(file_path, 'w') as file:
            file.write(UTILS_TEMPLATE)
        print(f"Created utils file: {file_path}")
    except Exception as e:
        print(f"Error creating utils file: {str(e)}")


def create_service_chains_folder():
    """
    Create the service_chains folder and initialize it as a Python package
    """
    # Create the folder
    os.makedirs("service_chains", exist_ok=True)

    # Create __init__.py
    init_path = os.path.join("service_chains", "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, 'w') as f:
            f.write("")

    # Create utils.py
    create_utils_file()


def read_yaml_file(file_path: str) -> Dict:
    """
    Read and parse the YAML file
    """
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return {}


def generate_chain_code(service_name: str, details: Dict) -> str:
    """
    Generate the chain code based on service details
    Args:
        service_name: Name of the service
        details: Service configuration details
    Returns:
        str: Generated chain code
    """
    provider = details['model']['provider']
    provider_config = PROVIDER_CONFIGS.get(provider)

    if not provider_config:
        raise ValueError(f"Unsupported provider: {provider}")

    # Generate imports section
    imports = IMPORTS_TEMPLATE.format(
        llm_import=provider_config['llm_import']
    )
    if provider_config['extra_imports']:
        imports += "\n" + "\n".join(provider_config['extra_imports'])

    # Generate chain section
    chain = CHAIN_TEMPLATE.format(
        service_name=service_name,  # Pass service_name for YAML config loading
        llm_class=provider_config['llm_class'],
        llm_params=provider_config['llm_params_template']
    )

    return f"{imports}\n{chain}"


def create_service_file(service_name: str, details: Dict) -> None:
    """
    Create a Python file for the service with LangChain configuration
    """
    file_name = f"{service_name}_chain.py"
    file_path = os.path.join("service_chains", file_name)

    try:
        content = generate_chain_code(service_name, details)  # Pass both service_name and details
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"Created file: {file_path}")
    except Exception as e:
        print(f"Error creating file {file_path}: {str(e)}")


def process_services(services: List[Dict]) -> None:
    """
    Process each service and create corresponding Python files
    """
    for service in services:
        for service_name, details in service.items():
            print(f"\nProcessing service: {service_name}")
            create_service_file(service_name, details)


def get_required_packages(services: List[Dict]) -> Set[str]:
    """
    Determine required packages based on providers used in services
    """
    required_packages = set(BASE_REQUIREMENTS)

    # Check each service for its provider and add corresponding requirements
    for service in services:
        for service_details in service.values():
            provider = service_details.get('model', {}).get('provider')
            if provider in PROVIDER_REQUIREMENTS:
                required_packages.update(PROVIDER_REQUIREMENTS[provider])

    return required_packages


def create_requirements_file(packages: Set[str]) -> None:
    """
    Create requirements.txt file with the specified packages
    """
    try:
        with open('requirements.txt', 'w') as file:
            for package in sorted(packages):  # Sort for consistent ordering
                file.write(f"{package}\n")
        print("\nCreated requirements.txt file")
    except Exception as e:
        print(f"\nError creating requirements.txt: {str(e)}")


def create_serve_app(services: List[Dict]) -> None:
    """
    Create serve_app.py file that imports and sets up routes for all chains
    """
    try:
        # Generate imports for each chain
        imports = []
        routes = []

        for service in services:
            for service_name in service.keys():
                # Create chain variable name (avoid potential naming conflicts)
                chain_var = f"chain_{service_name.lower()}"

                # Create import statement
                chain_file = f"service_chains.{service_name}_chain"
                import_stmt = IMPORT_CHAIN_TEMPLATE.format(
                    chain_file=chain_file,
                    chain_var=chain_var
                )
                imports.append(import_stmt)

                # Create add_routes statement
                route_stmt = ADD_ROUTE_TEMPLATE.format(
                    chain_var=chain_var,
                    path=service_name
                )
                routes.append(route_stmt)

        # Combine all components
        content = SERVE_APP_TEMPLATE.format(
            imports="\n".join(imports),
            routes="\n\n".join(routes)
        )

        # Write to file
        with open('serve_app.py', 'w') as file:
            file.write(content)
        print("\nCreated serve_app.py file")

    except Exception as e:
        print(f"\nError creating serve_app.py: {str(e)}")


def create_env_file() -> None:
    """
    Create .env file with default server configuration
    """
    try:
        # Check if .env file exists
        if os.path.exists('.env'):
            print("\n.env file already exists, skipping creation")
            return

        with open('.env', 'w') as file:
            for key, value in ENV_DEFAULTS.items():
                file.write(f"{key}={value}\n")
        print("\nCreated .env file with default configuration")
    except Exception as e:
        print(f"\nError creating .env file: {str(e)}")


def main():
    create_service_chains_folder()

    create_env_file()

    # File path
    file_path = "prompt_service.yaml"  # Replace with your file path

    # Read YAML file
    yaml_data = read_yaml_file(file_path)

    # Get services array
    prompt_services = yaml_data.get('PromptServices', [])

    if not prompt_services:
        print("No services found in the YAML file")
        return

    # Process services and create files
    process_services(prompt_services)

    # Generate requirements.txt
    required_packages = get_required_packages(prompt_services)
    create_requirements_file(required_packages)

    # Generate serve_app.py
    create_serve_app(prompt_services)

    # Print summary
    print("\nSummary:")
    print(f"Created {len(prompt_services)} chain files")
    print("Created requirements.txt with the following packages:")
    for package in sorted(required_packages):
        print(f"- {package}")
    print("Created serve_app.py with routes:")
    for service in prompt_services:
        for service_name in service.keys():
            print(f"- /{service_name}")