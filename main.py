import os
import traceback
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

        # Proteção contra erro interno da API do Google Trends
        try:
            related = pytrends.related_queries()
        except Exception as e:
            print("Erro interno em pytrends.related_queries():")
            traceback.print_exc()
            return jsonify([])

        if not related or termo not in related:
            return jsonify([])

        termo_data = related[termo]
        if not termo_data or 'top' not in termo_data:
            return jsonify([])

        top_df = termo_data['top']
        if top_df is None or top_df.empty:
            return jsonify([])

        return jsonify(top_df.to_dict(orient='records'))

    except Exception as e:
        print("Erro inesperado:")
        traceback.print_exc()
        return jsonify({"erro": f"Erro ao buscar dados do Google Trends: {str(e)}"}), 500

# Usa a porta do Railway
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
