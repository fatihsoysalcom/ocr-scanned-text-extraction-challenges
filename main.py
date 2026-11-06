from PIL import Image, ImageDraw, ImageFont, ImageFilter
import pytesseract
import os
import random

# --- Configuration ---
# Path to the Tesseract executable. Change this if Tesseract is not in your PATH.
# Example for Windows: r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Example for Linux/macOS: '/usr/local/bin/tesseract' or simply 'tesseract' if in PATH
pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_PATH', 'tesseract')

# --- 1. Create a simulated "scanned" image with text ---
# This simulates a portion of a bank statement that might be hard for OCR.
# We'll include some ambiguous characters and slight imperfections.
image_filename = "simulated_bank_statement_snippet.png"
img_width, img_height = 600, 250
img = Image.new('RGB', (img_width, img_height), color = (255, 255, 255))
d = ImageDraw.Draw(img)

# Attempt to load a common font, fallback to default if not found
try:
    font = ImageFont.truetype("arial.ttf", 24)
except IOError:
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except IOError:
        font = ImageFont.load_default() # Fallback to a basic font

# Simulate some bank statement data with potential OCR challenges
text_lines = [
    "İşlem Tarihi: 01.03.2023",
    "Açıklama: EFT GÖNDERİMİ - FATURA ÖDEMESİ",
    "Tutar: 1,250.50 TL (Bin İki Yüz Elli)", # '1' vs 'l', '0' vs 'O'
    "Hesap No: 5432109876", # '5' vs 'S', '0' vs 'O'
    "Referans: 1Z34567890" # 'Z' vs '2', '0' vs 'O'
]

y_offset = 20
for line in text_lines:
    d.text((30, y_offset), line, fill=(0,0,0), font=font)
    y_offset += 35

# Add some slight imperfections to simulate a scanned document
# Add random small lines/dots (noise)
for _ in range(70):
    x, y = random.randint(0, img_width-1), random.randint(0, img_height-1)
    d.point((x, y), fill=(random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)))

# Apply a slight blur and rotation to simulate a less-than-perfect scan
img = img.filter(ImageFilter.GaussianBlur(radius=0.5)) # Slight blur
img = img.rotate(random.uniform(-0.5, 0.5), expand=False, fillcolor=(255,255,255)) # Slight rotation

img.save(image_filename)
print(f"Simulated scanned image '{image_filename}' created.")

# --- 2. Perform OCR on the simulated image ---
print(f"\nPerforming OCR on '{image_filename}'...")
try:
    # Use Turkish language model ('tur') for better accuracy on Turkish text.
    # Tesseract needs the 'tur' language data installed.
    extracted_text = pytesseract.image_to_string(Image.open(image_filename), lang='tur')
    print("\n--- OCR Extracted Text ---")
    print(extracted_text.strip())
    print("--------------------------")

    # --- 3. Analyze and highlight potential OCR challenges ---
    print("\n--- OCR Analysis ---")
    original_text_joined = "\n".join(text_lines)
    print("Original text (for comparison):")
    print(original_text_joined)

    # Simple checks for common OCR misinterpretations. Actual OCR output may vary.
    if "1,250.50" not in extracted_text and ("l,250.50" in extracted_text or "I,250.50" in extracted_text):
        print("\nPotential OCR error: '1' (one) might have been misread as 'l' (lowercase L) or 'I' (uppercase I) in '1,250.50'.")
    if "5432109876" not in extracted_text and ("S432109876" in extracted_text or "54321O9876" in extracted_text):
        print("\nPotential OCR error: '5' (five) might have been misread as 'S', or '0' (zero) as 'O' (uppercase O) in 'Hesap No'.")
    if "1Z34567890" not in extracted_text and ("1234567890" in extracted_text or "IZ34567890" in extracted_text):
        print("\nPotential OCR error: 'Z' might have been misread as '2', or '1' as 'I' in 'Referans'.")
    if "ÖDEMESİ" not in extracted_text and "ODEMESI" in extracted_text:
        print("\nPotential OCR error: Turkish character 'Ö' might be misread as 'O' if language model is not perfectly tuned or font is unusual.")
    
    print("\nThis example demonstrates that OCR can extract text from image-based documents (like scanned PDFs),")
    print("but it's not always perfect. Ambiguous characters, noise, and document quality can lead to errors.")
    print("Therefore, manual verification or sophisticated post-processing logic is often required for accurate data extraction.")

except pytesseract.TesseractNotFoundError:
    print("\nERROR: Tesseract OCR engine not found.")
    print("Please ensure Tesseract is installed and its executable path is correctly configured.")
    print("You can set the TESSERACT_PATH environment variable or modify the 'pytesseract.pytesseract.tesseract_cmd' line in the script.")
    print("For Tesseract installation instructions, visit: https://tesseract-ocr.github.io/tessdoc/Installation.html")
    print("Also ensure the 'tur' language data is installed (e.g., 'sudo apt-get install tesseract-ocr-tur' on Debian/Ubuntu).")
except Exception as e:
    print(f"\nAn unexpected error occurred during OCR: {e}")

# --- Cleanup (optional) ---
# Uncomment the line below to remove the generated image after execution.
# os.remove(image_filename)
# print(f"\nCleaned up: '{image_filename}' removed.")
