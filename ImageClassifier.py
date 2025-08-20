import os
import requests
from flask import Flask, request, jsonify
import google.generativeai as genai  # type: ignore
import json
import re
import mediapipe as mp
import cv2
import numpy as np
import pandas as pd

app = Flask(__name__)

# Configuring Google Generative AI API
api_key = 'AIzaSyBpwCaDfkRhj4ZW7Yw3Xy7r0-A5N4okY_E'
genai.configure(api_key=api_key)

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)

PROMPT = """
Your role is to verify the image against a particular hashtag.
An image will be provided and you need to check whether the human face is visible or not, find number of human faces visible, whether they are performing activity indoor or outdoor, name of the game and whether the human is standing or sitting and you need to assign it a particular hashtag.

If human face is visible only then find hashtag and mark visible from the below category:

1. earthivist: mark all images related to plants, using broom, cleaning house or things, images related to power saving guides, using dustbins or using a cloth bag instead of a plastic bag under earthivist only if human face is visible.

2. wellnesschamp: mark images related to physical and mental health wellbeing (exercise,football yoga, meditation, dance, brain games (sudoku, chess,etc)) under this only if a human face is visible otherwise mark them as promotivator.

3. superempowerer:  mark images related to uplifting marginalized sections of society (donations, community work, skill development), learning new skills themselves under this only if a human face is visible otherwise mark them as promotivator.

4. chiefanimalofficer: mark images related to animal protection, helping the voiceless, feeding strays/pets, adopting, taking care of animals, connecting with animal shelter under this only if a human face is visible otherwise mark them as promotivator.

5. icreateimpact: Any image having certificates, medals, trophies (Student should be VISIBLE if he uploads only medals/trophies, certificate contains name and thus can be posted without student having to be present) (MARK VISIBLE WHEN STUDENT IS PRESENT)

6. championsofethics: any activity where student is reading books (around SDGs) to enhance knowledge (Student should be VISIBLE and MARKED VISIBLE)

7. roadsafetyheroes: any activity where student is uploading pictures/videos related to following traffic safety rules (Student should be VISIBLE and MARKED VISIBLE)

8. creator: any activity related to carrying out experiments, playing instruments, projects (Student should be VISIBLE and MARKED VISIBLE)

9. ewastehero: any activity related to electronic waste management (replacing batteries, recycling ewaste) (Student should be VISIBLE and MARKED VISIBLE)

10. waterwarrior: any activity related to water conservation (using bucket instead of shower, fixing leaky taps) (Student should be VISIBLE and MARKED VISIBLE)

11. technogeek: any activity related to website creation, programming languages, coding. 

12. speaker: any activity related to student presenting opinion of a particular topic, public speaking (Student should be VISIBLE and MARKED VISIBLE)

13. artist: mark images related to drawings,paintings,artwork under this only if a human face is visible otherwise mark them as promotivator.

15. appreciation: Any image which does not revolve around sustainable development goals but can be appreciated for engaging on the platform ( posting selfies, family pictures, artwork, posting self photos (not around sdgs) (VISIBLE STUDENTS MUST BE MARKED )

16. celebrations: posts related to wishes (happy new year, happy diwali, merry christmas, happy holi, happy independence day etc)

17. pending: if post only contains exact text " I am thrilled to announce that my journey towards building the sustainable world has begun ✨🎉", mark it as pending.

18. inappropriate: any activity containing any spam, violence, nudity, vulgar, obscene, cruelty to animals or people content then mark it as inappropriate.

Else If human face is not visible then find hashtag from this category:

1. Promotivator: Any activity performed under any hashtag or motivational/inspirational where the student is NOT VISIBLE will be marked here. Any google image containing meaningful pictures/ text (quotes/sustainability related) will also be marked under this.

2. celebrations: posts related to wishes (happy new year, etc)

3. pending: if post only contains text " I am thrilled to announce that my journey towards building the sustainable world has begun ✨🎉", mark it as pending.

4. inappropriate: any activity containing any spam, violence, nudity, vulgar, obscene, cruelty to animals or people content.

5. inappropriate: any activity related to animal cruelty.

RETURN THE OUTPUT IN JSON FORMAT

let's say you got an image which should be mark under earthivist and where the face is visible then the output should be like this (and if any image does not belongs to any of these hashtags then mark hashtag as 'None')

{hashtag:'earthivist', visible:'0',number_of_faces:'2',activity_type:'indoor',game:'sudoku',posture:'standing'}

"""

def process_image_with_mediapipe(image_path):
    """Process an image file to detect faces and return the confidence score and face count."""
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(image_rgb)
    face_count = 0
    confidence_scores = []

    if results.detections:
        face_count = len(results.detections)
        for detection in results.detections:
            confidence_scores.append(detection.score[0])

    average_confidence_score = np.mean(confidence_scores) if confidence_scores else 0
    average_confidence_score = round(average_confidence_score, 1)

    return face_count, average_confidence_score

