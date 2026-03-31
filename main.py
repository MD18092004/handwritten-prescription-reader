"""
Handwritten Prescription Reader
================================
Uses EasyOCR to extract text from handwritten prescription images.
Outputs annotated images (with bounding boxes) and text files.

Usage:
    python main.py --input sample_images --output output
"""

import os
import argparse
import easyocr
import cv2
import numpy as np
from PIL import Image


def read_prescription(image_path, reader):
    """
    Reads a single prescription image and returns OCR results.

    Args:
        image_path (str): Path to the image file.
        reader: EasyOCR reader instance.

    Returns:
        results (list): List of (bounding_box, text, confidence) tuples.
        image (numpy array): Original image loaded with OpenCV.
    """
    print(f"\n  Processing: {os.path.basename(image_path)}")

    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"  [ERROR] Could not load image: {image_path}")
        return None, None

    # Run OCR — detail=1 gives bounding boxes + confidence scores
    results = reader.readtext(image_path, detail=1)

    if not results:
        print("  [WARNING] No text detected in this image.")
    else:
        print(f"  Detected {len(results)} text region(s).")

    return results, image


def annotate_image(image, results, confidence_threshold=0.2):
    """
    Draws bounding boxes and detected text on the image.

    Args:
        image: OpenCV image (numpy array).
        results: EasyOCR results list.
        confidence_threshold: Only draw boxes above this confidence.

    Returns:
        annotated (numpy array): Image with annotations drawn.
    """
    annotated = image.copy()

    for (bbox, text, confidence) in results:
        if confidence < confidence_threshold:
            continue  # Skip low-confidence detections

        # bbox is a list of 4 points: top-left, top-right, bottom-right, bottom-left
        pts = np.array(bbox, dtype=np.int32)

        # Draw green bounding box
        cv2.polylines(annotated, [pts], isClosed=True, color=(0, 200, 0), thickness=2)

        # Put text label above the bounding box
        label = f"{text} ({confidence:.0%})"
        top_left = tuple(pts[0])
        cv2.putText(
            annotated,
            label,
            (top_left[0], max(top_left[1] - 8, 12)),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(0, 200, 0),
            thickness=1,
            lineType=cv2.LINE_AA,
        )

    return annotated


def save_text_output(results, output_text_path, confidence_threshold=0.2):
    """
    Saves extracted text to a .txt file.

    Args:
        results: EasyOCR results list.
        output_text_path (str): Path to save the text file.
        confidence_threshold: Only save text above this confidence.
    """
    lines = []
    for (_, text, confidence) in results:
        if confidence >= confidence_threshold:
            lines.append(f"{text}  [confidence: {confidence:.0%}]")

    with open(output_text_path, "w", encoding="utf-8") as f:
        f.write("=== Extracted Prescription Text ===\n\n")
        if lines:
            f.write("\n".join(lines))
        else:
            f.write("No text detected above the confidence threshold.")
        f.write("\n")

    print(f"  Text saved → {output_text_path}")


def process_folder(input_folder, output_folder, confidence_threshold=0.2):
    """
    Processes all images in a folder.

    Args:
        input_folder (str): Path to folder containing input images.
        output_folder (str): Path to folder where results will be saved.
        confidence_threshold (float): Minimum confidence to include a detection.
    """
    # Supported image extensions
    supported = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"}

    # Collect all image files
    image_files = [
        f for f in os.listdir(input_folder)
        if os.path.splitext(f)[1].lower() in supported
    ]

    if not image_files:
        print(f"[ERROR] No supported images found in '{input_folder}'.")
        print("Supported formats: JPG, JPEG, PNG, BMP, TIFF")
        return

    print(f"\nFound {len(image_files)} image(s) to process.")
    os.makedirs(output_folder, exist_ok=True)

    # Initialize EasyOCR reader (downloads model on first run, ~100MB)
    print("\nLoading OCR model... (this may take a minute on first run)")
    reader = easyocr.Reader(["en"], gpu=False)
    print("Model loaded.\n")
    print("=" * 50)

    total_words = 0
    processed = 0

    for filename in image_files:
        image_path = os.path.join(input_folder, filename)
        base_name = os.path.splitext(filename)[0]

        # Run OCR
        results, image = read_prescription(image_path, reader)
        if results is None:
            continue

        # Annotate and save image
        annotated = annotate_image(image, results, confidence_threshold)
        output_image_path = os.path.join(output_folder, f"{base_name}_annotated.jpg")
        cv2.imwrite(output_image_path, annotated)
        print(f"  Annotated image saved → {output_image_path}")

        # Save text output
        output_text_path = os.path.join(output_folder, f"{base_name}_extracted.txt")
        save_text_output(results, output_text_path, confidence_threshold)

        word_count = sum(1 for (_, _, c) in results if c >= confidence_threshold)
        total_words += word_count
        processed += 1

    print("\n" + "=" * 50)
    print(f"\nDone! Processed {processed}/{len(image_files)} image(s).")
    print(f"Total text regions extracted: {total_words}")
    print(f"Results saved to: '{output_folder}/'")


def main():
    parser = argparse.ArgumentParser(
        description="Handwritten Prescription Reader using EasyOCR"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="sample_images",
        help="Path to folder containing prescription images (default: sample_images)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output",
        help="Path to folder where results will be saved (default: output)",
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=0.2,
        help="Minimum confidence threshold (0.0 to 1.0, default: 0.2)",
    )

    args = parser.parse_args()

    print("=" * 50)
    print("   Handwritten Prescription Reader")
    print("=" * 50)
    print(f"Input folder  : {args.input}")
    print(f"Output folder : {args.output}")
    print(f"Min confidence: {args.confidence:.0%}")

    # Check that input folder exists
    if not os.path.isdir(args.input):
        print(f"\n[ERROR] Input folder not found: '{args.input}'")
        print("Please create the folder and add prescription images to it.")
        return

    process_folder(args.input, args.output, args.confidence)


if __name__ == "__main__":
    main()
