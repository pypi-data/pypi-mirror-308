import logging

import nltk
from nltk.corpus import wordnet

loggers = logging.getLogger(__name__)

class WordNet:
    """
    A class to interact with the WordNet lexical database for finding synonyms and antonyms.

    :param lang: The language for the WordNet database (default is "eng").
    :type lang: str
    :param is_synonym: A flag to indicate whether to find synonyms (True) or antonyms (False).
    :type is_synonym: bool
    """
    def __init__(self, lang="eng", is_synonym=True):
        """
        Initializes the WordNet class with the specified language and synonym/antonym flag.

        :param lang: The language for the WordNet database (default is "eng").
        :type lang: str
        :param is_synonym: A flag to indicate whether to find synonyms (True) or antonyms (False).
        :type is_synonym: bool
        """
        self.lang = lang
        self.is_synonym = is_synonym
        self.model = self.read()

    def read(self):
        """
        Loads the WordNet corpus, downloading it if necessary.

        :return: The WordNet corpus reader.
        :rtype: nltk.corpus.reader.wordnet.WordNetCorpusReader
        """
        try:
            wordnet.synsets("testing")
            return wordnet
        except LookupError:
            nltk.download("wordnet")
            nltk.download("omw-1.4")
            return wordnet

    def predict(self, word, pos=None):
        """
        Finds synonyms or antonyms for a given word.

        :param word: The word for which to find synonyms or antonyms.
        :type word: str
        :param pos: The part of speech tag (default is None).
        :type pos: str, optional
        :return: A list of synonyms or antonyms for the given word.
        :rtype: list
        """
        results = []
        for synonym in self.model.synsets(word, pos=pos, lang=self.lang):
            for lemma in synonym.lemmas(lang=self.lang):
                if self.is_synonym:
                    results.append(lemma.name())
                else:
                    for antonym in lemma.antonyms():
                        results.append(antonym.name())
        return results

    @classmethod
    def pos_tag(cls, tokens):
        """
        Tags parts of speech for a list of tokens.

        :param tokens: A list of tokens to tag.
        :type tokens: list
        :return: A list of tuples where each tuple contains a token and its part of speech tag.
        :rtype: list
        """
        try:
            results = nltk.pos_tag(tokens)
        except LookupError:
            nltk.download('averaged_perceptron_tagger')
            nltk.download('averaged_perceptron_tagger_eng')
            results = nltk.pos_tag(tokens)

        return results


class PartOfSpeech:
    """
    A class to handle part-of-speech (POS) tagging and mapping between POS tags and their constituents.

    Attributes:
    -----------
    NOUN : str
        Constant for noun POS.
    VERB : str
        Constant for verb POS.
    ADJECTIVE : str
        Constant for adjective POS.
    ADVERB : str
        Constant for adverb POS.
    pos2con : dict
        Dictionary mapping POS tags to their constituent tags.
    con2pos : dict
        Dictionary mapping constituent tags to their POS tags.
    poses : list
        List of all constituent tags.

    Methods:
    --------
    pos2constituent(pos):
        Maps a POS tag to its constituent tags.
    constituent2pos(con):
        Maps a constituent tag to its POS tags.
    get_pos():
        Returns a list of all constituent tags.
    """

    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"

    pos2con = {
        "n": ["NN", "NNS", "NNP", "NNPS"],
        "v": ["VB", "VBD", "VBG", "VBN", "VBZ", "VBP"],
        "a": ["JJ", "JJR", "JJS", "IN"],
        "s": ["JJ", "JJR", "JJS", "IN"],  # Adjective Satellite
        "r": ["RB", "RBR", "RBS"],
    }

    con2pos = {}
    poses = []
    for key, values in pos2con.items():
        poses.extend(values)
        for value in values:
            if value not in con2pos:
                con2pos[value] = []
            con2pos[value].append(key)

    @staticmethod
    def pos2constituent(pos):
        """
        Maps a POS tag to its constituent tags.

        :param pos: The POS tag.
        :type pos: str
        :return: A list of constituent tags for the given POS tag.
        :rtype: list
        """
        return PartOfSpeech.pos2con.get(pos, [])

    @staticmethod
    def constituent2pos(con):
        """
        Maps a constituent tag to its POS tags.

        :param con: The constituent tag.
        :type con: str
        :return: A list of POS tags for the given constituent tag.
        :rtype: list
        """
        return PartOfSpeech.con2pos.get(con, [])

    @staticmethod
    def get_pos():
        """
        Returns a list of all constituent tags.

        :return: A list of all constituent tags.
        :rtype: list
        """
        return PartOfSpeech.poses


