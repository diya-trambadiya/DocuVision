# DocuVision – AI-Powered Document Scanner & OCR System

DocuVision is a desktop-based document processing application built using OpenCV and OCR technologies for intelligent document enhancement, text extraction, and PDF generation workflows.

The application combines computer vision preprocessing with OCR-based text recognition to simplify document digitization and scanned-document management in a clean desktop interface.

---

## Features

- Intelligent document edge detection and perspective correction
- Image preprocessing for scanned-document enhancement
- OCR-based text extraction using EasyOCR
- Multi-image document processing
- Export scanned documents as PDF
- Save extracted OCR text as `.txt`
- Image rotation and navigation support
- Desktop GUI workflow built with Tkinter

---

## Core Workflow

```text
Upload Image
→ Document Detection
→ Perspective Transformation
→ Image Enhancement
→ OCR Text Extraction
→ PDF/Text Export
```
---

| Technology   | Purpose                              |
| ------------ | ------------------------------------ |
| Python       | Core application development         |
| OpenCV       | Image processing & document scanning |
| EasyOCR      | OCR text extraction                  |
| Tkinter      | Desktop GUI                          |
| Pillow (PIL) | Image handling                       |
| NumPy        | Image array processing               |

---
## Application Preview

Main Application Interface

OCR Text Extraction

---

## Use Cases
- Document digitization
- OCR-based text extraction
- Scanned PDF generation
- Image-to-text workflows
- Preprocessing for document AI pipelines

---
## Run Locally
pip install -r requirements.txt
pip install easyocr

python gui_app.py

---
## Folder Structure
DocuVision/

  ├── gui_app.py

  ├── scan.py

  ├── requirements.txt

  ├── output/

  ├── sample_images/

  ├── pymagesearch/

  └── screenshots/

---
## Future Improvements
- Multi-language OCR support
- Searchable PDF generation
- OCR confidence analytics
- Batch OCR export workflows
- Cloud storage integration

---
## License

This project is intended for educational and practical AI workflow experimentation purposes.

