# Координаты сегментов цифр из семи отрезков
OFFSETS = (
    (0, 0, 1, 0),  # верх
    (1, 0, 1, 1),  # верхний правый
    (1, 1, 1, 2),  # нижний правый
    (0, 2, 1, 2),  # низ
    (0, 1, 0, 2),  # нижний левый
    (0, 0, 0, 1),  # нижний правый
    (0, 1, 1, 1),  # середина
)

# структура цифр
DIGITS = (
    (1, 1, 1, 1, 1, 1, 0),  # 0
    (0, 1, 1, 0, 0, 0, 0),  # 1
    (1, 1, 0, 1, 1, 0, 1),  # 2
    (1, 1, 1, 1, 0, 0, 1),  # 3
    (0, 1, 1, 0, 0, 1, 1),  # 4
    (1, 0, 1, 1, 0, 1, 1),  # 5
    (1, 0, 1, 1, 1, 1, 1),  # 6
    (1, 1, 1, 0, 0, 0, 0),  # 7
    (1, 1, 1, 1, 1, 1, 1),  # 8
    (1, 1, 1, 1, 0, 1, 1),  # 9
)


