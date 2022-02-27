import numpy as np
from flask import Flask, jsonify, request

app = Flask(__name__)

SAMPLE_LEN = 1000


def d(x):
    return x[1:] - x[:-1]


def I(dx):
    x = np.empty(SAMPLE_LEN, dx.dtype)
    x[0] = 0
    x[1:] = dx.cumsum()
    return x


@app.route('/brownian')
def brownian():
    stop_time = float(request.args.get('stop_time'))
    drift = float(request.args.get('drift'))
    std = float(request.args.get('std'))

    t = np.linspace(0, stop_time, SAMPLE_LEN)
    dt = d(t)
    dx = np.random.normal(drift * dt, std * np.sqrt(dt))
    x = I(dx)
    return jsonify({'time': list(t), 'process': list(x)})


@app.route('/ornstein_uhlenbeck')
def ornstein_uhlenbeck():
    stop_time = float(request.args.get('stop_time'))
    std = float(request.args.get('std'))
    reverting = float(request.args.get('reverting'))

    t = np.linspace(0, stop_time, SAMPLE_LEN)
    dt = d(t)
    random_part = np.random.normal(scale=std * np.sqrt((1 - np.exp(-2 * reverting * dt)) / 2 / reverting))
    x = np.empty_like(t)
    x[0] = np.random.normal(scale=std / np.sqrt(2 * reverting))
    for i in range(0, SAMPLE_LEN - 1):
        x[i + 1] = x[i] * np.exp(-reverting * dt[i]) + random_part[i]
    return jsonify({'time': list(t), 'process': list(x)})


@app.route('/cauchy')
def cauchy():
    stop_time = float(request.args.get('stop_time'))
    drift = float(request.args.get('drift'))
    noise = float(request.args.get('noise'))

    t = np.linspace(0, stop_time, SAMPLE_LEN)
    dt = d(t)
    dx = np.random.standard_cauchy(SAMPLE_LEN - 1) * noise * dt + drift * dt
    x = I(dx)
    return jsonify({'time': list(t), 'process': list(x)})


@app.route('/poisson')
def poisson():
    stop_time = float(request.args.get('stop_time'))
    intensity = float(request.args.get('intensity'))

    t = np.linspace(0, stop_time, SAMPLE_LEN)
    dt = d(t)
    dx = np.random.poisson(intensity * dt)
    x = I(dx).astype(float)
    return jsonify({'time': list(t), 'process': list(x)})


@app.route('/stable')
def stable():
    stop_time = float(request.args.get('stop_time'))
    stability = float(request.args.get('stability'))
    drift = float(request.args.get('drift'))
    positive_noise = float(request.args.get('positive_noise'))
    negative_noise = float(request.args.get('negative_noise'))

    t = np.linspace(0, stop_time, SAMPLE_LEN)
    dt = d(t)
    dx = (dt / np.random.rand(SAMPLE_LEN - 1)) ** (1 / stability) * positive_noise - \
         (dt / np.random.rand(SAMPLE_LEN - 1)) ** (1 / stability) * negative_noise + \
         drift * dt
    if stability > 1:
        dx += stability / (stability - 1) * (negative_noise - positive_noise) * dt ** (1 / stability)
    x = I(dx)
    return jsonify({'time': list(t), 'process': list(x)})


if __name__ == '__main__':
    app.run(debug=True)
