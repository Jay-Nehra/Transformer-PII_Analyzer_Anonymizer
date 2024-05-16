from typing import List, Optional, Tuple
import logging
from presidio_analyzer import AnalyzerEngine, RecognizerResult, RecognizerRegistry, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import NlpEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

from presidio_nlp_engine_config import create_nlp_engine_with_spacy, create_nlp_engine_with_transformers

logger = logging.getLogger("Athena Anonymization")

def nlp_engine_and_registry(model_family: str, model_path: str) -> Tuple[NlpEngine, RecognizerRegistry]:
    if "spaCy" in model_family:
        return create_nlp_engine_with_spacy(model_path)
    elif "HuggingFace" in model_family:
        return create_nlp_engine_with_transformers(model_path)
    else:
        raise ValueError(f"Model family {model_family} not supported")

def analyzer_engine(model_family: str, model_path: str) -> AnalyzerEngine:
    nlp_engine, registry = nlp_engine_and_registry(model_family, model_path)
    return AnalyzerEngine(nlp_engine=nlp_engine, registry=registry)

def anonymizer_engine() -> AnonymizerEngine:
    return AnonymizerEngine()

def analyze(model_family: str, model_path: str, language='en', **kwargs):
    entities = kwargs.get("entities", None)
    if not entities or "All" in entities:
        kwargs["entities"] = None
    ad_hoc_recognizers = []
    if "deny_list" in kwargs:
        ad_hoc_recognizers.append(create_ad_hoc_deny_list_recognizer(kwargs.pop("deny_list", [])))
    if "regex_params" in kwargs:
        ad_hoc_recognizers.append(create_ad_hoc_regex_recognizer(*kwargs.pop("regex_params", [])))
    if ad_hoc_recognizers:
        kwargs["ad_hoc_recognizers"] = ad_hoc_recognizers
    return analyzer_engine(model_family, model_path).analyze(language=language, **kwargs)

def anonymize(text: str, operator: str, analyze_results: List[RecognizerResult], mask_char: Optional[str] = None, number_of_chars: Optional[int] = None, encrypt_key: Optional[str] = None):
    operator_config = {}
    if operator == "mask":
        operator_config = {"type": "mask", "masking_char": mask_char or "*", "chars_to_mask": number_of_chars or 0, "from_end": False}
    elif operator == "encrypt":
        operator_config = {"key": encrypt_key}
    elif operator == "highlight":
        operator_config = {"lambda": lambda x: x}  # How to do it?
    operator = "custom" if operator in ["highlight", "synthesize"] else operator
    anonymization_results = anonymizer_engine().anonymize(text, analyze_results, operators={"DEFAULT": OperatorConfig(operator, operator_config)})
    return anonymization_results

def create_ad_hoc_deny_list_recognizer(deny_list: List[str]) -> Optional[PatternRecognizer]:
    if not deny_list:
        return None
    return PatternRecognizer(supported_entity="GENERIC_PII", deny_list=deny_list)

def create_ad_hoc_regex_recognizer(regex: str, entity_type: str, score: float, context: Optional[List[str]] = None) -> Optional[PatternRecognizer]:
    if not regex:
        return None
    pattern = Pattern(name="Regex pattern", regex=regex, score=score)
    return PatternRecognizer(supported_entity=entity_type, patterns=[pattern], context=context)
