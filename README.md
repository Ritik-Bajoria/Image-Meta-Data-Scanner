# Metadata Extractor API

Welcome to the **Metadata Extractor API**! This API allows you to upload image files (JPEG, PNG, TIFF) and extract metadata such as EXIF, GPS, and other image-related information. It's built using **Flask**, and the metadata is stored in **MongoDB**. The API provides detailed information about each image's metadata, which can be used for various purposes like image analysis, tracking, or auditing.

## Features

- **Upload Image**: Upload an image file (JPEG, PNG, TIFF).
- **Extract Metadata**: The API reads the EXIF data (if available) and other related metadata from the image.
- **MongoDB Storage**: All extracted metadata is stored in a MongoDB database for future access and analysis.
- **Swagger UI**: API documentation is provided via Swagger UI for ease of use.

## Installation

### Requirements

To run this app, you'll need the following tools installed:

- Python 3.8 or higher
- MongoDB (or use the Docker container for MongoDB)
- Docker (optional, for containerized deployment)

### Install Dependencies

To install the required dependencies, create a virtual environment and install from `requirements.txt`:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
