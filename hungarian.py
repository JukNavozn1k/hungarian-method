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
    """
    n = len(cost)
    # Копируем матрицу и при необходимости превращаем максимум в минимум
    C = [row[:] for row in cost]
    if maximize:
        # для задачи на максимум: преобразуем pij -> M - pij
        M = max(max(row) for row in C)
        for i in range(n):
            for j in range(n):
                C[i][j] = M - C[i][j]

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

    # Метки вершин и вспомогательные структуры
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
        # Восстановление пути
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break

    # Составляем результат
    assignment = [-1] * n
    for j in range(1, n + 1):
        if p[j] != 0:
            assignment[p[j] - 1] = j - 1

    total = sum(cost[i][assignment[i]] for i in range(n))
    return assignment, total
