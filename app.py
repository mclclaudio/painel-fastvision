from flask import Flask, render_template
import requests
import pandas as pd

app = Flask(__name__)

# === ENDPOINT JSON DO FASTVISION ===
URL = "https://asapprd.seniorcloud.com.br/siltwms/fastvision.json?id=panel1716836573485431&uniq_param=1761241854143"

# === HEADERS E COOKIES ===
HEADERS = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
    "referer": "https://asapprd.seniorcloud.com.br/siltwms/painel/index.html?panel1716836573485431"
}

COOKIES = {
    "JSESSIONID": "65149B3B8F9B6FDE3E900B725DEDBC9D",
    "ArmazemLogin": "10"
}

@app.route('/')
def painel():
    try:
        # Faz a requisição
        resp = requests.get(URL, headers=HEADERS, cookies=COOKIES, timeout=10)
        resp.raise_for_status()

        # Converte o JSON em estrutura Python
        data = resp.json()

        # Caso o retorno seja uma lista, cria um DataFrame direto
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            # Se for dicionário único, cria um DataFrame com 1 linha
            df = pd.DataFrame([data])

        # Normaliza os nomes de coluna para manter consistência
        df.columns = [c.upper() for c in df.columns]

        # Ajusta colunas esperadas
        if "TITULO" not in df.columns:
            df["TITULO"] = df.get("NOME", "Sem título")
        if "VALOR" not in df.columns:
            df["VALOR"] = 0
        if "DESCRICAO" not in df.columns:
            df["DESCRICAO"] = "Atualizado via JSON"

    except Exception as e:
        df = pd.DataFrame([{
            "TITULO": "ERRO AO CARREGAR DADOS",
            "VALOR": 0,
            "DESCRICAO": str(e)
        }])

    return render_template("painel.html", df=df)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
