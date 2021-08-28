import tensorflow
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.applications.xception import Xception
from tensorflow.keras.models import load_model
from pickle import load
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import argparse

class CaptionGenerator:
    def __init__(self, caption_model, feature_model, tokenizer, max_length):
        self.caption_model = caption_model
        self.feature_model = feature_model
        self.tokenizer = tokenizer
        self.max_length = max_length

    def extract_features(self, filename):
        try:
            image = Image.open(filename)
            
        except:
            print("ERROR: Couldn't open image! Make sure the image path and extension is correct")
        image = image.resize((299,299))
        image = np.array(image)
        # for images that has 4 channels, we convert them into 3 channels
        if image.shape[2] == 4: 
            image = image[..., :3]
        image = np.expand_dims(image, axis=0)
        image = image/127.5
        image = image - 1.0
        feature = self.feature_model.predict(image)
        return feature

    def word_for_id(self, integer):
        for word, index in self.tokenizer.word_index.items():
            if index == integer:
                return word
        return None

    def generate_desc(self, photo):
        in_text = 'start'
        max_length = self.max_length
        for i in range(max_length):
            sequence = self.tokenizer.texts_to_sequences([in_text])[0]
            sequence = pad_sequences([sequence], maxlen=max_length)
            pred = self.caption_model.predict([photo,sequence], verbose=0)
            pred = np.argmax(pred)
            word = self.word_for_id(pred)
            if word is None:
                break
            in_text += ' ' + word
            if word == 'end':
                break
        clean_text = self.clean_text(in_text)
        return clean_text

    def clean_text(self, text):
        text = text.lstrip('start ')
        text = text.rstrip(' end')
        return text
    
    def get_description(self, img_path):
        photo = self.extract_features(img_path)
        description = self.generate_desc(photo)
        return description
    

if __name__ == "__main__":
    img_path = "./users/default/jobs/1/input/boat.png"

    max_length = 32
    tokenizer = load(open("tokenizer.p","rb"))
    model = load_model('checkpoints/model_9.h5')
    xception_model = Xception(include_top=False, pooling="avg")


    cg = CaptionGenerator(caption_model=model, feature_model=xception_model, tokenizer=tokenizer, max_length=max_length)
    desc = cg.get_description(img_path)
    print(desc)
    photo = cg.extract_features(img_path)
    description = cg.generate_desc(photo)

    print(description)