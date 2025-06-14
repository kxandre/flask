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
        
        if not related or termo not in related:
            return jsonify([])

        termo_data = related[termo]
        if not termo_data or not isinstance(termo_data, dict):
            return jsonify([])

        top_df = termo_data.get('top')
        if top_df is None or top_df.empty:
            return jsonify([])
