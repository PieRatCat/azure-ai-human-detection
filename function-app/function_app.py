import azure.functions as func
import logging
import os
import json

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from azure.storage.blob import BlobClient
from azure.identity import DefaultAzureCredential

app = func.FunctionApp()

@app.event_grid_trigger(arg_name="event")
def ImageAnalysisFunction(event: func.EventGridEvent):
    logging.info(f"Python EventGrid trigger processed an event: {event.get_json()}")
    
    try:
        event_data = event.get_json()
        
        if 'url' in event_data:
            blob_url = event_data['url']
            blob_name = blob_url.split('/')[-1]

            logging.info(f"Blob created at: {blob_url}")

            # Use managed identity to authenticate
            credential = DefaultAzureCredential()
            blob_client = BlobClient.from_blob_url(blob_url=blob_url, credential=credential)
            image_data = blob_client.download_blob().readall()

            # --- Your image analysis logic ---
            endpoint = os.environ["VISION_ENDPOINT"]
            key = os.environ["VISION_KEY"]

            client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
            analysis_result = client.analyze(
                image_data=image_data,
                visual_features=[VisualFeatures.PEOPLE]
            )

            analysis_report = {
                "image_name": blob_name,
                "human_detected": False,
                "detection_details": []
            }

            if analysis_result.people and analysis_result.people.list:
                analysis_report["human_detected"] = True
                for person in analysis_result.people.list:
                    analysis_report["detection_details"].append({
                        "confidence": person.confidence,
                        "bounding_box": {
                            "x": person.bounding_box.x,
                            "y": person.bounding_box.y,
                            "width": person.bounding_box.width,
                            "height": person.bounding_box.height
                        }
                    })

            logging.info("Analysis complete. Generating JSON report.")
            
            # --- New code to write directly to storage ---
            container_client = BlobClient.from_connection_string(
                conn_str=os.environ["AzureWebJobsStorage"],
                container_name="analysis-results",
                blob_name=f"{blob_name}.json"
            )
            container_client.upload_blob(json.dumps(analysis_report, indent=4), overwrite=True)
            logging.info(f"JSON report saved to analysis-results/{blob_name}.json")
        
        else:
            logging.warning("Event payload is missing a 'url' key. Skipping processing.")
            
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")