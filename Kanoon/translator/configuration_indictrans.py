from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

def load_translation_pipelines():
    # Correct model names
    en_hi_model_id = "ai4bharat/indictrans2-en-indic"
    hi_en_model_id = "ai4bharat/indictrans2-indic-en"

    en_hi_pipeline = pipeline(
        "translation",
        model=AutoModelForSeq2SeqLM.from_pretrained(en_hi_model_id),
        tokenizer=AutoTokenizer.from_pretrained(en_hi_model_id),
        src_lang="en",
        tgt_lang="hi"
    )

    hi_en_pipeline = pipeline(
        "translation",
        model=AutoModelForSeq2SeqLM.from_pretrained(hi_en_model_id),
        tokenizer=AutoTokenizer.from_pretrained(hi_en_model_id),
        src_lang="hi",
        tgt_lang="en"
    )

    return en_hi_pipeline, hi_en_pipeline
