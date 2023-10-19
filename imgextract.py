import os
import fitz  # PyMuPDF
import io
from PIL import Image


def pdf_image_extract(pdf_path):
    # Open the PDF file
    pdf_file_path = "unscraped/" + pdf_path
    pdf_file = fitz.open(pdf_file_path)

    # Extract filename from pdf filename
    filename = os.path.basename(pdf_path)

    # Create image folder, without .pdf extension
    img_folder = f"extracted/images/{os.path.splitext(filename)[0]}"

    # Create image folder if not exists
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    # Loop through each page
    for page_num in range(len(pdf_file)):
        page = pdf_file[page_num]

        # Get image list
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]

            # Open the image with PIL
            image = Image.open(io.BytesIO(image_bytes))

            # Save the image
            image_path = f"{img_folder}/image{page_num}_{img_index}.png"
            image.save(image_path)
            print(f"Saved {image_path}")

    # Move pdf file to scraped folder
    os.rename(pdf_file_path, "scraped/" + pdf_path)
    print(f"Moved {pdf_path} to scraped folder\n")


# Find all pdf in unscraped folder
for pdf_path in os.listdir("unscraped"):
    if pdf_path.endswith(".pdf"):
        print(f"Extracting images from {pdf_path}...")
        pdf_image_extract(pdf_path)
