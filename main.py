@app.route('/trends', methods=['GET'])
def get_trends():
    termo = request.args.get('termo')
    if not termo:
        return jsonify({"erro": "Parametro 'termo' é obrigatório"}), 400

    try:
        pytrends.build_payload([termo], timeframe='today 12-m', geo='BR')
        related = pytrends.related_queries()
        resultado = related.get(termo, {}).get('top')

        if resultado is not None:
            return jsonify(resultado.to_dict(orient='records'))
        else:
            return jsonify([])

    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar dados: {str(e)}"}), 500
