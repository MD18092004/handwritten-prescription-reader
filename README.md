# 📄 Handwritten Prescription Reader

A computer vision tool that reads handwritten medical prescriptions from images using OCR (Optical Character Recognition). It detects and extracts handwritten text, draws bounding boxes around each detected word or phrase, and saves both annotated images and plain-text outputs.

---

## 🩺 Problem Statement

Handwritten prescriptions are still widely used in clinics and hospitals — especially in resource-limited settings. They are difficult to digitize, prone to misreading, and create barriers to record-keeping and pharmacy automation. This tool addresses that problem by automatically extracting text from prescription images using a pre-trained OCR model, with no manual transcription required.

---

## 🎯 Features

- Processes an entire folder of prescription images in one command
- Detects and extracts handwritten (and printed) text using EasyOCR
- Draws bounding boxes around detected text with confidence scores
- Saves annotated images for visual verification
- Saves extracted text to `.txt` files for further use
- Configurable confidence threshold to filter low-quality detections

---

## 🗂️ Project Structure

```
handwritten-prescription-reader/
├── main.py               # Main script — run this
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── sample_images/        # Put your prescription images here
│   └── (add .jpg / .png files here)
└── output/               # Results appear here after running
    ├── image1_annotated.jpg
    ├── image1_extracted.txt
    └── ...
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/handwritten-prescription-reader.git
cd handwritten-prescription-reader
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** EasyOCR will automatically download the OCR model (~100 MB) the first time you run the script. Make sure you have an internet connection for the first run.

---

## 🚀 How to Use

### Step 1 — Add Your Images

Place your prescription images (`.jpg`, `.jpeg`, `.png`, `.bmp`, or `.tiff`) inside the `sample_images/` folder.

> You can find sample handwritten datasets on Kaggle, such as the [IAM Handwriting Dataset](https://www.kaggle.com/datasets/naderabdalghani/iam-handwritten-forms-dataset) or search for "handwritten prescription dataset".

### Step 2 — Run the Script

```bash
python main.py
```

This uses default settings:
- Input folder: `sample_images/`
- Output folder: `output/`
- Confidence threshold: 20%

### Step 3 — Custom Options

```bash
python main.py --input my_images --output results --confidence 0.3
```


| `--input` | Folder containing input images | `sample_images` |
| `--output` | Folder to save results | `output` |
| `--confidence` | Min confidence threshold (0.0–1.0) | `0.2` |

---

## 📤 Output

For each image processed, two files are created in the output folder:

**1. Annotated Image** (`imagename_annotated.jpg`)
- The original image with green bounding boxes drawn around detected text
- Each box is labeled with the detected word and its confidence score

**2. Text File** (`imagename_extracted.txt`)
- Plain text output of everything detected in the image
- Each line includes the detected text and its confidence score

Example text output:
```
=== Extracted Prescription Text ===

Tab. Amoxicillin 500mg  [confidence: 74%]
1-0-1 x 5 days  [confidence: 61%]
Cap. Omeprazole 20mg  [confidence: 68%]
SOS  [confidence: 55%]
```

---

## 🛠️ Technology Used


| [EasyOCR](https://github.com/JaidedAI/EasyOCR) | Pre-trained OCR model for text detection & recognition |
| [OpenCV](https://opencv.org/) | Image loading, annotation, and saving |
| [NumPy](https://numpy.org/) | Array operations for bounding box drawing |
| [Pillow](https://python-pillow.org/) | Supplementary image handling |

---

## ⚠️ Limitations

- Works best with clear, well-lit images
- Accuracy may be lower on very messy or cursive handwriting
- Does not interpret the meaning of prescriptions — only extracts text
- Currently supports English only

---

## 🔮 Possible Future Improvements

- Add a simple web interface (Flask/Streamlit) for drag-and-drop uploads
- Support multiple languages
- Use a fine-tuned model trained specifically on medical handwriting
- Parse extracted text into structured fields (medicine name, dosage, frequency)

---

## 📚 Dataset Suggestions

| IAM Handwriting Dataset | https://www.kaggle.com/datasets/naderabdalghani/iam-handwritten-forms-dataset |
| Handwritten Medical Prescriptions | Search "handwritten prescription" on Kaggle |
| IMGUR / Google Images | Search "handwritten doctor prescription" for quick test images |

---

## 👨‍💻 Author

DYAVANI MANISH
Computer Vision Course — BYOP Capstone Project
VIT / VIT Bhopal University

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