def init_ppdb_model(dict_path, force_reload=False):
    """
    Initializes the PPDB model from the given dictionary path.

    :param dict_path: The path to the PPDB dictionary file.
    :type dict_path: str
    :param force_reload: A flag to indicate whether to force reload the model (default is False).
    :type force_reload: bool
    :return: The initialized PPDB model.
    :rtype: nmw.Ppdb
    """
    global PPDB_MODEL

    model_name = os.path.basename(dict_path)
    if model_name in PPDB_MODEL and not force_reload:
        return PPDB_MODEL[model_name]

    model = nmw.Ppdb(dict_path)
    PPDB_MODEL[model_name] = model

    return model


import random

from NLarge.utils.words import WordsUtil


class SynonymAugmenter():
    """
    A class to perform synonym-based data augmentation using the WordNet lexical database.

    Methods:
    --------
    __call__(data, aug_src="wordnet", model_path=None, lang="eng", aug_min=1, aug_max=10, aug_p=0.3, stopwords=None, tokenizer=None, reverse_tokenizer=None, stopwords_regex=None, force_reload=False, verbose=0):
        Performs synonym-based data augmentation on the input data.
    """
    def __init__(self) -> None:
        loggers.info("SynonymAugmenter initialized")

    def __call__(
        self,
        data,
        aug_src="wordnet",
        model_path=None,
        lang="eng",
        aug_min=1,
        aug_max=10,
        aug_p=0.3,
        stopwords=None,
        tokenizer=None,
        reverse_tokenizer=None,
        stopwords_regex=None,
        force_reload=False,
        verbose=0,
    ):
        """
        Performs synonym-based data augmentation on the input data.

        :param data: The input text data to be augmented.
        :type data: str
        :param aug_src: The source for augmentation (default is "wordnet").
        :type aug_src: str
        :param model_path: The path to the model (not used in this implementation).
        :type model_path: str, optional
        :param lang: The language for the WordNet database (default is "eng").
        :type lang: str
        :param aug_min: The minimum number of words to augment (default is 1).
        :type aug_min: int
        :param aug_max: The maximum number of words to augment (default is 10).
        :type aug_max: int
        :param aug_p: The probability of a word being augmented (default is 0.3).
        :type aug_p: float
        :param stopwords: A list of stopwords to exclude from augmentation.
        :type stopwords: list, optional
        :param tokenizer: A function to tokenize the input text (default is str.split).
        :type tokenizer: function, optional
        :param reverse_tokenizer: A function to detokenize the augmented text (default is " ".join).
        :type reverse_tokenizer: function, optional
        :param stopwords_regex: A regex pattern to match stopwords (not used in this implementation).
        :type stopwords_regex: str, optional
        :param force_reload: A flag to indicate whether to force reload the model (default is False).
        :type force_reload: bool
        :param verbose: The verbosity level (default is 0).
        :type verbose: int
        :return: The augmented text.
        :rtype: str
        """
        if not data or not data.strip():
            return data

        model = WordNet(lang=lang) if aug_src == "wordnet" else None
        if model is None:
            raise ValueError("currently, aug_src can only be `wordnet`.")

        change_seq = 0
        tokenizer = tokenizer or str.split
        reverse_tokenizer = reverse_tokenizer or " ".join
        doc = WordsUtil(data, tokenizer(data))

        original_tokens = doc.get_original_tokens()
        pos = model.pos_tag(original_tokens)
        stopwords = stopwords or []

        def skip_aug(token_idxes, tokens):
            results = []
            for token_idx in token_idxes:
                if tokens[token_idx][1] in ["DT"]:
                    continue

                word_poses = PartOfSpeech.constituent2pos(tokens[token_idx][1])
                if aug_src == "ppdb" and not word_poses:
                    continue

                if word_poses and not any(
                    model.predict(tokens[token_idx][0], pos=pos)
                    for pos in word_poses
                ):
                    continue

                results.append(token_idx)

            return results

        def _get_aug_idxes(tokens):
            aug_cnt = (
                min(len(tokens), int(len(tokens) * aug_p)) if aug_p else aug_max
            )
            word_idxes = [i for i in range(len(tokens)) if i not in stopwords]
            word_idxes = skip_aug(word_idxes, tokens)

            return random.sample(word_idxes, aug_cnt) if word_idxes else []

        aug_idxes = _get_aug_idxes(pos)
        if not aug_idxes:
            return data

        for aug_idx in aug_idxes:
            original_token = original_tokens[aug_idx]
            word_poses = PartOfSpeech.constituent2pos(pos[aug_idx][1])
            candidates = sum(
                (
                    model.predict(pos[aug_idx][0], pos=word_pos)
                    for word_pos in word_poses
                ),
                [],
            )

            candidates = [
                c for c in candidates if c.lower() != original_token.lower()
            ]

            if candidates:
                substitute_token = random.choice(candidates).lower()
                if aug_idx == 0:
                    substitute_token = substitute_token.capitalize()

                change_seq += 1
                doc.add_change_log(
                    aug_idx,
                    new_token=substitute_token,
                    action="substitute",
                    change_seq=change_seq,
                )

        return reverse_tokenizer(doc.get_augmented_tokens())
