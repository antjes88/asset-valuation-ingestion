# Asset-valuation-ingestion
## Overview

This repository provides a solution for ingesting Asset Valuation data from files into a Data Warehouse (DW) layer. The current implementation supports parsing data from Generic and Hargreaves Lansdown file sources, whether stored locally or in a Google Cloud Platform (GCP) bucket. The ingested data is then stored in BigQuery. This repository includes tools, pipelines, and configurations designed to streamline the ingestion process while ensuring scalability and maintainability.

The solution is deployed using Terraform as a Google Cloud Function. This function is triggered whenever a file is uploaded to a specified GCP bucket. Upon activation, the function processes the CSV file and loads its data into BigQuery. See picture below.

![solution_diagram](docs/images/solution-diagram.png)

## Features

- **Development Environment**: Pre-configured development container for consistent setup.
- **Comprehensive Testing**: Includes unit tests and integration tests to ensure code reliability, along with test coverage reporting.
- **Pipeline Integration**: Automated pipelines to unit test python solution and deployment.


## Development environment

Recommended development enviroment is VSCode Dev Containers extension. The configuration and set up of this dev container is already defined in `.devcontainer/devcontainer.json` so setting up a new containerised dev environment on your machine is straight-forward.

Pre-requisites:
- docker installed on your machine and available on your `PATH`
- [Visual Studio Code](https://code.visualstudio.com/) (VSCode) installed on your machine
- [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) vscode extension installed

Steps:
- In VSCode go to `View -> Command Pallet` and search for the command `>Dev Containers: Rebuild and Reopen in Container`

The first time you open the workspace within the container it'll take a few minutes to build the container, setup the virtual env and then login to gcloud. At the end of this process you will be presented with a url and asked to provide an authorization. Simply follow the url, permit the access and copy the auth code provided at the end back into to the terminal and press enter. 

### Configure Git 

For seamless Git usage in a Dev Container, create a local script at .devcontainer/git_config.sh (do not push this file to the repository) and set your GitHub account name and email:

```bash
#!/bin/bash

git config --global user.name "your github account name"
git config --global user.email "your github account email"
```

### Local Execution

To execute the solution, use the following command in a Bash terminal `csv-ingestion` inside the devcontainer. Executing this command will prompt a message providing the available arguments to perform different actions. You can explore additional details and options by using the --help tag.

you need to provide a `.env` file at project root location with the following data:

```ini
PROJECT={name of GCP Project}
```

### Unit tests

To execute tests, provide a `tests/.env` file with the following data:

```ini
PROJECT={name of GCP Project}
SOURCE_BUCKET={If file in GCP Bucket, name of bucket}
DESTINATION_TABLE={name of destination table in BQ}
DATASET={name of destination dataset in BQ}
```

execute the following command in terminal to ensur:

```bash
python -m pytest -vv --cov --cov-report=html
```

Unit testing has been integrated into the CI/CD pipeline. A merge will not be approved unless all tests pass successfully. Additionally, a coverage report is automatically generated and provided as a comment for reference.

## Component Diagram

The code architecture of the Python solution is illustrated below. We adopt Onion/Clean Architecture, so ensuring that our Business Logic (Domain Model) has no dependencies. Our goal is to follow SOLID principles, promoting seamless future changes and enhancing code clarity.

The `src/entrypoints/cloud_function/main.py` file is used by the deployed solution as entrypoint, as required by GCP Cloud Functions. Locally, as described in the "Local Execution" section, code execution starts from the Python entrypoint located at `src/entrypoints/cli/__main__.py`. This entrypoint is invoked using the command `csv-ingestion` in a Bash terminal. 

Several entry points can be provided seamlessly because, following Clean Architecture principles, the `main.py` function is treated as the last detail. This ensures that none of the core solution code depends on the entry point; instead, the entry point depends on the core solution code. This design promotes flexibility and allows for the easy addition of new entry points without impacting the existing architecture. Which, in turn, means that the source is independent of the infrastructure. 

The Python entrypoint invokes one of the services found in `src/services.py`. In this case we have only the Asset Valuation pipeline. This service receive objects of the clients for both the destination repository and the source repository as parameters.

The services handle the execution by calling methods found in the Domain and Adapters to ensure the successful completion of the process.

![components_diagram.png](docs/images/components-diagram.png)

The clients for data storage have been implemented following the Repository pattern. This design pattern abstracts the logic for retrieving and storing data, providing a higher-level interface to the rest of the application. By doing so, it enables the implementation of the Dependency Inversion Principle (DIP). This approach allows our Database Layer (Adapters) to depend on the Domain Model, rather than the other way around. This, in turn, facilitates the seamless use of the same Business Logic/Domain Model in another scenario with a different Infrastructure/Data Layer.

Related code can be found on `src/destination_repository.py` and `src/source_repository.py`.

![adapters_diagram](docs/images/adapters-diagram.png)

In the picture above you can also find the Domain Model diagram representing the code found in `src/model` folder. Circles are value objects and rectangles are entities.

## CI/CD - Pipeline Integration
There are 2 CI/CD pipelines implemented as GitHub Actions:

1. **Pytest**: This pipeline is defined in the `.github/workflows/pytest.yaml` file. It is triggered on every pull request, what runs unit tests using `pytest`. It also generates a test coverage report to ensure code quality. If any test fails, the pipeline will block the merge process, ensuring that only reliable code is integrated into the main branch.
2. **Deployment**: #TODO: under development!!!

## Deployment implementation

The Terraform code in this repository automates the deployment of the Asset Valuation ingestion solution on Google Cloud Platform (GCP). It provisions and configures the necessary resources to ensure seamless ingestion and processing of data. Key resources created include:

1. **Google Cloud Storage Bucket**: A bucket is created to store the CSV files that trigger the ingestion process. This bucket is configured with event notifications to invoke the Cloud Function upon file upload.

2. **Google Cloud Function**: The Cloud Function is deployed to process the uploaded files. It serves as the entry point for the ingestion pipeline, parsing the data and loading it into BigQuery. _Note that for every deployment, the Cloud Function entrypoint name must be updated in the Terraform configuration to ensure a correct update_.

3. **IAM Roles and Permissions**: A Cloud Function Service Account is created and roles granted. The default Cloud Storage service account must be granted the `roles/pubsub.publisher` role to enable event notifications. Ensure this role is assigned before deployment.

4. **Null Resources**: Null resources are utilized during the deployment process to execute custom scripts. These scripts ensure that the necessary code files are properly captured and packaged for deployment.

### Requisites

Ensure that your default cloud storage service account is assigned the roles/pubsub.publisher role.