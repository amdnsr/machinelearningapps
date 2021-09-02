# Machine Learning Apps

This project aims to serve as the frontend user interface, to run various machine learning models like ***captiongeneration***, ***cartoonization*** and ***textsummarization***.
The actual deployment of the models is on another service, and this website connects to the service via *API protocols*.
The reason behind separation of the models and the frontend was taken, so as to ease the testing of the frontend, as well as make it easier to add support for newer models later in the future. 

## Requirements

To run the service, setup the API service, and edit it's home url in the `website_data` file.
Then, create a virtual environment for the website, and install the requirements by running the following command.:

```setup
pip install -r requirements.txt
```

## Usage

Change the working directory to `project`
Then, export the following `environment variables`
```usage
export FLASK_APP=application.py
export FLASK_DEBUG=1 # only in case of debugging else set it to 0
export EMAIL_ADDRESS=""
export PASSWORD=""
```
* `EMAIL_ADDRESS` should be the actual **Gmail** address from which the email will be sent and `PASSWORD` will be the password of the corresponding email address.

* By default the home address is the [localhost](http://127.0.0.1:5000/) If we are using an online webserver, then we'd have to replace the [localhost](http://127.0.0.1:5000/)  with the corresponding home address in the website_data.py file

* To use the email sender code, we need to allow [DisplayUnlockCaptcha](https://accounts.google.com/DisplayUnlockCaptcha) and [less secure apps](https://myaccount.google.com/lesssecureapps)

Finally, run the project using:
```
flask run
```
## Test

- Create an account and create a job
- Upload a single image per job
- The default examples for each task types are shown below
    1. captiongeneration
    2. cartoonization
    3. textsummarization

|<center> S. No. <center>| <center>Input</center> | <center>Result</center>|
|:-------:|----------|----------------------------------------------|
|1|<center><img src="project/users/default/jobs/1/input/boat.png" alt="input_image" height="200" width="200"/></center> | <center>man in yellow kayak is paddling through the water</center>|
|2|<center><img src="project/users/default/jobs/2/input/river.png" alt="input_image" height="200" width="200"/></center> | <center><img src="project/users/default/jobs/2/output/result_river.png" alt="cartoonized_image" width="200" /></center>|
|3|<center>We present BART, a denoising autoencoder for pretraining sequence-to-sequence models. BART is trained by (1) corrupting text with an arbitrary noising function, and (2) learning a model to reconstruct the original text. It uses a standard Tranformer-based neural machine translation architecture which, despite its simplicity, can be seen as generalizing BERT (due to the bidirectional encoder), GPT (with the left-to-right decoder), and many other more recent pretraining schemes. We evaluate a number of noising approaches, finding the best performance by both randomly shuffling the order of the original sentences and using a novel in-filling scheme, where spans of text are replaced with a single mask token. BART is particularly effective when fine tuned for text generation but also works well for comprehension tasks. It matches the performance of RoBERTa with comparable training resources on GLUE and SQuAD, achieves new state-of-the-art results on a range of abstractive dialogue, question answering, and summarization tasks, with gains of up to 6 ROUGE. BART also provides a 1.1 BLEU increase over a back-translation system for machine translation, with only target language pretraining. We also report ablation experiments that replicate other pretraining schemes within the BART framework, to better measure which factors most influence end-task performance.</center> |<center> BART is a denoising autoencoder for pretraining sequence-to-sequence models. It is trained by corrupting text with an arbitrary noising function, and learning a model to reconstruct the original text. BART is particularly effective when fine tuned for text generation but also works well for comprehension tasks.</center>|

## Credits
- [Filip Andersson](https://github.com/FilipAndersson245)