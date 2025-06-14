import os
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

    try:
        pytrends.build_payload([termo], timeframe='today 12-m', geo='BR')
        related = pytrends.related_queries()
        dados = related.get(termo)

        if dados and dados.get('top') is not None:
            return jsonify(dados['top'].to_dict(orient='records'))
        else:
            return jsonify([])

    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar dados do Google Trends: {str(e)}"}), 500

# Garante que o app escute na porta que o Railway define
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
