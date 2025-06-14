from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)
pytrends = TrendReq(hl='pt-BR', tz=360)

@app.route('/')
def home():
    return "API Pytrends no ar! 🧠"

@app.route('/trends', methods=['GET'])
def get_trends():
    termo = request.args.get('termo')
    if not termo:
        return jsonify({"erro": "Parametro 'termo' é obrigatório"}), 400

    pytrends.build_payload([termo], timeframe='today 12-m', geo='BR')
    related = pytrends.related_queries()
    resultado = related.get(termo, {}).get('top', {})

    if resultado is not None:
        return jsonify(resultado.to_dict(orient='records'))
    else:
        return jsonify([])
