# OCR Scanned Text Extraction Challenges

This example demonstrates how Optical Character Recognition (OCR) extracts text from an image, simulating a scanned PDF bank statement. It highlights the capabilities and common challenges of OCR, such as misinterpreting similar-looking characters (e.g., '1' vs 'l', '0' vs 'O', '5' vs 'S') and handling special characters. The script generates a sample image, performs OCR using Tesseract, and then prints the extracted text along with a basic analysis of potential errors, illustrating why post-processing is often necessary for accurate data extraction from scanned documents.

## Language

`python`

## How to Run

1. Install Python dependencies: `pip install Pillow pytesseract`
2. Install Tesseract OCR engine on your system. For installation guides, visit: `https://tesseract-ocr.github.io/tessdoc/Installation.html`. Also ensure the 'tur' language data is installed for Tesseract (e.g., `sudo apt-get install tesseract-ocr-tur` on Debian/Ubuntu).
3. If Tesseract is not in your system's PATH, set the `TESSERACT_PATH` environment variable to its executable path (e.g., `export TESSERACT_PATH=/usr/local/bin/tesseract` on Linux/macOS, or `set TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe` on Windows), or modify the `pytesseract.pytesseract.tesseract_cmd` line in the script.
4. Run the script: `python main.py`

## Original Article

This example accompanies the Turkish article: [Bank Statement PDF'lerini CSV'ye Dönüştürme, Bölüm 3: Taranmış PDF Yolu - OCR Neler Yaptı, Neler Yapmadı](https://fatihsoysal.com/blog/bank-statement-pdflerini-csvye-donusturme-bolum-3-taranmis-pdf-yolu-ocr-neler-yapti-neler-yapmadi/).

## License

MIT — see [LICENSE](LICENSE).
