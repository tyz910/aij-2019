from flask import Flask, request, jsonify
from lib.util.bert import Bert
from lib.util.sentence_encoder import SentenceEncoder
from lib.solver import SberbankSolver
from lib.ololosh import OloloshAI
from lib.sberbank.utils import rus_tok


bert = Bert()
bert.eval('warmup')

sentence_encoder = SentenceEncoder()
sentence_encoder.encode(['warmup'])

sberbank_solver = SberbankSolver()

ai = OloloshAI(bert=bert, sentence_encoder=sentence_encoder, sberbank_solver=sberbank_solver)
app = Flask(__name__)


@app.route('/ready')
def http_ready():
    return 'OK'


@app.route('/take_exam', methods=['POST'])
def http_take_exam():
    request_data = request.get_json()
    tasks = request_data['tasks']
    answers = ai.take_exam(tasks)

    return jsonify({
        'answers': answers
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
