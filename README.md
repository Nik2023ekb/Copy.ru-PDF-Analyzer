# PDF Analyzer (PySide6 + PyMuPDF)

Минимальное десктоп-приложение для анализа PDF:
- Общее количество страниц
- Размеры страниц (уникальные размеры, количество и номера)
- Цветные страницы (количество, номера и размеры)
- Чёрно-белые страницы (количество, номера и размеры)

## Быстрый старт (macOS, zsh)

```bash
cd "/Users/matveyromanov/Documents/Новая папка"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m src
```

## Сборка standalone-файла (PyInstaller)

```bash
chmod +x build_macos.sh
./build_macos.sh
```

Результат будет в ./dist/PDFAnalyzer
