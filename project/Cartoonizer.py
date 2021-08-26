import torch
from utils.transforms import get_no_aug_transform
import mimetypes
from PIL import Image
import torchvision.transforms.functional as TF
from models.generator import Generator
import numpy as np

class Cartoonizer:
    def __init__(self, pretrained_dir="./checkpoints/trained_netG.pth", user_stated_device="cpu", batch_size=4):
        self.pretrained_dir = pretrained_dir
        self.user_stated_device = user_stated_device
        self.batch_size = batch_size
        

    def inv_normalize(self, img, device):
        # Adding 0.1 to all normalization values since the model is trained (erroneously) without correct de-normalization
        mean = torch.Tensor([0.485, 0.456, 0.406]).to(device)
        std = torch.Tensor([0.229, 0.224, 0.225]).to(device)

        img = img * std.view(1, 3, 1, 1) + mean.view(1, 3, 1, 1)
        img = img.clamp(0, 1)
        return img

    def predict_images(self, image_list, device, netG):
        trf = get_no_aug_transform()
        image_list = torch.from_numpy(np.array([trf(img).numpy() for img in image_list])).to(device)

        with torch.no_grad():
            generated_images = netG(image_list)
        generated_images = self.inv_normalize(generated_images, device)

        pil_images = []
        for i in range(generated_images.size()[0]):
            generated_image = generated_images[i].cpu()
            pil_images.append(TF.to_pil_image(generated_image))
        return pil_images

    def predict_file(self, input_path, output_path, device, netG):
        # File is image
        if mimetypes.guess_type(input_path)[0].startswith("image"):
            image = Image.open(input_path).convert('RGB')
            predicted_image = self.predict_images([image], device, netG)[0]
            predicted_image.save(output_path)


    def cartoonize(self, input_path, output_path):
        user_stated_device = self.user_stated_device
        device = torch.device(user_stated_device)
        pretrained_dir = self.pretrained_dir
        netG = Generator().to(device)
        netG.eval()

        netG.load_state_dict(torch.load(pretrained_dir, map_location=torch.device('cpu')))
        self.predict_file(input_path, output_path,  device, netG)
