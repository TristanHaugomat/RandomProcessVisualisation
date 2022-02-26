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
    dx = np.random.normal(drift * dt, np.sqrt(std * dt))
    x = I(dx)
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


if __name__ == '__main__':
    app.run(debug=True)
