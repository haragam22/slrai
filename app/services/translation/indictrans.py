"""IndicTrans2 model wrapper for Hindi → English translation.

Batched, script-filtered translation. text_original is never touched —
translation is additive only (text_translated column).
"""
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from app.config import settings

_tokenizer = None
_model = None
TRANSLATION_BATCH_SIZE = 10  # per forward pass — max 10 CPU, 20 GPU
HINDI_SCRIPT_RANGE = ("ऀ", "ॿ")  # Devanagari Unicode block

HINDI_LEGAL_MAP = {
    "जबरन कब्जा": "forcible possession",
    "कब्जा नोटिस": "possession notice",
    "नीलामी": "auction",
    "माँग नोटिस": "demand notice",
    "बकाया राशि": "outstanding amount",
    "बंधक": "mortgage",
    "गारंटर": "guarantor",
    "पुनर्गठन": "restructuring",
    "आपत्ति": "objection",
    "किरायेदार": "tenant",
    "अप्रचलित आस्ति": "non-performing asset",
    "प्रतिभूति": "security interest",
    "देनदार": "debtor",
    "वसूली": "recovery",
    "प्रतिनिधित्व": "representation",
    "नीलाम": "auction sale",
}


def _load_model():
    global _tokenizer, _model
    if _tokenizer is None:
        name = settings.translation_model
        _tokenizer = AutoTokenizer.from_pretrained(name, trust_remote_code=True)
        _model = AutoModelForSeq2SeqLM.from_pretrained(name, trust_remote_code=True)
        _model = _model.to(settings.translation_device).eval()


def needs_translation(text: str, threshold: float = 0.05) -> bool:
    """True if Devanagari characters exceed threshold fraction of text."""
    if not text or len(text) < 5:
        return False
    hindi = sum(1 for c in text if HINDI_SCRIPT_RANGE[0] <= c <= HINDI_SCRIPT_RANGE[1])
    return (hindi / len(text)) > threshold


def preprocess_hindi(text: str) -> str:
    for hindi, english in HINDI_LEGAL_MAP.items():
        text = text.replace(hindi, english)
    return text


def translate_batch(texts: list[str]) -> list[str]:
    """Single batched forward pass through IndicTrans2. Never call one-at-a-time."""
    _load_model()
    inputs = _tokenizer(
        texts,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512,
    ).to(settings.translation_device)

    with torch.no_grad():
        outputs = _model.generate(
            **inputs, max_length=512, num_beams=4, early_stopping=True
        )
    return [_tokenizer.decode(o, skip_special_tokens=True) for o in outputs]


def translate_paragraphs(paragraphs: list[dict]) -> list[dict]:
    """
    Entry point for task_translate_hindi_paragraphs in Chain A.
    paragraphs: list of {para_id, text_original, language}
    Returns same list with text_translated populated for Hindi paragraphs.
    text_original is NEVER modified. English paragraphs: text_translated = None.
    """
    to_translate = [
        (i, p) for i, p in enumerate(paragraphs)
        if needs_translation(p["text_original"])
    ]
    if not to_translate:
        return paragraphs

    preprocessed_texts = [preprocess_hindi(p["text_original"]) for _, p in to_translate]

    translations = []
    for start in range(0, len(preprocessed_texts), TRANSLATION_BATCH_SIZE):
        batch = preprocessed_texts[start:start + TRANSLATION_BATCH_SIZE]
        translations.extend(translate_batch(batch))

    for (orig_idx, _), translation in zip(to_translate, translations):
        paragraphs[orig_idx]["text_translated"] = translation

    return paragraphs
