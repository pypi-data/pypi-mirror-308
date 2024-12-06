import os
import cv2
import torch
import open_clip
import lpips
import numpy as np
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import warnings

warnings.filterwarnings("ignore")

device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, _, preprocess_clip = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
clip_model = clip_model.to(device)
lpips_model = lpips.LPIPS(net='vgg').to(device)

class CLORPS:
    def __init__(self):
        self.device = device

    @staticmethod
    def preprocess_image_clip(image_path):
        image = Image.open(image_path).convert("RGB")
        return preprocess_clip(image).unsqueeze(0).to(device)

    @staticmethod
    def get_clip_embedding(image_path):
        image = CLORPS.preprocess_image_clip(image_path)
        with torch.no_grad():
            embedding = clip_model.encode_image(image).cpu().numpy().squeeze(0)
        return embedding

    @staticmethod
    def get_lpips_distance(image1_path, image2_path):
        img1 = Image.open(image1_path).convert("RGB")
        img2 = Image.open(image2_path).convert("RGB")
        common_size = (min(img1.size[0], img2.size[0]), min(img1.size[1], img2.size[1]))
        img1 = img1.resize(common_size, Image.BICUBIC)
        img2 = img2.resize(common_size, Image.BICUBIC)
        img1_tensor = lpips.im2tensor(np.array(img1)).to(device)
        img2_tensor = lpips.im2tensor(np.array(img2)).to(device)
        with torch.no_grad():
            distance = lpips_model(img1_tensor, img2_tensor).item()
        return 1 / distance  # Inverted for similarity

    @staticmethod
    def get_orb_similarity(img1_path, img2_path):
        orb = cv2.ORB_create()
        img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)
        keypoints1, descriptors1 = orb.detectAndCompute(img1, None)
        keypoints2, descriptors2 = orb.detectAndCompute(img2, None)
        if descriptors1 is None or descriptors2 is None:
            return 0
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(descriptors1, descriptors2)
        return len(matches)

    @staticmethod
    def normalize_scores(scores):
        scaler = MinMaxScaler()
        scores = np.array(scores).reshape(-1, 1)
        return scaler.fit_transform(scores).flatten()

    def calculate_combined_similarity(self, input_image_path, target_image_paths):
        if isinstance(target_image_paths, str):
            target_image_paths = [target_image_paths]

        lpips_scores, orb_scores, clip_scores = [], [], []
        clip_embedding1 = self.get_clip_embedding(input_image_path)

        for target_image_path in target_image_paths:
            lpips_score = self.get_lpips_distance(input_image_path, target_image_path)
            lpips_scores.append(lpips_score)
            orb_score = self.get_orb_similarity(input_image_path, target_image_path)
            orb_scores.append(orb_score)
            clip_embedding2 = self.get_clip_embedding(target_image_path)
            clip_sim = cosine_similarity([clip_embedding1], [clip_embedding2])[0][0]
            clip_scores.append(clip_sim)

        lpips_scores = self.normalize_scores(lpips_scores)
        orb_scores = self.normalize_scores(orb_scores)
        clip_scores = self.normalize_scores(clip_scores)

        combined_scores = np.array(lpips_scores) + np.array(orb_scores) + np.array(clip_scores)
        return combined_scores