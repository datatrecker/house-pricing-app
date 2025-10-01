
import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm

st.set_page_config(page_title='Prevendo Preço de Imóvel (Regressão Linear)', layout='centered')

st.title('Prevendo Preço de Imóvel')
st.caption('Artefato interativo: regressão linear treinada em **RL_house_pricing.xlsx**')

@st.cache_data(show_spinner=False)
def load_data(path):
    df = pd.read_excel(path)
    df.columns = [c.strip().lower() for c in df.columns]
    # detectar coluna binária yes/no (exempHS/exemploHS)
    bin_col = None
    for c in df.columns:
        if set(df[c].astype(str).str.lower().unique()).issubset({'yes','no'}):
            bin_col = c
            break
    if bin_col is None:
        st.error('Não foi possível identificar a coluna binária (yes/no) — esperada como exempHS/exemploHS.')
        st.stop()
    # conversões
    df['exemphs_num'] = df[bin_col].astype(str).str.lower().map({'yes':1,'no':0})
    for c in ['price_1000s','sqft','beds','bath']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df = df.dropna(subset=['price_1000s','sqft','beds','bath','exemphs_num'])
    return df, bin_col

@st.cache_data(show_spinner=False)
def train_model(df):
    X = df[['sqft','exemphs_num','beds','bath']]
    X = sm.add_constant(X, has_constant='add')
    y = df['price_1000s']
    model = sm.OLS(y, X).fit()
    # métricas no treino
    y_hat = model.predict(X)
    r2 = float(model.rsquared)
    r2_adj = float(model.rsquared_adj)
    rmse = float(np.sqrt(np.mean((y - y_hat)**2)))
    mae = float(np.mean(np.abs(y - y_hat)))
    coefs = pd.DataFrame({'coeficiente': model.params, 'p-valor': model.pvalues})
    return model, {'R² treino': r2, 'R² ajustado': r2_adj, 'RMSE treino (mil)': rmse, 'MAE treino (mil)': mae}, coefs

@st.cache_data(show_spinner=False)
def crossval_metrics(df, n_splits=5, seed=42):
    from sklearn.model_selection import KFold
    from sklearn.metrics import mean_squared_error, mean_absolute_error
    X = df[['sqft','exemphs_num','beds','bath']]
    X = sm.add_constant(X, has_constant='add')
    y = df['price_1000s']
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=seed)
    rmses, maes = [], []
    for tr, te in kf.split(X):
        m = sm.OLS(y.iloc[tr], X.iloc[tr]).fit()
        p = m.predict(X.iloc[te])
        rmses.append(np.sqrt(mean_squared_error(y.iloc[te], p)))
        maes.append(mean_absolute_error(y.iloc[te], p))
    return {'RMSE CV (mil)': float(np.mean(rmses)), 'MAE CV (mil)': float(np.mean(maes))}

# Carregar dados e treinar
DATA_PATH = 'RL_house_pricing.xlsx'
df, bin_col = load_data(DATA_PATH)
model, train_metrics, coefs = train_model(df)
cv_metrics = crossval_metrics(df)

st.subheader('Parâmetros de entrada')
col1, col2 = st.columns(2)
with col1:
    sqft = st.slider('Área (sqft)', int(df['sqft'].min()), int(df['sqft'].max()), int(df['sqft'].median()), step=1)
    beds_opts = sorted(df['beds'].dropna().unique().tolist())
    beds = st.select_slider('Quartos (beds)', options=beds_opts, value=min(beds_opts, key=lambda x: abs(x - np.median(beds_opts))))
with col2:
    bath_opts = sorted(df['bath'].dropna().unique().tolist())
    bath = st.select_slider('Banheiros (bath)', options=bath_opts, value=min(bath_opts, key=lambda x: abs(x - np.median(bath_opts))))
    exemp = st.radio(f"{bin_col} (1=Yes, 0=No)", options=[0,1], index=1, format_func=lambda x: 'yes (1)' if x==1 else 'no (0)')

run = st.button('Rodar previsão')

if run:
    X_new = pd.DataFrame([{'sqft': sqft, 'exemphs_num': int(exemp), 'beds': float(beds), 'bath': float(bath)}])
    X_new = sm.add_constant(X_new, has_constant='add')
    pred = float(model.predict(X_new)[0])
    # Intervalos de predição (95% e ~68%)
    pr95 = model.get_prediction(X_new).summary_frame(alpha=0.05).iloc[0]
    pr68 = model.get_prediction(X_new).summary_frame(alpha=0.32).iloc[0]

    st.success(f"Preço previsto: **US$ {pred*1000:,.0f}**")
    st.write(f"Intervalo de predição 95%: {pr95['obs_ci_lower']*1000:,.0f} — {pr95['obs_ci_upper']*1000:,.0f}")
    st.write(f"Faixa ~68% (±1σ): {pr68['obs_ci_lower']*1000:,.0f} — {pr68['obs_ci_upper']*1000:,.0f}")

st.divider()

st.subheader('Acurácia do modelo')
colA, colB = st.columns(2)
with colA:
    st.metric('R² (treino)', f"{train_metrics['R² treino']:.3f}")
    st.metric('R² ajustado', f"{train_metrics['R² ajustado']:.3f}")
with colB:
    st.metric('RMSE CV (mil)', f"{cv_metrics['RMSE CV (mil)']:.2f}")
    st.metric('MAE CV (mil)', f"{cv_metrics['MAE CV (mil)']:.2f}")

with st.expander('Coeficientes do modelo'):
    st.dataframe(coefs.style.format({'coeficiente':'{:.3f}','p-valor':'{:.3g}'}))

st.caption('Observação: preços no dataset estão em **milhares de dólares** (coluna price_1000s); a saída é multiplicada por 1.000 para exibir em dólares.')

with st.expander('Ver estatísticas do dataset'):
    st.write(df.describe(include='all'))

st.info('O intervalo de predição de 95% reflete a incerteza para **um único** imóvel com esses atributos (erro residual + incerteza dos coeficientes).')
