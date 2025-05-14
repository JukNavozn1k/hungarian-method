import streamlit as st
from hungarian import hungarian

def parse_matrix(inputs, size):
    """
    Формирование квадратной матрицы из отдельных полей ввода с проверкой данных.
    """
    try:
        matrix = [
            [float(inputs[f"cell_{i}_{j}"]) for j in range(size)]
            for i in range(size)
        ]
        return matrix
    except ValueError:
        st.error("Ошибка: Убедитесь, что все поля заполнены корректными числами.")
        return None



tab1, tab2 = st.tabs(["Рассчитать", "Инструкция"])

with tab1:
    st.write("""
    Этот интерфейс позволяет решать задачу о назначениях с использованием метода Венгера.
    Укажите размерность матрицы, заполните элементы матрицы, выберите режим (минимизация или максимизация) и нажмите "Рассчитать".
    """)

    # Ввод размерности квадратной матрицы с ограничениями
    size = st.number_input("Размерность матрицы (1-10):", min_value=1, max_value=10, step=1, value=3)

    # Ввод элементов матрицы
    st.write("Введите элементы матрицы:")
    inputs = {}
    for i in range(size):
        cols_container = st.columns(size)  # Create columns for each element in the row
        for j in range(size):
            key = f"cell_{i}_{j}"
            placeholder = f"{i+1},{j+1}" # подсказка для пользователя
            inputs[key] = cols_container[j].text_input(f"({i+1}, {j+1})", key=key, placeholder=placeholder, label_visibility="collapsed")

    # Выбор режима
    maximize = st.checkbox("Решать задачу на максимум", value=False)

    # Кнопка для расчета
    if st.button("Рассчитать"):
        cost_matrix = parse_matrix(inputs, size)
        if cost_matrix:
            try:
                assignment, total_cost = hungarian(cost_matrix, maximize=maximize)
                st.success("Результаты:")
                st.write(f"Назначения: {assignment}")
                st.write(f"Общая стоимость: {total_cost}")
            except ValueError as e:
                st.error(f"Ошибка: {e}")

with tab2:
    st.write("""
    **Инструкция по использованию интерфейса:**
    
    1. Укажите размерность квадратной матрицы (от 1 до 10).
    2. Заполните элементы матрицы, вводя числа в соответствующие поля.
    3. Выберите режим:
       - Оставьте флажок пустым для минимизации.
       - Установите флажок для максимизации.
    4. Нажмите кнопку "Рассчитать".
    5. Результаты будут отображены ниже, включая назначения и общую стоимость.
    """)