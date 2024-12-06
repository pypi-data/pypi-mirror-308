# GenAI REST Builder

The **GenAI REST Builder** is a tool that helps create RESTful services around AI models using a YAML configuration file. It automates the setup of FastAPI endpoints, configurations, and environment files for easy deployment of AI-powered services.

## Key Features

- **Service Configuration with Custom Prompts**: Define each service's prompt, model configuration, and provider-specific details in YAML format.
- **Cloud Provider Compatibility**: Supports major providers, including AWS and Azure.
- **Automated Code Generation**: Quickly create FastAPI service endpoints based on YAML configurations.

## Installation

1. **Install the GenAI REST Builder Tool**:

   Start by installing the `genai-rest-builder` package:

   ```bash
   pip install genai-rest-builder
   ```

2. **Generate Project Structure**:

   Use the command below to generate the full project structure with REST APIs for all defined services based on your YAML configuration file:

   ```bash
   genai-rest-proj-build
   ```

   This reads from `prompt_service.yaml` (user needs to create it with prompt details) and creates a structured project with service files, configuration settings, and the main FastAPI application.

3. **Install Project Dependencies**:

   Once the project structure is generated, install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Server**:

   Launch the FastAPI server using `serve_app.py`:

   ```bash
   python serve_app.py
   ```

   The server will start based on the host and port specified in the `.env` file, defaulting to `localhost:8080` if not configured otherwise.

## Example YAML - `prompt_service.yaml` Configuration File

Here’s the structure of a sample YAML configuration file that defines services:

```yaml
PromptServices:
  - <servicename>:
      prompt: <prompt template>
      model:
        provider: [aws, azure]
        modelId: <model id>
        temperature: <temperature>
        maxTokens: <maximum tokens>
```

### YAML Configuration Details

- **servicename**: Unique identifier for the service.
- **prompt**: Template for the AI model’s prompt.
- **model**: Contains model details such as:
  - **provider**: Cloud provider (either `aws` or `azure`).
  - **modelId**: ID for the specific model.
  - **temperature**: Controls randomness in the output.
  - **maxTokens**: Specifies the maximum tokens the model should generate.

## Project Structure

The following structure is generated after running the project build command:

```
.
├── service_chains/
│   ├── <servicename>_chain.py          # Generated service chain files for each service
│   ├── __init__.py                      # Package initialization file
├── serve_app.py                         # Main FastAPI application
├── .env                                 # Environment configuration file
├── requirements.txt                     # Dependencies file
├── prompt_service.yaml                  # YAML configuration file (user-defined)
```

## Accessing API Documentation

After starting the server, the OpenAPI documentation is available at:

```
http://<GENAI_SERVER_HOST>:<GENAI_SERVER_PORT>/docs
```

This page provides an interactive UI to explore and test the API endpoints.

## Invoking Services

Each service can be accessed via its unique REST API path, structured as follows:

```
http://<GENAI_SERVER_HOST>:<GENAI_SERVER_PORT>/<service>/invoke
```

Replace `<service>` with the name defined in the YAML configuration file to make requests to that service.