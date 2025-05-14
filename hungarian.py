# hungarian.py

from typing import List, Tuple


def hungarian(cost: List[List[float]], maximize: bool = False) -> Tuple[List[int], float]:
    """
    Решение задачи о назначениях методом Венгера.

    Args:
        cost: Квадратная матрица стоимостей размера n×n.
        maximize: Если True — решаем задачу на максимум (по умолчанию минимум).

    Returns:
        assignment: Список длины n, где assignment[i] = индекс столбца,
                    назначенный строке i.
        total_cost: Общая стоимость (или прибыль, если maximize=True).

    Raises:
        ValueError: если матрица не является квадратной или содержит inf/NaN.
    """
    # Проверка размеров
    n = len(cost)
    if any(len(row) != n for row in cost):
        raise ValueError("Матрица должна быть квадратной (n x n)")

    # Проверка на inf/NaN
    for i, row in enumerate(cost):
        for j, val in enumerate(row):
            if val != val or val in (float('inf'), float('-inf')):
                raise ValueError(f"Матрица содержит недопустимое значение в элементе ({i}, {j})")

    # Копируем матрицу и при необходимости превращаем максимум в минимум
    C = [row[:] for row in cost]
    if maximize:
        M = max(max(row) for row in C)
        # Если M бесконечность, дальше нет смысла
        if M == float('inf') or M == float('-inf'):
            raise ValueError("Невозможно решать задачу максимизации из-за бесконечных значений")
        for i in range(n):
            for j in range(n):
                C[i][j] = M - C[i][j]

    # Пустая задача
    if n == 0:
        return [], 0.0

    # Шаг 1: вычитаем минимумы по строкам
    for i in range(n):
        mi = min(C[i])
        for j in range(n):
            C[i][j] -= mi

    # Шаг 2: вычитаем минимумы по столбцам
    for j in range(n):
        mj = min(C[i][j] for i in range(n))
        for i in range(n):
            C[i][j] -= mj

    # Инициализация меток и вспомогательных массивов
    u = [0] * (n + 1)
    v = [0] * (n + 1)
    p = [0] * (n + 1)
    way = [0] * (n + 1)

    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [float('inf')] * (n + 1)
        used = [False] * (n + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = float('inf')
            j1 = 0
            for j in range(1, n + 1):
                if not used[j]:
                    cur = C[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break

    # Составление задания
    assignment = [-1] * n
    for j in range(1, n + 1):
        if p[j] != 0:
            assignment[p[j] - 1] = j - 1

    total = sum(cost[i][assignment[i]] for i in range(n))
    return assignment, total