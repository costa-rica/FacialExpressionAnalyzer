import os
import json
from google.cloud import vision
from datetime import datetime
from google.protobuf.json_format import MessageToDict
from google.cloud.vision_v1 import AnnotateImageResponse
from app_package._common.utilities import custom_logger
from app_package._common.config import config

logger_bp_main = custom_logger('bp_main.log')

def send_image_to_google_for_analysis(username, image_path):
    logger_bp_main.info(f"-- in send_image_to_google_for_analysis function --")
    # image_path = nick_face_05_web
    # path_to_dir = "/Users/nick/Library/CloudStorage/OneDrive-Personal/Documents/_projects/20240603facialHappinessApp"

    # Hard-coded paths for credentials and output files
    # credentials_path = os.path.join(path_to_dir, "leafy-outrider-245913-815b02067797.json")
    credentials_path = os.path.join(config.GOOGLE_CREDENTIALS_FILE_PATH, config.GOOGLE_CREDENTIALS_FILE_NAME)
    # output_path = 'path_to_output_directory/'
    # output_path = "/Users/nick/Documents/_project_resources/FaceExpressionApp/responses"
    output_path = os.path.join(config.PROJECT_RESOURCES_ROOT, "user_images", username,"responses")
    # output_path_small = "/Users/nick/Documents/_project_resources/FaceExpressionApp/responses_small"
    output_path_small = os.path.join(config.PROJECT_RESOURCES_ROOT, "user_images", username,"responses_small")

    logger_bp_main.info(f"-- output_path: {output_path} --")
    logger_bp_main.info(f"-- output_path_small: {output_path_small} --")

    # Ensure the output directories exist
    os.makedirs(output_path, exist_ok=True)
    os.makedirs(output_path_small, exist_ok=True)

    # Client setup
    client = vision.ImageAnnotatorClient.from_service_account_file(credentials_path)

    # Load the image
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Perform the request
    response = client.face_detection(image=image)

    # Prepare the base response JSON
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    response_to_str = AnnotateImageResponse.to_json(response)
    response_json = json.loads(response_to_str)
    base_response = {
        'image_file_name': os.path.basename(image_path),
        'google_vision_api_response': response_json
    }

    # Save the detailed response
    detailed_response_path = os.path.join(output_path, f'g_vision_response_{timestamp}.json')
    with open(detailed_response_path, 'w') as f:
        json.dump(base_response, f, indent=2)

    # Extract key metrics for the smaller response
    face_annotations = response.face_annotations
    if face_annotations:

        key_metrics = {
            'detectionConfidence': response_json.get('faceAnnotations')[0].get('detectionConfidence'),
            'landmarkingConfidence': response_json.get('faceAnnotations')[0].get('landmarkingConfidence'),
            'joyLikelihood': response_json.get('faceAnnotations')[0].get('joyLikelihood'),
            'sorrowLikelihood': response_json.get('faceAnnotations')[0].get('sorrowLikelihood'),
            'angerLikelihood': response_json.get('faceAnnotations')[0].get('angerLikelihood'),
            'surpriseLikelihood': response_json.get('faceAnnotations')[0].get('surpriseLikelihood'),
            'underExposedLikelihood': response_json.get('faceAnnotations')[0].get('underExposedLikelihood'),
            'blurredLikelihood': response_json.get('faceAnnotations')[0].get('blurredLikelihood'),
            'headwearLikelihood': response_json.get('faceAnnotations')[0].get('headwearLikelihood')
        }
    else:
        key_metrics = {}

    # Save the smaller response
    small_response = {
        'image_file_name': os.path.basename(image_path),
        'google_vision_api_response_key_metrics': key_metrics
    }
    small_response_path = os.path.join(output_path_small, f'g_vision_response_small_{timestamp}.json')
    with open(small_response_path, 'w') as f:
        json.dump(small_response, f, indent=2)