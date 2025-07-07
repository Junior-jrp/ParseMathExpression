import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                               QLabel, QLineEdit, QPushButton, QMessageBox, QStyle,
                               QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QPixmap
from parser import resolver_expressao, LexerError, ParserError


class ParserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de Expressões")
        self.setMinimumSize(600, 500)
        self.setWindowIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c313c;
            }
            QLabel {
                color: #e0e0e0;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit {
                background-color: #3a3f4b;
                border: 1px solid #4a4f5b;
                border-radius: 8px;
                padding: 12px;
                color: #f0f0f0;
                font-size: 16px;
                font-family: 'Consolas', 'Courier New', monospace;
            }
            QLineEdit:focus {
                border: 1px solid #7a8290;
            }
            QPushButton {
                background-color: #5a6373;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #6a7383;
            }
            QPushButton:pressed {
                background-color: #4a5363;
            }
            QMessageBox {
                background-color: #3a3f4b;
            }
            QTabWidget::pane {
                border: 1px solid #4a4f5b;
                border-top: none;
            }
            QTabBar::tab {
                background-color: #3a3f4b;
                color: #e0e0e0;
                padding: 10px 20px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background-color: #2c313c;
                border: 1px solid #4a4f5b;
                border-bottom: 1px solid #2c313c;
            }
            QTabBar::tab:!selected {
                margin-top: 2px;
            }
            QTableWidget {
                background-color: #3a3f4b;
                color: #e0e0e0;
                gridline-color: #4a4f5b;
                border: none;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #2c313c;
                color: #ffffff;
                padding: 8px;
                border: 1px solid #4a4f5b;
                font-weight: bold;
            }
        """)

        self.tabs = QTabWidget()
        self.calculadora_tab = QWidget()
        self.exemplos_tab = QWidget()
        self.sobre_tab = QWidget()

        self.tabs.addTab(self.calculadora_tab, "Calculadora")
        self.tabs.addTab(self.exemplos_tab, "Exemplos")
        self.tabs.addTab(self.sobre_tab, "Sobre")

        self.setup_calculadora_tab()
        self.setup_exemplos_tab()
        self.setup_sobre_tab()

        self.setCentralWidget(self.tabs)

    def setup_calculadora_tab(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("Calculadora de Expressões")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        self.expressao_entry = QLineEdit()
        self.expressao_entry.setPlaceholderText("Digite a expressão, ex: 2 * (3 + 4)^2")
        self.expressao_entry.returnPressed.connect(self.calcular)
        layout.addWidget(self.expressao_entry)

        self.calcular_button = QPushButton("Calcular")
        self.calcular_button.setMinimumHeight(50)
        self.calcular_button.clicked.connect(self.calcular)
        layout.addWidget(self.calcular_button)

        self.expressao_calculada_label = QLabel("")
        self.expressao_calculada_label.setFont(QFont("Consolas", 16))
        self.expressao_calculada_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.expressao_calculada_label.setStyleSheet("color: #a0a0a0;")
        layout.addWidget(self.expressao_calculada_label)

        self.resultado_label = QLabel("Resultado")
        self.resultado_label.setFont(QFont("Segoe UI", 14))
        self.resultado_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.resultado_label)

        self.resultado_display = QLabel("?")
        self.resultado_display.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        self.resultado_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.resultado_display.setStyleSheet("color: #50fa7b;")
        layout.addWidget(self.resultado_display)

        layout.addStretch()
        self.calculadora_tab.setLayout(layout)

    def setup_exemplos_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Expressão", "Resultado / Erro"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.populate_exemplos_table()

        layout.addWidget(self.table)
        self.exemplos_tab.setLayout(layout)

    def setup_sobre_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap('logo.png')

        if not pixmap.isNull():
            image_label.setPixmap(pixmap.scaledToWidth(150, Qt.TransformationMode.SmoothTransformation))
        else:
            image_label.setText("[logo.png não encontrado]")
            image_label.setFont(QFont("Segoe UI", 12))
            image_label.setStyleSheet("border: 1px dashed #4a4f5b; border-radius: 8px; padding: 10px;")
            image_label.setMinimumSize(150, 150)

        texto_sobre = """
            <p align="justify">
            Este projeto foi desenvolvido como parte avaliativa da disciplina de 
            <b>Teoria da Computação</b>, servindo como uma ferramenta prática para 
            o estudo e a demonstração de conceitos fundamentais de análise léxica e sintática 
            na construção de um parser de expressões matemáticas.
            </p>
            <br>
            <p align="center">
            IFCE - Campus Maracanaú<br>
            2025
            </p>
        """
        sobre_label = QLabel(texto_sobre)
        sobre_label.setFont(QFont("Segoe UI", 14))
        sobre_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sobre_label.setWordWrap(True)

        layout.addStretch()
        layout.addWidget(image_label)
        layout.addSpacing(20)
        layout.addWidget(sobre_label)
        layout.addStretch()

        self.sobre_tab.setLayout(layout)

    def populate_exemplos_table(self):
        expressoes_exemplo = [
            "3 + 4 * 5", "10 / 2 + 3", "1 + 2 - 3 * 4 / 2 + 5",
            "-5 + 10", "10 / -(-2)", "2 ^ 3", "2 * 3 ^ 2",
            "(2 * 3) ^ 2", "2 ^ 3 ^ 2", "100 / 2 ^ 2 / 5",
            "-2 ^ 4", "(-2) ^ 4", "10 / 0", "", "10 +",
            "(3 + 4", "3 & 4"
        ]

        self.table.setRowCount(len(expressoes_exemplo))

        for i, expr in enumerate(expressoes_exemplo):
            expr_item = QTableWidgetItem(expr if expr else "'' (vazio)")

            try:
                resultado = resolver_expressao(expr)
                resultado_formatado = f"{resultado:g}"
                resultado_item = QTableWidgetItem(resultado_formatado)
                resultado_item.setForeground(QColor("#50fa7b"))
            except Exception as e:
                resultado_item = QTableWidgetItem(f"{type(e).__name__}: {e}")
                resultado_item.setForeground(QColor("#ff5555"))

            self.table.setItem(i, 0, expr_item)
            self.table.setItem(i, 1, resultado_item)

    def calcular(self):
        expressao_str = self.expressao_entry.text()
        if not expressao_str.strip():
            self.show_error("Entrada vazia", "Por favor, digite uma expressão matemática.")
            return

        try:
            resultado = resolver_expressao(expressao_str)
            resultado_formatado = f"{resultado:g}"

            self.resultado_display.setText(resultado_formatado)
            self.expressao_calculada_label.setText(f'Expressão: {expressao_str}')

        except (LexerError, ParserError, ZeroDivisionError, Exception) as e:
            self.show_error("Erro na Expressão", f"Ocorreu um erro ao calcular:\n{e}")
            self.resultado_display.setText("?")
            self.expressao_calculada_label.setText("")

    def show_error(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParserApp()
    window.show()
    sys.exit(app.exec())
