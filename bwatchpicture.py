# views.py
import requests
import cv2
import numpy as np
from bs4 import BeautifulSoup

def filter_images(image_urls, sample_image_url):
    # Load the sample image
    response = requests.get(sample_image_url)
    image = np.asarray(bytearray(response.content), dtype="uint8")
    sample_image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    if sample_image is None:
        print("Error loading sample image")
        return None

    sample_gray = cv2.cvtColor(sample_image, cv2.COLOR_BGR2GRAY)

    for image_url in image_urls:
        # Load the image from the URL
        response = requests.get(image_url)
        image = np.asarray(bytearray(response.content), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        if image is None:
            print("Error decoding image")
            continue
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Compare the images using the ORB (Oriented FAST and Rotated BRIEF) feature detector
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(sample_gray, None)
        kp2, des2 = orb.detectAndCompute(gray, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)

        # Check if the image is a match
        if len(matches) > 20:
            return image_url

mmsi = 257863000
# Define the search query
name = "ABRAMIS"

# Fetch images using the Unsplash API
response = requests.get(f"https://www.fotoalfi.com/skip/p/{name}.html")
if (response.status_code != 200):
    print("Error loading images, status code:", response.status_code)

data = response.json()
image_urls = [item["urls"]["regular"] for item in data["results"]][:100]

# Filter the images to find the one you want
sample_image_url = image_urls[0]
image_url = filter_images(image_urls, sample_image_url)

print(image_url)


"""
import os
import openai

openai.api_key = "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"

prompt = "mmsi 257863000 boat image"
n = 1
size = "1024x1024"

response = openai.Image.create(
    prompt=prompt,
    n=n,
    size=size
)

print(response)
"""