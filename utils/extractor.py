import exifread
from PIL import Image
from io import BytesIO

def exif_extractor(image):
    # with open(image, "rb") as img_file:
    # Extract metadata
    tags = exifread.process_file(image)
    metadata = {}
    for tag, value in tags.items():
        metadata[tag] = value
    
    # Convert IfdTag objects to strings for JSON serialization
    metadata = {tag: str(value) for tag, value in tags.items()}

    # Open the image using Pillow
    img = Image.open(image.stream)
    # Grayscale
    metadata["Grayscale"] = "Yes" if img.mode in ["L", "1"] else "No"
        
    # File size (in bytes)
    image.stream.seek(0, 2)  # Move to the end of the file
    metadata["File Size"] = image.stream.tell()
    image.stream.seek(0)  # Reset position to the start
    
    # Type of file (extension derived from MIME type)
    metadata["File Type"] = image.mimetype.split('/')[-1].upper()
    
    width = img.width
    height = img.height
    metadata["Width"] = width
    metadata["Height"] = height
    
    # Bit depth
    if img.mode == "1":
        metadata["Bit Depth"] = 1  # 1-bit images
    elif img.mode in ["L", "P"]:
        metadata["Bit Depth"] = 8  # 8-bit images
    elif img.mode in ["RGB", "YCbCr"]:
        metadata["Bit Depth"] = 24  # 8 bits per channel * 3 channels
    elif img.mode == "RGBA":
        metadata["Bit Depth"] = 32  # 8 bits per channel * 4 channels
    else:
        metadata["Bit Depth"] = "Unknown"

    # Quality classification based on resolution
    resolution = width * height
    if resolution >= 3840 * 2160:  # 4K (or higher)
        metadata["Quality"] = "4K or higher"
    elif resolution >= 2560 * 1440:  # 2K
        metadata["Quality"] = "2K"
    elif resolution >= 1920 * 1080:  # Full HD
        metadata["Quality"] = "Full HD"
    elif resolution >= 1280 * 720:  # HD
        metadata["Quality"] = "HD"
    else:
        metadata["Quality"] = "Standard Definition"
    
    return metadata