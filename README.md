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

## 🚀 Instalação e execução local

### 1) Pré-requisitos
- **Python 3.9+** (recomendado 3.10/3.11)
- `git` opcional (para versionamento)

### 2) Clonar ou baixar este repositório
```bash
# via git
git clone https://github.com/<seu-usuario>/<seu-repo>.git
cd <seu-repo>

# ou baixe o ZIP pelo GitHub e extraia numa pasta
```

### 3) (Opcional) Criar e ativar um ambiente virtual
**macOS / Linux**
```bash
python -m venv .venv
source .venv/bin/activate
```
**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 4) Atualizar ferramentas de build (recomendado)
```bash
python -m pip install --upgrade pip setuptools wheel
```

### 5) Instalar dependências
```bash
pip install -r requirements.txt
```
> Se surgir erro envolvendo `statsmodels`/`scipy`, tente:
```bash
# opção 1: somente binários pré-compilados
pip install --only-binary=:all: numpy scipy statsmodels

# opção 2: reinstalar numpy/scipy/statsmodels após atualizar pip
python -m pip install --upgrade pip
pip install --force-reinstall numpy scipy statsmodels
```

### 6) Executar o app
```bash
streamlit run app.py
```
O navegador abrirá em `http://localhost:8501`.

---

## ☁️ Deploy no Streamlit Community Cloud (GitHub)

### Passo a passo
1. **Crie um repositório no GitHub** (ex.: `house-pricing-app`).
2. **Envie** os arquivos `app.py`, `requirements.txt` e `RL_house_pricing.xlsx` para a **raiz** do repositório.
   ```bash
   git init
   git add .
   git commit -m "Primeira versão do app Streamlit"
   git branch -M main
   git remote add origin https://github.com/<seu-usuario>/<seu-repo>.git
   git push -u origin main
   ```
3. Acesse **https://share.streamlit.io** e faça login com o GitHub.
4. Clique em **New app** e selecione:
   - **Repository**: `<seu-usuario>/<seu-repo>`
   - **Branch**: `main` (ou `master`)
   - **Main file path**: `app.py`
5. Clique em **Deploy**. Aguarde a instalação das dependências e a compilação.
6. O app ficará disponível em uma **URL pública** (ex.: `https://<seu-usuario>-<seu-repo>.streamlit.app`).

> **Importante:** Garanta que o `requirements.txt` esteja na **raiz** do repositório. Se aparecer `ModuleNotFoundError: statsmodels`, confirme que `statsmodels` está no `requirements.txt` e faça novo **commit & push**. O Streamlit Cloud recompila automaticamente a cada commit.

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
**`ModuleNotFoundError: No module named 'statsmodels'`**
- Ative o **mesmo** ambiente virtual onde você instalou as libs.
- Rode `pip install -r requirements.txt`.
- Atualize o pip: `python -m pip install --upgrade pip setuptools wheel`.
- Em Apple Silicon (M1/M2), preferir `--only-binary` para `numpy`, `scipy`, `statsmodels`.

**`FileNotFoundError: RL_house_pricing.xlsx`**
- O arquivo precisa estar **na raiz** do projeto (mesmo diretório do `app.py`).
- Se preferir outro caminho, ajuste no código: `DATA_PATH = 'RL_house_pricing.xlsx'`.

**App sobe mas a predição não aparece**
- Clique no botão **“Rodar previsão”** após definir os parâmetros.

---

## 📜 Licença
Defina a licença que preferir (ex.: MIT). Crie um arquivo `LICENSE` se desejar.

---

## ✉️ Contato
Dúvidas ou sugestões? Abra uma **Issue** ou envie um PR.
