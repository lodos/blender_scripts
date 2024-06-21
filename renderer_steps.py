import bpy
import os

def choose_blend_file():
    # Функция для выбора файла .blend
    while True:
        blend_file_path = input("Введите путь к файлу проекта Blender: ").strip()
        if blend_file_path.endswith('.blend') and os.path.isfile(blend_file_path):
            return blend_file_path
        else:
            print(f"Файл '{blend_file_path}' не найден или не является файлом проекта Blender. Пожалуйста, введите корректный путь.")

def choose_frame_range():
    # Функция для выбора стартового и конечного кадра
    frame_ranges = []
    while True:
        start_frame = int(input("Введите начальный кадр: ").strip())
        end_frame = int(input("Введите конечный кадр: ").strip())

        if start_frame < end_frame:
            frame_ranges.append((start_frame, end_frame))
            add_more = input("Хотите добавить еще один диапазон кадров? (yes/no): ").strip().lower()
            if add_more != 'yes':
                break
        else:
            print("Ошибка: начальный кадр должен быть меньше конечного кадра. Попробуйте снова.")

    return frame_ranges

def choose_output_directory():
    # Функция для указания директории для выходных .mp4 файлов
    while True:
        output_directory = input("Введите путь к директории для сохранения выходных .mp4 файлов: ").strip()
        if os.path.isdir(output_directory):
            return output_directory
        else:
            print(f"Директория '{output_directory}' не найдена. Пожалуйста, введите корректный путь.")

def choose_output_filename():
    # Функция для указания имени выходного .mp4 файла
    output_file_name = input("Введите имя выходного .mp4 файла (без расширения): ").strip()
    return output_file_name + '.mp4'

def setup_rendering(scene):
    # Функция для настройки параметров рендеринга

    # Установка типа вычислительного устройства (CUDA или METAL)
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'METAL'

    # Включение всех доступных устройств GPU
    for device in bpy.context.preferences.addons['cycles'].preferences.devices:
        device.use = True

    # Установка движка рендеринга и параметров
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    scene.cycles.samples = 128
    scene.cycles.adaptive_sampling = True
    scene.cycles.use_denoising = True

    # Установка формата файла и кодека для сохранения
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'HIGH'
    scene.render.ffmpeg.ffmpeg_preset = 'GOOD'

    # Установка количества потоков CPU для рендеринга
    bpy.context.scene.render.threads_mode = 'AUTO'  # Использовать автоматическое определение потоков
    bpy.context.scene.render.threads = 6  # Пример: использовать 6 потока

def render_animation(blend_file, output_file, start_frame, end_frame):
    # Функция для рендеринга анимации

    if not os.path.isfile(blend_file):
        print(f"Файл '{blend_file}' не найден.")
        return

    bpy.ops.wm.open_mainfile(filepath=blend_file)
    scene = bpy.context.scene

    setup_rendering(scene)

    # Создание директории для вывода, если её нет
    output_directory = os.path.dirname(output_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Установка начального и конечного кадров
    scene.frame_start = start_frame
    scene.frame_end = end_frame
    scene.render.filepath = output_file

    try:
        bpy.ops.render.render(animation=True, write_still=False)
    except RuntimeError as ex:
        print(f"Ошибка рендеринга: {ex}")

def run_render_setup():
    # Загрузка текущей сцены
    scene = bpy.context.scene

    # Выбор файла .blend
    blend_file_path = choose_blend_file()

    # Выбор стартового и конечного кадра
    frame_ranges = choose_frame_range()

    # Указание директории для выходных .mp4 файлов
    output_directory = choose_output_directory()

    # Указание имени выходного .mp4 файла
    output_file_name = choose_output_filename()

    # Настройка параметров рендеринга
    setup_rendering(scene)

    # Вывод информации о завершении настройки
    print("\nНастройка параметров рендеринга завершена.")

    # Создание путей к выходным файлам для каждого диапазона кадров
    for start_frame, end_frame in frame_ranges:
        output_file = os.path.join(output_directory, f"{output_file_name.split('.mp4')[0]}_{start_frame}_{end_frame}.mp4")
        print(f"\nРендеринг анимации с {start_frame} по {end_frame}")
        render_animation(blend_file_path, output_file, start_frame, end_frame)

    print("\nРендеринг завершен.")

# Запуск мастера
run_render_setup()
