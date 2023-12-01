""" 
Author: Walter Teitelbaum
Date: 11/30/2023

Description: This file is used to download a batch of google street view
             images from a specific area.

Usage: Specify a location with coordinates, a radius in feet, and a spacing in feet.
       You will also have to replace YOUR_API_KEY with a valid Maps API key from google.
       Run the script, and wait for all the files to download from google.

Notes: GPT 3.5 helped me write part of this script
"""


import os
import requests
from math import radians, sin, cos, sqrt, atan2


def calculate_distance(coord1, coord2):
    # Calculate the distance between two sets of coordinates using Haversine formula

    R = 6371.0  # Radius of the Earth in kilometers

    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance_km = R * c

    # Convert distance from kilometers to feet
    distance_feet = distance_km * 3280.84

    return distance_feet


def generate_coordinate_grid(center_coord, radius_feet, spacing_feet):
    grid = []

    # Calculate the number of steps in latitude and longitude
    lat_steps = int(radius_feet / spacing_feet)
    lon_steps = int(radius_feet / spacing_feet)

    # Iterate through latitude steps
    for lat_step in range(-lat_steps, lat_steps + 1):
        # Iterate through longitude steps
        for lon_step in range(-lon_steps, lon_steps + 1):
            # Calculate the current coordinates
            current_coord = (
                center_coord[0] + lat_step * (spacing_feet / 364567.2),
                center_coord[1] + lon_step * (spacing_feet / 364567.2)
            )

            # Calculate the distance from the center coordinate
            distance = calculate_distance(center_coord, current_coord)

            # Check if the current coordinate is within the specified radius
            if distance <= radius_feet:
                grid.append(current_coord)

    return grid


def download_street_view_image(api_key, location, filename, heading, size="640x480", fov=90, pitch=1):
    base_url = "https://maps.googleapis.com/maps/api/streetview"

    params = {
        "size": size,
        "location": f"{location[0]},{location[1]}",
        "heading": heading,
        "fov": fov,
        "pitch": pitch,
        "key": api_key,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to download image for {location}. Status code: {response.status_code}")


def main():
    api_key = "YOUR_API_KEY"
    location = (47.66284282810757, -122.33663859881885)  # Example: Wallingford coordinates
    radius_feet = 300.0
    output_folder = "street_view_images"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    spacing_feet = 200.0
    coordinate_grid = generate_coordinate_grid(location, radius_feet, spacing_feet)

    for coord in coordinate_grid:
        headings = [0, 90, 180, 270]
        for heading in headings:

            filename = os.path.join(output_folder, f"{coord[0]}_{coord[1]}_{heading}.jpg")
            # Download Street View image for the current location
            download_street_view_image(api_key, coord, filename, heading)

    print("Image download complete.")


if __name__ == "__main__":
    main()
