# Azure AI Human Detection Pipeline

### Project Overview
This project demonstrates an automated, serverless pipeline for detecting human presence in images. Built with Python on Azure Functions and Azure AI services, the system processes image files uploaded to a storage account, analyses them for human presence, and generates a structured report of the findings. This project showcases a practical application of computer vision and a modern cloud-native architecture.

---

### Architecture
The pipeline follows an event-driven, serverless architecture.

1.  **Image Ingestion:** An image file is uploaded to a designated Azure Blob Storage container (`image-feed`).
2.  **Serverless Processing:** This upload event triggers a Python-based Azure Function.
3.  **AI Analysis:** The Python function uses the Azure AI Vision service to analyse the image and detect any people.
4.  **Reporting:** If a human is detected, the function generates a JSON report with details like confidence scores and bounding box coordinates.
5.  **Output Storage:** The JSON report is saved to a separate Azure Blob Storage container (`analysis-results`) for later review and analysis.

---

### Repository Structure
This repository is organized to clearly separate the project's components.

* `analysis/` - Contains the Jupyter Notebook (`project_analysis.ipynb`) for data analysis and visualisation.
* `function-app/` - The source code for the Python Azure Function.
* `samples/` - A folder with example images for testing and demonstration.
* `README.md` - This project overview and guide.
* `requirements.txt` - Lists all the Python dependencies for the project.

---

### Setup and Usage
Follow these steps to set up and run the project locally and in Azure.

#### Prerequisites
* An active Azure subscription.
* Visual Studio Code with the Azure Functions extension.
* Python 3.10 or later.
* Azure Functions Core Tools.

#### 1. Azure Resource Setup
1.  In the Azure portal, create a **Storage Account**.
2.  Inside the Storage Account, create two Blob containers: `image-feed` and `analysis-results`.
3.  Also in the portal, create an **Azure AI Vision** resource. Note down the endpoint and one of the API keys.

#### 2. Local Configuration
1.  Clone this repository to your local machine.
2.  In the `function-app` directory, open `local.settings.json`.
3.  Add the connection string for your storage account and the endpoint/key for your Azure AI Vision resource to the `Values` section.
4.  Install the required Python packages by running `pip install -r requirements.txt` in a terminal.

#### 3. Deployment
* Use the Azure Functions extension in VS Code to deploy the `function-app` to Azure.

#### 4. Testing
* Upload images to the `image-feed` container via the Azure portal or the VS Code Azure Storage extension. The function should trigger automatically, and a JSON report will be saved to `analysis-results` if a human is detected.

---

### Data Analysis
The Jupyter Notebook located in the `analysis/` folder provides a detailed breakdown of the analysis performed on the generated JSON reports. It includes visualisations and key metrics to evaluate the pipeline's performance.