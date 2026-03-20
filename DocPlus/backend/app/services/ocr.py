import os
import logging
import typing
import json
import numpy as np
import pypdfium2 as pdfium

os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"

logging.getLogger("ppocr").setLevel(logging.WARNING)

from paddleocr import PaddleOCR
ocr_model_global = PaddleOCR(use_angle_cls=True, lang='ro', ocr_version='PP-OCRv3')

def pdf_to_images(pdf_path: str) -> list[np.ndarray]:
    with pdfium.PdfDocument(pdf_path) as pdf:
        list_images = []
        for page in pdf:
            image_numpy = page.render(scale=4, fill_color=(255, 255, 255, 255)).to_numpy()
            image_rgb = image_numpy[:, :, :3]
            list_images.append(image_rgb)
    return list_images


def extract_text_from_images(images: list[np.ndarray], ocr_model: PaddleOCR) -> list[dict[str, typing.Any]]:
    text_list = []
    for page_number, image in enumerate(images):
        ocr_result = ocr_model.ocr(image)
        if ocr_result and ocr_result[0] is not None:
            for line in ocr_result[0]:
                result_dict = {
                    'text': line[1][0],
                    'confidence': line[1][1],
                    'bbox': line[0],
                    'page_number': page_number + 1
                }
                text_list.append(result_dict)
    return text_list


def generate_plain_text(
        extracted_data: list[dict[str, typing.Any]],
        y_threshold: int = 15,
        y_quantization: int = 15
) -> str:
    if not extracted_data:
        return ""

    sorted_data = sorted(
        extracted_data,
        key=lambda item: (
            item.get('page_number', 1),
            item['bbox'][0][1] // y_quantization,
            item['bbox'][0][0]
        )
    )

    text_parts: list[str] = []

    current_page = sorted_data[0].get('page_number', 1)
    last_y = sorted_data[0]['bbox'][0][1]

    text_parts.append(f"--- PAGINA {current_page} ---\n")

    for data in sorted_data:
        page = data.get('page_number', 1)
        current_y = data['bbox'][0][1]
        current_text = str(data.get('text', '')).strip()

        if not current_text:
            continue

        if page != current_page:
            text_parts.append(f"\n\n--- PAGINA {page} ---\n")
            current_page = page
            last_y = current_y

        else:
            if abs(current_y - last_y) > y_threshold:
                text_parts.append('\n')
            elif text_parts and not text_parts[-1].endswith('\n'):
                text_parts.append(' ')

        text_parts.append(current_text)
        last_y = current_y

    return "".join(text_parts)

def process_document(pdf_path: str) -> dict[str, typing.Any]:

    list_images = pdf_to_images(pdf_path)
    extracted_data = extract_text_from_images(list_images, ocr_model_global)
    plain_text = generate_plain_text(extracted_data)

    return {
        "file_path": pdf_path,
        "ocr_json": extracted_data,
        "text_plain": plain_text
    }



