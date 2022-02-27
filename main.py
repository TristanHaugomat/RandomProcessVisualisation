import decimal
import subprocess
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import streamlit as st

URL = 'http://127.0.0.1:5000/'


@st.cache
def run_api():
    subprocess.Popen([sys.executable, 'app.py'])


@st.cache
def decibel_scale(m, M):
    return [decimal.Decimal(10) ** (n // 10) * round(decimal.Decimal(10 ** (n % 10 / 10)), 2)
            for n in range(round(10 * np.log10(m)), round(10 * np.log10(M)) + 1)]


run_api()
params = {}

process_name = st.sidebar.selectbox('', (
    'Brownian motion', 'Cauchy process', 'Poisson process'
))
st.sidebar.button('Reload')

params['stop_time'] = st.sidebar.select_slider('Maximum time', list(decibel_scale(.1, 10)), 1)

if process_name == 'Brownian motion':
    params['drift'] = st.sidebar.slider('Drift', -10., 10., 0., .1)
    params['std'] = st.sidebar.slider('Standard deviation', 0., 5., 1., .1)
    end_point = 'brownian'

elif process_name == 'Cauchy process':
    params['drift'] = st.sidebar.slider('Drift', -10., 10., 0., .1)
    params['noise'] = st.sidebar.slider('Noise level', 0., 5., 1., .1)
    end_point = 'cauchy'

elif process_name == 'Poisson process':
    params['intensity'] = st.sidebar.slider('Intensity', 0., 5., 1., .1)
    end_point = 'poisson'

df = pd.DataFrame(requests.get(f'{URL}/{end_point}', params=params).json())

fig, ax = plt.subplots()
ax.plot(df['time'], df['process'])
st.pyplot(fig)
