"""PySide6 GUI for PDF analysis."""

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QFileDialog, QLabel, QFrame
)
from PySide6.QtGui import QPixmap, QDragEnterEvent, QDropEvent
import os
import sys

def resource_path(rel_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel_path)
    return rel_path
from PySide6.QtCore import Qt
from PySide6.QtCore import Qt
from .pdf_analyzer import analyze_pdf


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Copy.ru PDF Analyzer by Ekaterinburg branch")
        self.resize(900, 600)
        self.setStyleSheet("background: #f7f7fa; color: #222;")
        # Установка иконки приложения
        from PySide6.QtGui import QIcon
        self.setWindowIcon(QIcon("src/assets/app_icon.icns"))

        # Главный layout: горизонтальный, без явных колонок
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(24)

        # Слева — вертикальный блок с элементами управления
        controls = QFrame()
        controls.setFrameShape(QFrame.NoFrame)
        controls.setStyleSheet("background: transparent;")
        controls.setAcceptDrops(True)
        controls_layout = QVBoxLayout(controls)
        controls_layout.setAlignment(Qt.AlignTop)
        controls_layout.setSpacing(18)

        # Логотип компактный
        logo = QLabel()
        logo.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(resource_path("src/assets/logo.png"))
        if not pixmap.isNull():
            logo.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            logo.setText("[Логотип]")
        logo.setStyleSheet("background: transparent; margin-bottom: 8px;")
        controls_layout.addWidget(logo)

        # Инструкция
        instr = QLabel('Нажмите кнопку "ОТКРЫТЬ" или перетащите PDF-файл')
        instr.setAlignment(Qt.AlignCenter)
        instr.setWordWrap(True)
        instr.setStyleSheet("font-size: 15px; color: #222; margin: 12px;")
        controls_layout.addWidget(instr)

        # Кнопка ОТКРЫТЬ
        self.open_btn = QPushButton("ОТКРЫТЬ")
        self.open_btn.setStyleSheet("background: #e0e0f0; border-radius: 16px; padding: 12px 28px; font-size: 17px; color: #222; border: 1px solid #c0c0d0;")
        self.open_btn.clicked.connect(self._open_dialog)
        controls_layout.addWidget(self.open_btn)

        controls_layout.addStretch(1)

        # Копирайт — две строки, меньший размер
        copyright = QLabel("© 2025\nСоздано гениальностью MaxArt")
        copyright.setStyleSheet("color: #888; font-size: 11px; margin-top: 8px; line-height: 1.2;")
        copyright.setAlignment(Qt.AlignCenter)
        controls_layout.addWidget(copyright)

        # Справа — поле информации
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setStyleSheet("font-size: 15px; background: #fff; color: #222;")

        main_layout.addWidget(controls)
        main_layout.addWidget(self.result, 1)

        # Drag&Drop
        controls.dragEnterEvent = self.dragEnterEvent
        controls.dropEvent = self.dropEvent

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith('.pdf'):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith('.pdf'):
                self.open_pdf(path)
                break
    def _open_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self, "Открыть PDF", filter="PDF Files (*.pdf)")
        if path:
            self.open_pdf(path)

    def open_pdf(self, path=None):
        if not path:
            return
        self.result.setText("Анализ: " + path)
        try:
            report = analyze_pdf(path)
            self.result.setText(self._format_report(report))
        except Exception as e:
            self.result.setText(f"Ошибка анализа PDF: {e}")
    def _format_report(self, rep: dict) -> str:
        lines = []
        lines.append(f"1. Общее количество страниц: {rep['num_pages']}")

        # Цветные страницы
        lines.append(f"2. Цветных страниц:")
        for fmt in ["A4", "A3", "A2", "A1", "A0", "Другие размеры"]:
            stat = rep['color_stat'][fmt]
            if stat['count'] > 0:
                nums = ", ".join(str(p) for p in stat['pages'])
                lines.append(f"{fmt} — {stat['count']} ({nums})")

        # Чёрно-белые страницы
        lines.append(f"3. ЧБ страниц:")
        for fmt in ["A4", "A3", "A2", "A1", "A0", "Другие размеры"]:
            stat = rep['bw_stat'][fmt]
            if stat['count'] > 0:
                nums = ", ".join(str(p) for p in stat['pages'])
                lines.append(f"{fmt} — {stat['count']} ({nums})")

        return "\n".join(lines)
