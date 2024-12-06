import logging

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Create the Logger
loggers = logging.getLogger(__name__)

class LLMAugmenter():
    """
    A class to perform data augmentation using Large Language Models (LLMs).

    Methods:
    --------
    init_qn_ans_model():
        Initializes the question-answering model.
    init_summarizer_model():
        Initializes the summarizer model.
    paraphrase_with_question(sentence, max_new_tokens=512):
        Generates a paraphrase of the given sentence using the question-answering model.
    summarize_with_summarizer(text, max_length=100, min_length=30):
        Summarizes the given text using the summarizer model.
    """
    def __init__(self):
        self.model_name: str
        self.model:AutoModelForCausalLM
        self.tokenizer:AutoTokenizer
        loggers.info("LLMAugmenter initialized")
         
    def init_qn_ans_model(self):
        """
        Initializes the question-answering model.
        """
        self.model_name = "Qwen/Qwen2.5-1.5B-Instruct"
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype="auto",
            device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
    
    def init_summarizer_model(self):
        """
        Initializes the summarizer model.
        """
        device = 0 if torch.cuda.is_available() else -1
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)

    def paraphrase_with_question(self, sentence: str, max_new_tokens=512):
        """
        Generates a paraphrase of the given sentence using the question-answering model.

        :param sentence: The sentence to be paraphrased.
        :type sentence: str
        :param max_new_tokens: The maximum number of new tokens to generate (default is 512).
        :type max_new_tokens: int
        :return: The paraphrased sentence.
        :rtype: str
        """
        if not hasattr(self, 'model'):
            self.init_qn_ans_model()
        
        prompt =f"Answer the following following english paraphrase question. what is the paraphrase of the following sentence if you cannot repeat the verb phrases used in the given sentence? {sentence}"
        messages = [
            {"role": "system", "content": "You are Qwen, you are tasked to paraphrase english sentences that are given to you."},
            {"role": "user", "content": prompt}
        ]
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=max_new_tokens
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response

    def summarize_with_summarizer(self, text: str, max_length = 100, min_length = 30):
        """
        Summarizes the given text using the summarizer model.

        :param text: The text to be summarized.
        :type text: str
        :param max_length: The maximum length of the summary (default is 100).
        :type max_length: int
        :param min_length: The minimum length of the summary (default is 30).
        :type min_length: int
        :return: The summarized text.
        :rtype: str
        """
        if not hasattr(self, 'summarizer'):
            self.init_summarizer_model()
        text = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return text[0]['summary_text']