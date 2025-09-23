import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import os
import pandas as pd
import json

# Define the local file path where the DataFrame is saved
local_file_path = './reports_dataframe.pkl'

# Load the DataFrame from the pickle file
try:
    df = pd.read_pickle(local_file_path)
    print("DataFrame loaded successfully from local file.")
except FileNotFoundError:
    print(f"Error: The file {local_file_path} was not found.")

# Now you can use the 'df' DataFrame in your script
print(f"The DataFrame has {len(df)} rows.")

# Define the paths
data_folder = '../samples/images/'
output_folder = './visualizations/'
os.makedirs(output_folder, exist_ok=True)

# Loop through each analysis report in your DataFrame
for index, report in df.iterrows():
    try:
        image_filename = report['image_name']
        image_path = os.path.join(data_folder, image_filename)
        
        # Check if the image file exists
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}. Skipping...")
            continue

        # Open the image file
        img = Image.open(image_path)
        
        # Create the plot
        fig, ax = plt.subplots(1)
        ax.imshow(img)

        # Draw bounding boxes if any are detected
        if report['detection_details']:
            for detail in report['detection_details']:
                bbox = detail['bounding_box']
                x, y, width, height = bbox['x'], bbox['y'], bbox['width'], bbox['height']
                rect = patches.Rectangle((x, y), width, height, linewidth=2, edgecolor='r', facecolor='none')
                ax.add_patch(rect)
                confidence = detail['confidence']
                plt.text(x, y - 5, f'Conf: {confidence:.2f}', color='red', fontsize=10, weight='bold')

        plt.axis('off')
        
        # Save the figure to the new visualizations folder
        output_filename = f"{os.path.splitext(image_filename)[0]}_analyzed.png"
        plt.savefig(os.path.join(output_folder, output_filename), bbox_inches='tight', pad_inches=0)
        plt.close(fig) # Close the figure to free up memory

        print(f"Successfully processed and saved: {output_filename}")
        
    except Exception as e:
        print(f"Failed to process {image_filename}: {e}")