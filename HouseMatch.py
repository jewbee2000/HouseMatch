""" 
Author: Walter Teitelbaum
Date: 11/30/2023

Description: This file is used to find similar images to a base image in a folder.

Usage: Set 'query_image_path' to the path of your reference image.
       Set 'directory_path'to the path of your directory containing photos to compare
       Set 'top_n' equal to the number of most similar photos you'd like to find.
       Run the scirpt. It make take about a second per comparison.

Notes: GPT 3.5 helped me write part of this script
"""

import cv2
import numpy as np
import tensorflow as tf
import keras
from sklearn.metrics.pairwise import cosine_similarity
import os

def load_and_preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))  # Input size for ResNet50
    img = keras.applications.resnet.preprocess_input(img)
    return img

def extract_features(image_path, model):
    img = load_and_preprocess_image(image_path)
    features = model.predict(np.expand_dims(img, axis=0))
    return features.flatten()

def find_similar_images(query_image_path, directory_path, top_n=2):
    # Load pre-trained ResNet50 model
    model = keras.applications.ResNet50(weights='imagenet', include_top=False, pooling='avg')

    # Extract features for the query image
    query_features = extract_features(query_image_path, model)

    similar_images = []

    # Iterate through all images in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(directory_path, filename)

            # Extract features for the current image
            image_features = extract_features(image_path, model)

            # Calculate cosine similarity between query and current image features
            similarity = cosine_similarity([query_features], [image_features])[0][0]

            # Store the image path and similarity score
            similar_images.append((image_path, similarity))

    # Sort the images by similarity score in descending order
    similar_images.sort(key=lambda x: x[1], reverse=True)

    # Return the top N similar images
    return similar_images[:top_n]

def main():
    # Replace these paths with the actual paths
    query_image_path = 'test1.jpg'
    directory_path = 'C:\\Downloads\\street_view_images'

    similar_images = find_similar_images(query_image_path, directory_path)

    if similar_images:
        print("Top similar images found:")
        for image_path, similarity in similar_images:
            print(f"{image_path} - Similarity: {similarity:.4f}")
    else:
        print("No similar images found.")

if __name__ == "__main__":
    main()
