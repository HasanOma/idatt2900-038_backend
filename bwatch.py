#import requests

#ais = requests.curl("Https:")
#print(ais)

#import http.client

#conn = http.client.HTTPSConnection("live.ais.barentswatch.no")

#payload = "{}"

#headers = { 'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjBCM0I1NEUyRkQ5OUZCQkY5NzVERDMxNDBDREQ4OEI1QzA5RkFDRjNSUzI1NiIsIng1dCI6IkN6dFU0djJaLTctWFhkTVVETjJJdGNDZnJQTSIsInR5cCI6ImF0K2p3dCJ9.eyJpc3MiOiJodHRwczovL2lkLmJhcmVudHN3YXRjaC5ubyIsIm5iZiI6MTY3NTI0MjE2NiwiaWF0IjoxNjc1MjQyMTY2LCJleHAiOjE2NzUyNDU3NjYsImF1ZCI6ImFpcyIsInNjb3BlIjpbImFpcyJdLCJjbGllbnRfaWQiOiJoYXNhbnJvQHN0dWQubnRudS5ubzpNYXJpbmUgVHJhZmZpYyBQb3J0YWwifQ.T5hKpRXa6KLUNxwulc0u3u0FK-W4aCLxUpo_gxO26Z1V5qImAb_qtlivHthgTBrovR9eKF_Q8xC7ZC9Ig7j-bH5WdjCMSUXABoQIngpE_9U2H3aG2WU105-JZXUqHqJth1ccj_WjMmShTNB-QVKO_e5nHcSfaagQzeV49H2YHQIf3b8mOEdea5VkDmESjshrslUBlWQp2RK2lJqJKF2Ivxj_Llut31Eu5uKujY5gZ43dPIohLfqlWn0WK1S5VmLU4LCE4HpjnnHRLWYfZNBRFgCyxRYovXhb7CCmqhDopex1UFSVe1fQVuBGXSD7GLHoWaeysINQHgYQFl4rHFvR8PMZ2h_-QtignpVxFAiIKNhxOlyx5Vixcaj_Nx4bwYfqNZOQDIJVlc-tiz6yW3sNFIdnH4o8xWqfOhZfTAiVjQKd6IGD-qW1_e-6aFCYw3kQNeZwelGSCurETTPSAAisDY20Jrq3g8vl5desu_uVJD11KUJoMK_C-qmZW3edElqFZMt8KFLOEfe4E-ayEqWBgNr_G9cKDOkx-neIBx6bYVB86TigFU_9XD6XrIDsH9MTxUKNJNHwkNfQRhdYdPiPY_QSTXjl0nwSEdn7SU2oZZlusL5rIw-dZw-w5iDRFHyxCwDUMHFCAWYMP5xd2Rsjl2xxTxNsm8Y9RdGETpVLIHw" }

#conn.request("GET", "/v1/latest/combined", payload, headers)

#res = conn.getresponse()
#data = res.read()
#print(data.decode("utf-8"))
# views.py
import requests
import cv2
import numpy as np
from bs4 import BeautifulSoup

"""
def filter_images(image_urls, sample_image_path):
    # Load the sample image
    print("filtering")
    sample_image = cv2.imread(sample_image_path)
    response = requests.get("https:"+sample_image_path)
    print(response)
    image = np.asarray(bytearray(response.content), dtype="uint8")
    sample_image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    if sample_image is None:
        print("Error loading image from URL")
    sample_gray = cv2.cvtColor(sample_image, cv2.COLOR_BGR2GRAY)

    for image_url in image_urls:
        # Load the image from the URL
        response = requests.get("https:"+image_url)
        print(response + " in response")
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
query = f"{mmsi} boat image"

# Make a request to the search engine
response = requests.get(f"https://www.google.com/search?q={query}")
print(response)
if (response.status_code != 200):
    print("Error loading image from URL, status code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")
print(soup)
# Extract the URLs of the images
image_urls = [img.get("src") for img in soup.find_all("img")][:100]
print(image_urls)
# Filter the images to find the one you want
# ...
image_url = filter_images(image_urls, image_urls[2])

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