# Azure AI Human Detection Pipeline

### Project Overview
This project demonstrates an automated, serverless pipeline for detecting human presence in images. Built with the **Python v2 programming model** on Azure Functions, the system processes image files uploaded to a storage account, analyses them for human presence using **Azure AI Vision**, and generates a structured report of the findings. The solution showcases a practical application of computer vision and a modern cloud-native architecture.

---

### Architecture
The pipeline follows a robust event-driven, serverless architecture.

1.  **Image Ingestion:** An image file is uploaded to a designated Azure Blob Storage container (`camera-feed`).
2.  **Event Trigger:** This upload event triggers an **Azure Event Grid** subscription, which forwards the event to the Azure Function.
3.  **Serverless Processing:** The Python-based Azure Function is invoked. It downloads the image and uses a **managed identity** for secure authentication.
4.  **AI Analysis:** The function sends the image data to the Azure AI Vision service to analyse it for people.
5.  **Reporting:** If a person is detected, the function generates a JSON report with details like confidence scores and bounding box coordinates.
6.  **Output Storage:** The JSON report is saved to a separate Azure Blob Storage container (`analysis-results`) for later review and analysis.

---

### Repository Structure
This repository is organized to clearly separate the project's components.

* `analysis/` - Contains the Jupyter Notebook (`project_analysis.ipynb`) for data analysis and visualisation.
* `function-app/` - The source code for the Python Azure Function, including the `function_app.py` script.
* `samples/` - A folder with example images for testing and demonstration.
* `README.md` - This project overview and guide.
* `requirements.txt` - Lists all the Python dependencies for the project.

---

### Setup and Usage
Follow these steps to set up and run the project in Azure.

#### Prerequisites
* An active Azure subscription.
* Visual Studio Code with the Azure Functions extension.
* Python 3.12 or later.
* Azure Functions Core Tools.

#### 1. Azure Resource Setup
1.  In the Azure portal, create a **Storage Account** and two Blob containers: `camera-feed` and `analysis-results`.
2.  Create an **Azure AI Vision** resource.
3.  Create a new **Function App** and ensure it is on the **Consumption plan** with a **Python 3.12** runtime.
4.  Enable the **System-assigned managed identity** on your Function App.
5.  On the Storage Account, assign the **`Storage Blob Data Reader`** and **`Storage Blob Data Contributor`** roles to your Function App's managed identity.
6.  On the Azure AI Vision resource, assign the **`Cognitive Services User`** role to your Function App's managed identity.

#### 2. Deployment
* Use the Azure Functions extension in VS Code to deploy the `function-app` to your Function App in Azure.

#### 3. Event Grid Subscription
* In your Storage Account in the Azure portal, go to the **`Events`** blade.
* Create a new **Event Subscription** and set the endpoint type to **`Azure Function`**.
* Select your Function App and ensure the filter is set to **`Blob Created`** events in the `camera-feed` container.

#### 4. Testing
* Upload images to the `camera-feed` container via the Azure portal. The function should trigger automatically, and a JSON report will be saved to `analysis-results` if a person is detected.

---

### Data Analysis
The Jupyter Notebook located in the `analysis/` folder provides a detailed breakdown of the analysis performed on the generated JSON reports. It includes visualisations and key metrics to evaluate the pipeline's performance.

---

### Dataset
The images used for this analysis are from the Human Detection Dataset, available on Kaggle. [https://www.kaggle.com/datasets/constantinwerner/human-detection-dataset](https://www.kaggle.com/datasets/constantinwerner/human-detection-dataset)