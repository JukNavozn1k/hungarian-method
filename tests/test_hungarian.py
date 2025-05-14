# tests/test_hungarian.py

import random
import math
import pytest
from scipy.optimize import linear_sum_assignment

from hungarian import hungarian


def reference_assignment(cost, maximize: bool = False):
    """Сравнение с scipy без numpy: scipy принимает array-like."""
    mat = [row[:] for row in cost]
    if maximize:
        # scipy решает только минимум
        M = max(max(row) for row in mat)
        mat = [[M - val for val in row] for row in mat]
    row_ind, col_ind = linear_sum_assignment(mat)
    total = sum(cost[i][j] for i, j in zip(row_ind, col_ind))
    return list(col_ind), total


@pytest.mark.parametrize("n", [1, 2, 5, 10])
@pytest.mark.parametrize("maximize", [False, True])
def test_random(n, maximize):
    # Генерируем случайную квадратную матрицу стоимостей
    cost = [[random.uniform(0, 100) for _ in range(n)] for _ in range(n)]
    assign, total = hungarian(cost, maximize=maximize)
    ref_assign, ref_total = reference_assignment(cost, maximize=maximize)
    # Проверяем корректность назначения
    assert sorted(assign) == list(range(n)), "Некорректное соответствие строк и столбцов"
    # Сравниваем стоимость с допуском
    assert pytest.approx(total, rel=1e-7, abs=1e-7) == ref_total


def test_known_example_min():
    cost = [
        [4, 1, 3],
        [2, 0, 5],
        [3, 2, 2]
    ]
    assign, total = hungarian(cost, maximize=False)
    assert assign == [1, 0, 2]
    assert total == 5


def test_known_example_max():
    cost = [
        [4, 1, 3],
        [2, 0, 5],
        [3, 2, 2]
    ]
    assign, total = hungarian(cost, maximize=True)
    _, ref_total = reference_assignment(cost, maximize=True)
    assert pytest.approx(total, rel=1e-7) == ref_total

@pytest.mark.parametrize("n", [1, 2, 5, 10])
@pytest.mark.parametrize("maximize", [False, True])
def test_random(n, maximize):
    # Генерируем случайную квадратную матрицу стоимостей
    cost = [[random.uniform(0, 100) for _ in range(n)] for _ in range(n)]
    assign, total = hungarian(cost, maximize=maximize)
    ref_assign, ref_total = reference_assignment(cost, maximize=maximize)
    # Проверяем совпадение назначений и итоговой стоимости
    assert sorted(assign) == list(range(n)), "Некорректное соответствие строк и столбцов"
    # Сравниваем стоимость с небольшим допуском
    assert pytest.approx(total, rel=1e-7, abs=1e-7) == ref_total


def test_known_example_min():
    cost = [
        [4, 1, 3],
        [2, 0, 5],
        [3, 2, 2]
    ]
    assign, total = hungarian(cost, maximize=False)
    # Оптимальное назначение: 0→1, 1→0, 2→2, стоимость = 1+2+2 = 5
    assert assign == [1, 0, 2]
    assert total == 5


def test_known_example_max():
    cost = [
        [4, 1, 3],
        [2, 0, 5],
        [3, 2, 2]
    ]
    assign, total = hungarian(cost, maximize=True)
    # Для max: прибыль = 4+5+3 = 12 (назначение 0→0,1→2,2→0 или аналогичное)
    # Проверяем, что общая прибыль совпадает с максимальной
    _, ref_total = reference_assignment(cost, maximize=True)
    assert pytest.approx(total, rel=1e-7) == ref_total

# 1. Пустая матрица

def test_empty_matrix():
    assign, total = hungarian([], maximize=False)
    assert assign == []
    assert total == 0.0

# 2. Несквадратная матрица → ValueError

def test_non_square_matrix():
    with pytest.raises(ValueError):
        hungarian([[1, 2], [3, 4], [5, 6]])

# 3. Матрица с inf и NaN → ValueError

def test_inf_nan_values():
    mat_inf = [[1, 2], [3, float('inf')]]
    mat_nanf = [[1, 2], [math.nan, 4]]
    with pytest.raises(ValueError):
        hungarian(mat_inf)
    with pytest.raises(ValueError):
        hungarian(mat_nanf)

# 4. Максимизация с бесконечным максимумом → ValueError

def test_max_with_infinite_max():
    mat = [[1, 2], [3, float('inf')]]
    with pytest.raises(ValueError):
        hungarian(mat, maximize=True)