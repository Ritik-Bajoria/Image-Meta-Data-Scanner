import exifread

def exif_extractor(image):
    # with open(image, "rb") as img_file:
    # Extract metadata
    tags = exifread.process_file(image)
    if not tags:
        metadata = {"message": "This file doesn't contain any metadata"}
        return metadata
    metadata = {}
    for tag, value in tags.items():
        metadata[tag] = value
    
    # Convert IfdTag objects to strings for JSON serialization
    metadata = {tag: str(value) for tag, value in tags.items()}

    return metadata