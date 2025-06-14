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
        # Solicita dados ao Google Trends
        pytrends.build_payload([termo], timeframe='today 12-m', geo='BR')
        related = pytrends.related_queries()

        # Verifica se há dados relacionados para o termo
        termo_data = related.get(termo)
        if not termo_data or 'top' not in termo_data:
            return jsonify([])

        top = termo_data['top']
        if top is None or top.empty:
            return jsonify([])

        # Converte para JSON e retorna
        return jsonify(top.to_dict(orient='records'))

    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar dados do Google Trends: {str(e)}"}), 500

# Executa o app na porta definida pelo Railway
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
