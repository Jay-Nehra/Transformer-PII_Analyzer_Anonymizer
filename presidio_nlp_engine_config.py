from typing import Tuple
import logging
import spacy
from presidio_analyzer import RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngine, NlpEngineProvider

logger = logging.getLogger("PII-Presidio")


def create_nlp_engine_with_spacy(
    model_path: str,
) -> Tuple[NlpEngine, RecognizerRegistry]:
    """
    Instantiate an NlpEngine with a spaCy model
    :param model_path: spaCy model path.
    """
    registry = RecognizerRegistry()
    registry.load_predefined_recognizers()

    if not spacy.util.is_package(model_path):
        spacy.cli.download(model_path)

    nlp_configuration = {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "en", "model_name": model_path}],
    }

    nlp_engine = NlpEngineProvider(nlp_configuration=nlp_configuration).create_engine()

    return nlp_engine, registry


def create_nlp_engine_with_transformers(
    model_path: str,
) -> Tuple[NlpEngine, RecognizerRegistry]:
    """
    Instantiate an NlpEngine with a TransformersRecognizer and a small spaCy model.
    The TransformersRecognizer would return results from Transformers models, the spaCy model
    would return NlpArtifacts such as POS and lemmas.
    :param model_path: HuggingFace model path.
    """

    from transformers_rec import (
        STANFORD_COFIGURATION,
        BERT_DEID_CONFIGURATION,
        TransformersRecognizer,
    )

    registry = RecognizerRegistry()
    registry.load_predefined_recognizers()

    if not spacy.util.is_package("en_core_web_sm"):
        spacy.cli.download("en_core_web_sm")
    # Using a small spaCy model + a HF NER model
    transformers_recognizer = TransformersRecognizer(model_path=model_path)

    if model_path == "StanfordAIMI/stanford-deidentifier-base":
        transformers_recognizer.load_transformer(**STANFORD_COFIGURATION)
    elif model_path == "obi/deid_roberta_i2b2":
        transformers_recognizer.load_transformer(**BERT_DEID_CONFIGURATION)
    else:
        print(f"Warning: Model has no configuration, loading default.")
        transformers_recognizer.load_transformer(**BERT_DEID_CONFIGURATION)

    nlp_configuration = {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
    }

    registry.add_recognizer(transformers_recognizer)
    registry.remove_recognizer("SpacyRecognizer")

    nlp_engine = NlpEngineProvider(nlp_configuration=nlp_configuration).create_engine()

    return nlp_engine, registry
