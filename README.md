# BlenderScripts


## Настройки в файле renderer.py

1. Указать путь к .blend-модели в строке 50 и папку для хранения отрендеренных .mp4 файлов. Папка называется Render и должны присутствовать права на запись
2. Указать диапазоны кадров для рендера в переменной frame_ranges. Каждый элемент массива состоит из 2-х элементов: начальный и конечный кадр. 
3. Указать в строке 15 значение 'GPU' если есть ускоритель, и 'CPU', если нет. Если ускоритель есть, то необходимо указать 'METAL' (Mac OS X M1) или 'CUDA' (NVidia, etc.)
4. Задать желаемые значения:
   - количество сэмплов scene.cycles.samples = 128. Чем выше значение, тем больше проходов при рендере будет выполняться. При значении в 128, в целом, можно продолжать работать с другими программами
   - шаблон для выходного файла scene.render.ffmpeg.ffmpeg_preset = 'GOOD'. Возможные значения GOOD, HIGH, REALTIME
5. Запустить скрипт
6. В папке для рендеринга проверить готовые .mp4 файлы


## Примеры использования

### Вариант №1

Непосредственно, в Blender -> Scripts. Создать новый файл, вставить в него содержимое renderer.py и выполнить

### Вариант №2
Запустить скрипт из консоли, в фоновом режиме. 

Преимущества варианта:
- значительно ускоряет рендеринг 
- освобождает ресурсы за счет того, что не запущен GUI
- позволяет параллельно работать еще в одном проекте Blender
- если позволяют аппаратные ресурсы, можно запускать параллельные потоки рендеринга

Mac OS X \ Linux
```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python /path/to/renderer.py
```

Windows
```powershell
"C:\Program Files\Blender Foundation\Blender\blender.exe" --background --python C:\path\to\renderer.py
```


### Для улучшения дружелюбности, можно использовать из консоли скрипт с пошаговым мастером
Mac OS X \ Linux
```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python /path/to/renderer_steps.py
```

Windows
```powershell
"C:\Program Files\Blender Foundation\Blender\blender.exe" --background --python C:\path\to\renderer_steps.py
```
