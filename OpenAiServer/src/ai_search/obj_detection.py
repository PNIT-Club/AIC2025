import os
import glob
import torch
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
from PIL import Image, ImageDraw, ImageFont
import random


# generate random RGB tuple
def random_rgb():
    return (random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255))


def display(image_path, boxes, labels=None, scores=None):
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()

    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box
        color = random_rgb()
        draw.rectangle([x1, y1, x2, y2], outline=color, width=2)

        label_text = ""
        if labels:
            label_text += str(labels[i])
        if scores:
            label_text += f" {scores[i]:.2f}"

        if label_text:
            text_size = draw.textbbox((x1, y1), label_text, font=font)
            draw.rectangle([text_size[0], text_size[1], text_size[2], text_size[3]], fill="purple")
            draw.text((x1, y1), label_text, fill="white", font=font)

    # Show image
    img.show()

    return img


MODEL_ID = "IDEA-Research/grounding-dino-tiny"
DEVICE = "cpu"
ALL_LABELS = [["door", "cup", "window", "yellow tree", "human", "sign"]]


class DinoDetect:
    def __init__(self, model_id=MODEL_ID, device=DEVICE):
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForZeroShotObjectDetection.from_pretrained(model_id).to(device)
        self.text_cache = self.processor(text=ALL_LABELS, return_tensors="pt").to(device)

    def detect(self, image_path: str, confidence_threshold=0.36, display_result=False):
        image = Image.open(image_path)
        encoded_image = self.processor(images=image, return_tensors="pt").to(self.model.device)

        inputs = {**encoded_image, **self.text_cache}

        with torch.no_grad():
            outputs = self.model(**inputs)

        results = self.processor.post_process_grounded_object_detection(
            outputs=outputs,
            input_ids=inputs["input_ids"],
            target_sizes=[image.size[::-1]]
        )

        result = results[0]

        labels = []
        bboxes = []
        scores = []
        for score, label, box in zip(result["scores"], result["text_labels"], result["boxes"]):
            if score >= confidence_threshold:
                labels.append(label)
                bboxes.append([int(x) for x in box.tolist()])
                scores.append(round(score.item(), 2))

        res = []
        for label, bbox, score in zip(labels, bboxes, scores):
            res.append({"label": label, "bbox": bbox, "conf": score})

        if display_result:
            display(image_path, bboxes, labels, scores)

        return res


if __name__ == "__main__":
    counter = 0

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Root/
    IMAGE_DIR = os.path.join(BASE_DIR, "res", "images", "L21_V001")
    IMAGE_LIST = os.listdir(IMAGE_DIR)

    dino_detector = DinoDetect()
    for img_name in IMAGE_LIST:
        detections = dino_detector.detect(os.path.join(IMAGE_DIR, img_name), display_result=True)
        print(detections)
        counter += 1;

        if counter > 20:
            break