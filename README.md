# Prevendo Preço de Imóvel — Regressão Linear (Streamlit)

Aplicação **Streamlit** que treina uma **Regressão Linear (OLS)** a partir do arquivo `RL_house_pricing.xlsx` e permite **prever o preço de um imóvel** com base em:

- `sqft` (área)
- `beds` (quartos)
- `bath` (banheiros)
- `exempHS` (binária yes/no → convertida para 1/0 automaticamente)

A interface limita os controles às **faixas/valores observados no conjunto de treino**. O app exibe:

- **Preço previsto** (em dólares),
- **Intervalo de predição 95%** e **~68% (±1σ)**,
- **Acurácia**: R² (treino), R² ajustado e **validação cruzada (5-fold)** com RMSE/MAE.

> **Observação:** a coluna alvo `price_1000s` está em **milhares de dólares**; o app multiplica por 1.000 ao exibir.

---

## 📁 Estrutura do repositório
```
.
├── app.py                   # Código do app Streamlit
├── requirements.txt         # Dependências do projeto
└── RL_house_pricing.xlsx    # Dataset (necessário na raiz do projeto)
```

---

## ☁️ Deploy no Streamlit Community Cloud

   O app está disponível no **[Streamlit](https://house-pricing-predictions.streamlit.app/)**.

---

## 🧩 Como usar
1. Ajuste os controles de **Área (sqft)**, **Quartos (beds)**, **Banheiros (bath)** e **exempHS** (Yes/No).
2. Clique em **“Rodar previsão”**.
3. Veja o **Preço previsto** e os **intervalos 68% e 95%**.
4. Acompanhe a **Acurácia** (R², RMSE/MAE de validação cruzada) na seção dedicada.

Os valores dos controles são limitados aos **valores presentes no treino**, evitando extrapolações extremas.

---

## ⚙️ Tecnologias
- [Streamlit](https://streamlit.io) — UI reativa em Python
- [pandas](https://pandas.pydata.org) — manipulação de dados
- [NumPy](https://numpy.org)
- [Statsmodels](https://www.statsmodels.org) — OLS e intervalos de predição
- [scikit-learn](https://scikit-learn.org) — Validação cruzada, métricas
- [openpyxl](https://openpyxl.readthedocs.io) — leitura de `.xlsx`

---

## 🧰 Solução de problemas (FAQ)
**App sobe mas a predição não aparece**
- Clique no botão **“Rodar previsão”** após definir os parâmetros.
