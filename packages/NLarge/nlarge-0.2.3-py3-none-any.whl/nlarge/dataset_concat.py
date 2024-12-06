from NLarge.random import RandomAugmenter
from NLarge.random import Action
from NLarge.synonym import SynonymAugmenter
from NLarge.llm import LLMAugmenter
import math
import random
from datasets import concatenate_datasets
import nltk
from nltk.corpus import stopwords, wordnet

class MODE:
    class RANDOM:
        SWAP = 'random.swap'
        SUBSTITUTE = 'random.substitute'
        DELETE = 'random.delete'
        CROP = 'random.crop'
    class SYNONYM:
        WORDNET = 'synonym.wordnet'
    class LLM:
        PARAPHRASE = 'llm.paraphrase'
        SUMMARIZE = 'llm.summarize'

def generate_stopwords():
    try:
        stopwords.words('english')
    except LookupError:
        nltk.download('stopwords')  

    return set(stopwords.words('english'))

def generate_targetwords(size=300):
    try:
        wordnet.synsets('test')
    except LookupError:
        nltk.download('wordnet')  

    all_words = list(wordnet.words())
    random_target_words = random.sample(all_words, size)
    return random_target_words

def augment_data(dataset, percentages):
    """
    Augments dataset using different techniques with specified percentage allocation for each technique.
    
    Parameters:
    - dataset: the original dataset to augment
    - percentages: a dictionary where keys are augmentation modes (from MODE) and values are the percentages allocated for each mode.
    
    Returns:
    - A list of augmented samples.
    """
    random_aug = RandomAugmenter()
    syn_aug = SynonymAugmenter()
    llm_aug = LLMAugmenter()

    augmented_samples = []
    dataset_size = len(dataset)

    for mode, percentage in percentages.items():
        # Cap the percentage at 500% to avoid excessive augmentation
        if percentage > 5.0:
            raise ValueError(f"Percentage for {mode} exceeds the maximum allowed 500%.")
        
        # Calculate total samples to generate for this mode
        num_samples = int(dataset_size * percentage)
        
        # Repeat the dataset if necessary to reach desired number of samples
        full_repeats = math.ceil(num_samples / dataset_size)
        repeated_dataset = concatenate_datasets([dataset.shuffle(seed=42)] * full_repeats)
        
        # Limit to the exact number of samples needed
        mode_subset = repeated_dataset.select(range(num_samples))
        
        for data in mode_subset:
            words = data["text"].split()
            if len(words) < 2:  # Skip samples with too few words
                continue
            try:
                # Apply the augmentation based on mode
                match mode:
                    case MODE.RANDOM.SUBSTITUTE:
                        stop_words = generate_stopwords()
                        target_words = generate_targetwords(300)
                        augmented_text = random_aug(data["text"], action=Action.SUBSTITUTE, aug_percent=0.3, target_words=target_words, skipwords=stop_words)

                    case MODE.RANDOM.SWAP:
                        augmented_text = random_aug(data["text"], action=Action.SWAP, aug_percent=0.3)

                    case MODE.RANDOM.DELETE:
                        stop_words = generate_stopwords()
                        augmented_text = random_aug(data["text"], action=Action.DELETE, skipwords=stop_words)

                    case MODE.RANDOM.CROP:
                        augmented_text = random_aug(data["text"], action=Action.CROP)

                    case MODE.SYNONYM.WORDNET:
                        augmented_text = syn_aug(data["text"], aug_src='wordnet', aug_p=0.3)

                    case MODE.LLM.PARAPHRASE:
                        augmented_text = llm_aug.paraphrase_with_question(data["text"], max_new_tokens=20)
                    
                    case MODE.LLM.SUMMARIZE:
                        augmented_text = llm_aug.summarize_with_summarizer(data["text"])

                    case _:
                        raise ValueError(f"Invalid mode: {mode}")
                    
                augmented_samples.append({"text": augmented_text, "label": data["label"]})

            except ValueError as e:
                print(f"Skipping augmentation for text due to error: {e}")
    
    return augmented_samples