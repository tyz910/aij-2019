import sys
from deeppavlov import build_model, configs

CONFIG_PATH = configs.spelling_correction.levenshtein_corrector_ru
model = build_model(CONFIG_PATH, download=True)
