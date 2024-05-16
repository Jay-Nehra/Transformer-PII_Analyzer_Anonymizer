## Analyzer Testing 

### Dummy TEXT 

```text
{
  "text": "John Doe lives in New York and his email is john.doe@example.com.",
  "model_family": "HuggingFace",
  "model_path": "StanfordAIMI/stanford-deidentifier-base",
  "entities": null,
  "threshold": 0.5
}
```

> curl -X 'POST' \
  'http://127.0.0.1:8000/analyze' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "John Doe lives in New York and his email is john.doe@example.com.",
  "model_family": "HuggingFace",
  "model_path": "StanfordAIMI/stanford-deidentifier-base",
  "entities": null,
  "threshold": 0.5
}
'

### Output
```JSON
[
  {
    "entity_type": "PERSON",
    "start": 0,
    "end": 8,
    "score": 1,
    "analysis_explanation": null,
    "recognition_metadata": {
      "recognizer_identifier": "Transformers model StanfordAIMI/stanford-deidentifier-base_130330195868352",
      "recognizer_name": "Transformers model StanfordAIMI/stanford-deidentifier-base"
    }
  },
  {
    "entity_type": "LOCATION",
    "start": 18,
    "end": 26,
    "score": 1,
    "analysis_explanation": null,
    "recognition_metadata": {
      "recognizer_identifier": "Transformers model StanfordAIMI/stanford-deidentifier-base_130330195868352",
      "recognizer_name": "Transformers model StanfordAIMI/stanford-deidentifier-base"
    }
  },
  {
    "entity_type": "EMAIL_ADDRESS",
    "start": 44,
    "end": 64,
    "score": 1,
    "analysis_explanation": null,
    "recognition_metadata": {
      "recognizer_name": "EmailRecognizer",
      "recognizer_identifier": "EmailRecognizer_130329497672320"
    }
  },
  {
    "entity_type": "PERSON",
    "start": 44,
    "end": 52,
    "score": 1,
    "analysis_explanation": null,
    "recognition_metadata": {
      "recognizer_identifier": "Transformers model StanfordAIMI/stanford-deidentifier-base_130330195868352",
      "recognizer_name": "Transformers model StanfordAIMI/stanford-deidentifier-base"
    }
  },
  {
    "entity_type": "ORGANIZATION",
    "start": 53,
    "end": 60,
    "score": 0.9900000095367432,
    "analysis_explanation": null,
    "recognition_metadata": {
      "recognizer_identifier": "Transformers model StanfordAIMI/stanford-deidentifier-base_130330195868352",
      "recognizer_name": "Transformers model StanfordAIMI/stanford-deidentifier-base"
    }
  },
  {
    "entity_type": "ORGANIZATION",
    "start": 61,
    "end": 64,
    "score": 0.8399999737739563,
    "analysis_explanation": null,
    "recognition_metadata": {
      "recognizer_identifier": "Transformers model StanfordAIMI/stanford-deidentifier-base_130330195868352",
      "recognizer_name": "Transformers model StanfordAIMI/stanford-deidentifier-base"
    }
  },
  {
    "entity_type": "URL",
    "start": 44,
    "end": 51,
    "score": 0.5,
    "analysis_explanation": null,
    "recognition_metadata": {
      "recognizer_name": "UrlRecognizer",
      "recognizer_identifier": "UrlRecognizer_130329497672560"
    }
  },
  {
    "entity_type": "URL",
    "start": 53,
    "end": 64,
    "score": 0.5,
    "analysis_explanation": null,
    "recognition_metadata": {
      "recognizer_name": "UrlRecognizer",
      "recognizer_identifier": "UrlRecognizer_130329497672560"
    }
  }
]
```


## Anonymize Endpoint

### Testing Text

```text

{
  "text": "John Doe's email address is john.doe@example.com, and he lives at 1234 Main St, Springfield, IL. His phone number is 312-555-1234. John's date of birth is 01/02/1980, and his Social Security Number is 123-45-6789. He works at Acme Corp. His wife's name is Jane Doe and his child's name is Jimmy Doe.",
  "model_family": "HuggingFace",
  "model_path": "StanfordAIMI/stanford-deidentifier-base",
  "operator": "mask",
  "mask_char": "*",
  "number_of_chars": 5,
  "encrypt_key": "",
  "entities": null,
  "threshold": 0.5
}

```

> curl -X 'POST' \
  'http://127.0.0.1:8000/anonymize' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "John Doe'\''s email address is john.doe@example.com, and he lives at 1234 Main St, Springfield, IL. His phone number is 312-555-1234. John'\''s date of birth is 01/02/1980, and his Social Security Number is 123-45-6789. He works at Acme Corp. His wife'\''s name is Jane Doe and his child'\''s name is Jimmy Doe.",
  "model_family": "HuggingFace",
  "model_path": "StanfordAIMI/stanford-deidentifier-base",
  "operator": "mask",
  "mask_char": "*",
  "number_of_chars": 15,
  "encrypt_key": "",
  "entities": null,
  "threshold": 0.5
}
'

### Output

```JSON

{
  "text": "********'s email address is ***************e.com, and he lives at ***************pringfield, IL. His phone number is ************. ****'s date of birth is **********, and his Social Security Number is ***********. He works at *********. His wife's name is ******** and his child's name is *********."
}
```