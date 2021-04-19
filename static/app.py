import numpy as np
from math import sqrt
from flask import Flask, Response, request, jsonify

app = Flask(__name__)


def square_root_alghoritm(A, B):
    # Если матрица не равна транспонированной
    # - то она не симметрична - алгоритм для
    # нее работать не будет,возвращаем None
    if not (np.allclose(A, A.T, 1e-08)):
        return None
    n = len(A[0])

    # A = T' * T
    T = np.zeros((n, n))
    Y = np.zeros((1, n))
    # result
    X = np.zeros((1, n))
    d = np.zeros((1, n))

    T[0][0] = sqrt(abs(A[0, 0]))
    d[0, 0] = np.sign(A[0, 0])
    # Прямой ход
    for i in range(n):
        for j in range(n):
            # Для первой строки
            if i == 0 and j != 0:
                T[i, j] = A[i, j] / (T[0, 0] * d[0, 0])
            # для диагонали
            elif i == j:
                difference = A[i][i] - sum((T[k, i] ** 2) * d[0, k] for k in range(i))
                d[0, i] = np.sign(difference)
                T[i, i] = sqrt(abs(difference))
            # Для верхнего треугольника
            elif i < j:
                T[i, j] = (A[i][j] - sum(T[k, i] * T[k, j] * d[0, k] for k in range(i))) / (T[i, i] * d[0, i])

    # Обратный ход
    Y[0, 0] = B[0] / (T[0, 0] * d[0, 0])
    for i in range(1, n):
        Y[0, i] = (B[i] - sum(T[k, i] * Y[0, k] * d[0, k] for k in range(i))) / (T[i, i] * d[0, i])
    X[0, -1] = Y[0, -1] / T[-1, -1]
    for i in reversed(range(n - 1)):
        X[0, i] = (Y[0, i] - sum(T[i, k] * X[0, k] for k in range(i + 1, n))) / T[i, i]
    return [X[0],Y[0],T,d[0]]


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/solve", methods=['POST'])
def solve():
    system = request.json
    matrix = np.asarray(system['matrix'], dtype=float)
    vector = np.asarray(system['vector'], dtype=float)
    if np.linalg.det(matrix) == 0:
        return Response("{\"message\":\" Матрица не должна иметь нулевой определитель!\"}", status=400)
    try:
        result = square_root_alghoritm(matrix, vector)
    except Exception as e:
        return Response("{\"message\":\" " + str(e) + "\"}", status=400)
    if result is None:
        return Response("{\"message\":\" Матрица не является симметричной!\"}", status=400)
    return jsonify({
        "result": list(result[0]),
        "y": list(result[1]),
        "d": list(result[3])
         })


if __name__ == "__main__":
    app.run(debug=True)
