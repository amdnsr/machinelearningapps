from transformers import BartForConditionalGeneration, BartTokenizer, PretrainedConfig, pipeline

import os
from pprint import pprint

class TextSummarizer:
    # https://huggingface.co/transformers/model_doc/bart.html#bartforconditionalgeneration
    def __init__(self, model_directory):
        self.model_directory = model_directory
        self.files_dict = {}
    
        self._load_files()

        pprint(self.files_dict)
        config = PretrainedConfig(config_file=self.files_dict["config_file"])
        tokenizer = BartTokenizer(vocab_file=self.files_dict["vocab_file"], merges_file=self.files_dict["merges_file"])
        # tokenizer = BartTokenizer("my_model_directory/vocab.json", "my_model_directory/merges.txt")

        # Loading the model
        # https://huggingface.co/transformers/installation.html#offline-mode

        # loading the model without config variable
        self.model = BartForConditionalGeneration.from_pretrained(model_directory, cache_dir=None)
        
        # loading the model with config variable, in this case, we can add/modify the config values using the kwargs
        # https://huggingface.co/transformers/main_classes/model.html#transformers.PreTrainedModel.from_pretrained
        # self.model = BartForConditionalGeneration.from_pretrained(model_directory, cache_dir=None, config=config)

        # Starting the summarization pipeline
        self.bart_summarization_pipeline = pipeline(task="summarization", model=self.model, tokenizer=tokenizer)
        
    def _load_files(self):
        model_directory = self.model_directory

        # creating file paths
        config_file = self.join_path(model_directory, "config.json")
        merges_file = self.join_path(model_directory, "merges.txt")
        tokenizer_file = self.join_path(model_directory, "tokenizer.json")
        vocab_file = self.join_path(model_directory, "vocab.json")

        # adding the paths to the files_dict
        self.files_dict["config_file"] = config_file
        self.files_dict["merges_file"] = merges_file
        self.files_dict["tokenizer_file"] = tokenizer_file
        self.files_dict["vocab_file"] = vocab_file

    def join_path(self, p1, p2):
        return os.path.join(p1, p2)
        # return p1 + "/" + p2

    def get_summary(self, text):
        summary_list = self.bart_summarization_pipeline(text, max_length=150)
        summary = summary_list[0]['summary_text']
        return summary


if __name__ == "__main__":
    text = \
    """"
        We present BART, a denoising autoencoder for pretraining sequence-to-sequence models. BART is trained by (1) corrupting text with an arbitrary noising function, and (2) learning a model to reconstruct the original text. It uses a standard Tranformer-based neural machine translation architecture which, despite its simplicity, can be seen as generalizing BERT (due to the bidirectional encoder), GPT (with the left-to-right decoder), and many other more recent pretraining schemes. We evaluate a number of noising approaches, finding the best performance by both randomly shuffling the order of the original sentences and using a novel in-filling scheme, where spans of text are replaced with a single mask token. BART is particularly effective when fine tuned for text generation but also works well for comprehension tasks. It matches the performance of RoBERTa with comparable training resources on GLUE and SQuAD, achieves new state-of-the-art results on a range of abstractive dialogue, question answering, and summarization tasks, with gains of up to 6 ROUGE. BART also provides a 1.1 BLEU increase over a back-translation system for machine translation, with only target language pretraining. We also report ablation experiments that replicate other pretraining schemes within the BART framework, to better measure which factors most influence end-task performance.
    """

    textsummarizer = TextSummarizer("my_model_directory")
    summary = textsummarizer.get_summary(text)
    pprint(text)
    print("-"*50)
    pprint(summary)
