import bpy
import os

def get_project_directory():
    # Функция для получения директории проекта, где расположен данный скрипт
    return os.path.dirname(os.path.abspath(__file__))

def setup_rendering(scene):
    # Функция для настройки параметров рендеринга
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'METAL'  # Использование CUDA для GPU
    for device in bpy.context.preferences.addons['cycles'].preferences.devices:
        device.use = True

    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    scene.cycles.samples = 128
    scene.cycles.adaptive_sampling = True
    scene.cycles.use_denoising = True
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'HIGH'
    scene.render.ffmpeg.ffmpeg_preset = 'GOOD'

def render_animation(blend_file, output_file, start_frame, end_frame):
    if not os.path.isfile(blend_file):
        print(f"Файл '{blend_file}' не найден.")
        return

    bpy.ops.wm.open_mainfile(filepath=blend_file)
    scene = bpy.context.scene

    setup_rendering(scene)

    # Создание директории, если она не существует
    output_directory = os.path.dirname(output_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    scene.frame_start = start_frame
    scene.frame_end = end_frame
    scene.render.filepath = output_file

    try:
        bpy.ops.render.render(animation=True, write_still=False)
    except RuntimeError as ex:
        print(f"Ошибка рендеринга: {ex}")

# Пример использования
blend_file_path = "/Volumes/Untitled/Gym/Blender/bpy/models/Nata_Breath.blend"  # Путь к вашему .blend файлу
project_directory = get_project_directory()
output_directory = "/Volumes/Untitled/Gym/Blender/Render"  # Полный путь к директории Render

frame_ranges = [
    (1, 1),
    (12, 13)
]

# Создание путей к выходным файлам с учетом диапазонов кадров
for start_frame, end_frame in frame_ranges:
    output_file = os.path.join(output_directory, f"out_{start_frame}_{end_frame}.mp4")

    print(f"\nРендеринг анимации с {start_frame} по {end_frame}")
    render_animation(blend_file_path, output_file, start_frame, end_frame)

print("\nРендеринг завершен.")

