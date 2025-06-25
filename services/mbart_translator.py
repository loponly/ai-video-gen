import os
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

class MBartTranslator:
    def __init__(self, model_name="facebook/mbart-large-50-many-to-many-mmt",cache_dir = "/Users/enkhbat_1/projects/ai-video-ge/cache-models/"):
        """Initialize the mBART-50 model and tokenizer."""
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        self.cache_dir = cache_dir
        self.model = MBartForConditionalGeneration.from_pretrained(model_name, cache_dir=cache_dir)
        self.tokenizer = MBart50TokenizerFast.from_pretrained(model_name, cache_dir=cache_dir)

    def translate(self, text, src_lang, tgt_lang):
        """Translate text from src_lang to tgt_lang using mBART-50."""
        self.tokenizer.src_lang = src_lang
        encoded = self.tokenizer(text, return_tensors="pt")
        generated_tokens = self.model.generate(
            **encoded, forced_bos_token_id=self.tokenizer.lang_code_to_id[tgt_lang]
        )
        return self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]


if __name__ == "__main__":

    # Usage example:
    translator = MBartTranslator()
    translation_en_to_mn = translator.translate("The UN chief says there is no military solution in Syria.", "en_XX", "mn_MN")

    print("English ➔ Mongolian:", translation_en_to_mn)