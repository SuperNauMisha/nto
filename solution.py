from ctypes.wintypes import tagSIZE

import cv2
import threading
from dotenv import load_dotenv
from nto.final import Task
from my_teleop import MyTeleop


load_dotenv('.env')


def teleop_worker(teleop: MyTeleop):
    pass
    # """
    # Функция для запуска управления роботом с клавиатуры в отдельном потоке.
    # """
    # teleop.run()

def solve():
    # Создаем экземпляр класса Task и запускаем задание (параметры могут задаваться через .env)
    # task = Task()
    # task.start({
    #             "camera_url": "http://root:admin@10.128.73.50/mjpg/video.mjpg",
    #             "server_address": "localhost",
    #             "server_port": 8000,
    #             "task_id": 1
    #         })
    #
    # task.start()
    #
    # # Выводим полученное задание
    # print("Task details:")
    # print(task.getTask())

    # Создаем объект для управления роботом с клавиатуры
    teleop = MyTeleop()
    # Запускаем обработку клавиатуры в отдельном потоке
    teleop_thread = threading.Thread(target=teleop_worker, args=(teleop,), daemon=True)
    teleop_thread.start()

    # Запускаем цикл обновления изображения с камеры
    scene = [None]
    while True:
    	teleop.send_velocity(100, 100)
        # scene = task.getTaskScene()
        if scene and scene[0] is not None:
            frame = scene[0]
        else:
            # print("Failed to capture frame.")
            continue

    # Пример вызова проверки востребованных грузов и фиксации доставки
    try:
        demanded = task.checkCargoDemand()
        if demanded:
            print("Demanded cargos:")
            for cargo in demanded:
                print(cargo)
        else:
            print("No demanded cargos at the moment.")
    except Exception as e:
        print("Error checking cargo demand:", e)

    try:
        result = task.cargoDelivered("C1", "U1")
        print("Cargo delivery result:")
        print(result)
    except Exception as e:
        print("Error during cargo delivery:", e)

    # Завершаем работу: освобождаем ресурсы камеры и закрываем окна
    task.stop()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    solve()
