from deeppavlov import build_model, configs


class NER:
    def __init__(self):
        self.model = None

    def get_name(self, text: str) -> str:
        if self.model is None:
            self.model = build_model(configs.ner.ner_rus, download=False)

        ner_result = self.model([text])
        name_tokens = []
        for token, token_type in zip(ner_result[0][0], ner_result[1][0]):
            if token_type in ['B-PER', 'I-PER']:
                name_tokens.append(token)
            elif len(name_tokens) > 0:
                break

        return ' '.join(name_tokens[-3:])
