import azure.functions as func
import logging

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="image-feed/{name}", connection="AzureWebJobsStorage")
def ImageAnalyser(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob\n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    # core image analysis logic will go here
    # Use myblob to get the image data
    