import pyautogui
import time
import random
from datetime import datetime
import requests

# ============================================================================
# Вспомогательные функции для рандомизированных задержек
# ============================================================================

def random_sleep_parts(total, parts):
    """
    Делит общее время total (в секундах) на случайные доли, суммарно равные total,
    и делает последовательные вызовы time.sleep() для каждой части.
    """
    weights = [random.random() for _ in range(parts)]
    total_weight = sum(weights)
    for w in weights:
        duration = total * (w / total_weight)
        time.sleep(duration)

def randomized_sleep_range(min_time, max_time, parts):
    """
    Выбирает случайное время в интервале [min_time, max_time] и разбивает его на 'parts'
    случайных частей.
    """
    total = random.uniform(min_time, max_time)
    random_sleep_parts(total, parts)

# ============================================================================
# Функция для отправки сообщения в Telegram
# ============================================================================

def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Ошибка отправки сообщения: {response.text}")
    except Exception as e:
        print(f"Исключение при отправке сообщения: {e}")

# ============================================================================
# Функция для чтения координат из файла main.txt
# ============================================================================

def read_coordinates(file_path):
    coordinates = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '/' in line:
                    x, y = map(int, line.strip().split('/'))
                    coordinates.append((x, y))
        return coordinates
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return []
    except ValueError:
        print(f"Ошибка в формате файла {file_path}.")
        return []

# ============================================================================
# Функция для получения рандомной точки внутри фиксированной области
# ============================================================================

def apply_jitter(x, y):
    """
    Добавляет случайное смещение для фиксированных координат.
    Для координаты (x, y) генерируется случайная точка в квадрате:
      по оси X: [x-5, x+4]
      по оси Y: [y-5, y+4]
    Таким образом, если исходная точка (100, 100), возможны точки с (95, 95) до (104, 104)
    (всего 100 вариантов).
    """
    jitter_x = x + random.randint(-5, 4)
    jitter_y = y + random.randint(-5, 4)
    return jitter_x, jitter_y

# ============================================================================
# Основной функционал для обработки файла и выполнения кликов
# ============================================================================

def process_file(file_path, activation_coordinates, fixed_coordinates):
    # Получаем время начала выполнения (для логирования)
    start_time = datetime.now()
    print(f"Начало выполнения: {start_time.strftime('%H:%M:%S')}")

    coordinates = read_coordinates(file_path)
    if not coordinates:
        return

    # Перемешиваем координаты, полученные из файла
    random.shuffle(coordinates)

    for coord in coordinates:
        x, y = coord

        # Клик по координате активации (без смещения)
        pyautogui.click(x=activation_coordinates[0], y=activation_coordinates[1])
        randomized_sleep_range(1.5, 2.5, 10)

        # Клик по координате из файла (без смещения)
        pyautogui.click(x=x, y=y)
        randomized_sleep_range(1.5, 2.5, 10)
        # Обход фиксированных координат с добавлением смещения
        for fx, fy in fixed_coordinates:
            # Получаем рандомную точку в области смещения
            jittered_fx, jittered_fy = apply_jitter(fx, fy)

            if (fx, fy) == (915, 831):
                # Перед нажатием задержка 4-6 секунд (20 частей)
                randomized_sleep_range(4, 6, 20)
                pyautogui.click(x=jittered_fx, y=jittered_fy)
                # После нажатия задержка 4-6 секунд (20 частей)
                randomized_sleep_range(4, 6, 20)
            else:
                pyautogui.click(x=jittered_fx, y=jittered_fy)
                if (fx, fy) in [(856, 921), (1199, 50)]:
                    if (fx, fy) == (965, 680):
                        randomized_sleep_range(2, 4, 20)
                    randomized_sleep_range(3, 5, 20)
                else:
                    randomized_sleep_range(1.5, 2.5, 10)

        # Дополнительные задержки после обработки координат из файла
        randomized_sleep_range(4, 6, 20)  # вместо time.sleep(5)
        randomized_sleep_range(2, 4, 20)  # вместо time.sleep(3)

    end_time = datetime.now()
    print(f"Завершение выполнения: {end_time.strftime('%H:%M:%S')}")
    return start_time, end_time

# ============================================================================
# Основной код программы
# ============================================================================

def main():
    activation_coordinates = (1543, 1041)  # Координаты для активации (без смещения)
    file_path = 'main.txt'                # Имя файла с координатами

    # Настройки Telegram
    bot_token = ''  # Замените на ваш токен бота
    chat_id = ''  # Замените на ваш chat_id

    # Обновлённые фиксированные координаты
    fixed_coordinates_set_1 = [
        (575, 225),
        (856, 921),
        (915, 831),
        (1199, 50),
        (1529, 35),
    ]

    fixed_coordinates_set_2 = [
        (575, 225),
        (856, 921),
        (915, 831),
        (800, 830),
        (965, 680),
        (1199, 50),
        (1529, 35),
    ]

    # Флаг для чередования наборов координат
    use_first_set = True

    print("Программа запущена. Ожидание подходящего времени...")

    while True:
        now = datetime.now()
        current_hour = now.hour

        if 8 <= current_hour < 24:
            # Отправка сообщения о старте сессии (только время)
            time_str = now.strftime("%H:%M:%S")
            start_msg = f"[tiny verse] отработка начата в {time_str}"
            print(start_msg)
            send_telegram_message(bot_token, chat_id, start_msg)

            print(f"Запуск сессии в {time_str}")
            if use_first_set:
                current_fixed_coordinates = fixed_coordinates_set_1
                print("Используется первый набор фиксированных координат.")
            else:
                current_fixed_coordinates = fixed_coordinates_set_2
                print("Используется второй набор фиксированных координат.")

            result = process_file(file_path, activation_coordinates, current_fixed_coordinates)
            if result is None:
                break
            start_time, end_time = result

            # Отправка сообщения о завершении сессии (только время)
            end_time_str = end_time.strftime("%H:%M:%S")
            finish_msg = f"[tiny verse] отработка закончена в {end_time_str}"
            send_telegram_message(bot_token, chat_id, finish_msg)
            print("Сессия отработана.")

            # Чередуем набор координат для следующей сессии
            use_first_set = not use_first_set
            # Задержка между сессиями: от 5 до 15 минут, разбитых на 20 частей
            print("Ожидание следующей сессии (от 5 до 15 минут)...")
            randomized_sleep_range(5 * 60, 15 * 60, 20)
        else:
            print("Неробочее время. Ожидание рабочего времени...")
            # Ночной режим: 8 часов + от 10 до 20 минут дополнительно, разбитых на 50 частей
            randomized_sleep_range(8 * 3600 + 10 * 60, 8 * 3600 + 20 * 60, 50)

if __name__ == "__main__":
    main()
