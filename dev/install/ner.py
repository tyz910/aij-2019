from deeppavlov import build_model, configs

CONFIG_PATH = configs.ner.ner_rus
model = build_model(CONFIG_PATH, download=True)
