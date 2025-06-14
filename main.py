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
        return jsonify({"erro": "Parâmetro 'termo' é obrigatório"}), 400

    try:
        pytrends.build_payload([termo], cat=0, timeframe='today 12-m', geo='BR', gprop='')
        dados = pytrends.interest_over_time()

        if dados.empty:
            return jsonify({"erro": f"Sem dados disponíveis para o termo '{termo}'"}), 404

        # Transforma o resultado em lista de dicionários
        resultados = dados.reset_index()[['date', termo]].rename(columns={termo: 'valor'})
        retorno = resultados.to_dict(orient='records')

        return jsonify(retorno)

    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar dados do Google Trends: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