def js_object_to_dict(js_object_str):
    """Convert a JavaScript object-like string to a Python dictionary.""" 
    js_object_str = js_object_str.replace("'", '"')
    js_object_str = re.sub(r'(\w+):', r'"\1":', js_object_str);
    js_object_to_fict
    try:
        return json.loads(js_object_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {}

@app.route('/processexcelll', methods=['POST'])
def process_excel_images():
    try:
        # Check if a file is present in the request
        if 'file' not in request.files:
            return jsonify({"Error": "No file provided"}), 400
        
        file = request.files['file']
        excel_path = 'updated_file.xlsx'

        # Load the existing Excel file or create a new one if it doesn't exist
        if os.path.exists(excel_path):
            df_existing = pd.read_excel(excel_path)
        else:
            df_existing = pd.DataFrame(columns=['sno', 'urls', 'hashtag', 'Gemini_hashtag'])

        # Load the uploaded Excel file
        df_new = pd.read_excel(file)

        # Ensure the necessary columns are present
        if not all(col in df_new.columns for col in ['sno', 'urls', 'hashtag', 'Gemini_hashtag']):
            return jsonify({"Error": "Excel file must contain 'sno', 'urls', 'hashtag', 'Gemini_hashtag' columns"}), 400

        confidence_threshold = 0.5  # Define your confidence threshold here
        results = []
        low_confidence_images = []

        # Compare URLs to find new ones
        existing_urls = set(df_existing['urls'].explode()) if not df_existing.empty else set()
        new_rows = df_new[~df_new['urls'].isin(existing_urls)]  # Select rows with new URLs

        if new_rows.empty:
            return jsonify({"message": "No new URLs to process."})

        # Get the maximum sno from the existing DataFrame
        max_sno = df_existing['sno'].max() if not df_existing.empty else 0

        # Iterate over each row and process the new image URLs
        for index, row in new_rows.iterrows():
            
            image_urls = row['urls'].split(',')  # Assuming URLs are comma-separated
            url_results = []
            best_confidence_score = 0
            best_output_dict = {}

            if len(image_urls) == 1:
                image_url = image_urls[0].strip()  # Remove any leading/trailing spaces

                # Download the image
                response = requests.get(image_url)
                if response.status_code != 200:
                    return jsonify({"Error": f"Failed to download image: {image_url}"}), 400

                # Save the image locally
                image_name = os.path.basename(image_url)
                image_path = os.path.join('images', image_name)
                if not os.path.exists('images'):
                    os.makedirs('images')  # Create the 'images' folder if it doesn't exist

                with open(image_path, 'wb') as f:
                    f.write(response.content)

                # Process the image with MediaPipe
                face_count, confidence_score = process_image_with_mediapipe(image_path)

                # Check if confidence score is below the threshold
                if confidence_score < confidence_threshold or confidence_score == 0:
                    low_confidence_images.append({
                        "image_url": image_url,
                        "confidence_score": confidence_score,
                        "image_order": index + 1,
                        "reason": "Low confidence score. Manual verification recommended."
                    })
                generation_config = {
                    "temperature":0,
                    "top_p":1,
                    "top_k":1,
                    "max_output_tokens":400,
                }

                safety_settings = [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_NONE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_NONE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_NONE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_NONE"
                    },
                ]
                # Process the image (passing the image link to Generative AI)
                model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                              generation_config=generation_config,
                                              safety_settings=safety_settings)
                
                uploaded_file = genai.upload_file(image_path)
                result = model.generate_content([uploaded_file, PROMPT])
                json_output = result.text

                # Convert output to Python dictionary
                output_dict = js_object_to_dict(json_output)
                output_dict["confidence_score"] = confidence_score
                output_dict["number_of_faces"] = face_count
                output_dict["image_url"] = image_url

                url_results.append(output_dict)
                best_output_dict = output_dict
                os.remove(image_path)

            else:
                for image_url in image_urls:
                    image_url = image_url.strip()

                    response = requests.get(image_url)
                    if response.status_code != 200:
                        return jsonify({"Error": f"Failed to download image: {image_url}"}), 400

                    image_name = os.path.basename(image_url)
                    image_path = os.path.join('images', image_name)
                    if not os.path.exists('images'):
                        os.makedirs('images')

                    with open(image_path, 'wb') as f:
                        f.write(response.content)

                    face_count, confidence_score = process_image_with_mediapipe(image_path)

                    if confidence_score < confidence_threshold or confidence_score == 0:
                        low_confidence_images.append({
                            "image_url": image_url,
                            "confidence_score": confidence_score,
                            "image_order": index + 1,
                            "reason": "Low confidence score. Manual verification recommended."
                        })

                    model = genai.GenerativeModel("gemini-1.5-flash")
                    uploaded_file = genai.upload_file(image_path)
                    result = model.generate_content([uploaded_file, PROMPT])
                    json_output = result.text

                    output_dict = js_object_to_dict(json_output)
                    output_dict["confidence_score"] = confidence_score
                    output_dict["number_of_faces"] = face_count
                    output_dict["image_url"] = image_url
                    
                    url_results.append(output_dict)

                    if confidence_score > best_confidence_score:
                        best_confidence_score = confidence_score
                        best_output_dict = output_dict

                    os.remove(image_path)

                if best_confidence_score > 0:
                    best_hashtag = best_output_dict.get('hashtag', 'None')
                    for result in url_results:
                        result["hashtag"] = best_hashtag

            results.extend(url_results)
            new_rows.at[index, 'Gemini_hashtag'] = best_output_dict.get('hashtag', 'None')

        # Increment sno for new rows
        new_rows['sno'] = range(max_sno + 1, max_sno + 1 + len(new_rows))

        # Append only new rows to the existing DataFrame and save it
        df_updated = pd.concat([df_existing, new_rows], ignore_index=True)
        df_updated.to_excel(excel_path, index=False)

        if low_confidence_images:
            return jsonify({
                "results": results,
                "alert": "Manual verification needed: Some images have confidence scores below the threshold.",
                "low_confidence_images": low_confidence_images
            })

        return jsonify({
            "results": results,
            "message": f"File has been updated and saved as {excel_path}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
