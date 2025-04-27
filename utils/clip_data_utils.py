import numpy as np
import torch
from tqdm import tqdm
from IPython.display import display, Image
from PIL import Image as PilImage

class CustomImageDataSet(torch.utils.data.Dataset):
    def __init__(self, img_paths, transform):
        self.transform = transform
        self.img_paths = img_paths

    def __len__(self):
        return len(self.img_paths)

    def get_image_name(self, idx):
        return self.img_paths[idx]

    def __getitem__(self, idx):
        img_loc = self.img_paths[idx]
        image = PilImage.open(img_loc).convert("RGB")
        tensor_image = self.transform(image)
        return tensor_image

class SimpleTextDataset(torch.utils.data.Dataset):

    def __init__(self, texts):
        self.texts = texts

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        return self.texts[idx]

def precompute_text_features(loader, language_model):
    text_features = []

    for i, (texts) in enumerate(tqdm(loader)):
        embedding = language_model(texts)
        embedding = embedding / np.linalg.norm(embedding)

        text_features.extend(embedding)

    return np.array(text_features)

def precompute_image_features(loader, image_model):
    image_features = []
    for i, (images) in enumerate(tqdm(loader)):
        features =image_model(images)
        features = features / np.linalg.norm(features, axis=1, keepdims=True)
        image_features.extend(features)
    return np.array(image_features)

def text_encoder(text, language_model):
    embedding = language_model(text)
    embedding = embedding / np.linalg.norm(embedding)
    return embedding

def image_encoder(image):
    features =image_model(image)
    features = features / np.linalg.norm(features)
    return features

def find_image(text_query, image_features, image_dataset, language_model, n=1):
    text_embedding = text_encoder(text_query, language_model)
    text_embedding = text_embedding / np.linalg.norm(text_embedding)
    distances = np.dot(image_features, text_embedding.reshape(-1, 1))
    file_paths = []
    for i in range(1, n+1):
        idx = np.argsort(distances, axis=0)[-i, 0]
        file_paths.append(image_dataset.get_image_name(idx))
    return file_paths


def show_images(image_list):
    for im_path in image_list:
        display(Image(filename=im_path))
