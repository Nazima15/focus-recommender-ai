from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QStackedWidget, QFileDialog, QFrame
)
from PyQt5.QtCore import Qt
from gui.charts import ChartWidget
import pandas as pd
import matplotlib

# Mac 한글 폰트
matplotlib.rcParams['font.family'] = 'AppleGothic'
matplotlib.rcParams['axes.unicode_minus'] = False


# ---------------- DashboardPage ----------------
class DashboardPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.ai_result_label = None  # 예측 결과 표시용

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 🔵 추천 시간 라벨
        self.focus_label = QLabel("📊 오늘의 집중 추천 시간: -")
        self.focus_label.setAlignment(Qt.AlignCenter)
        self.focus_label.setStyleSheet("font-size:22px; font-weight:bold; color:#2E4053;")
        layout.addWidget(self.focus_label)

        # 🔵 오늘 요약 카드 3개
        cards_layout = QHBoxLayout()
        for title, value in [
            ("공부", "0분"),
            ("SNS", "0분"),
            ("유튜브", "0분")
        ]:
            card = self._create_info_card(title, value)
            cards_layout.addWidget(card)
        layout.addLayout(cards_layout)

        # 🔵 그래프 영역
        self.chart_widget = ChartWidget()
        layout.addWidget(self.chart_widget)

        # 🔵 AI 예측 결과 표시
        self.ai_result_label = QLabel("⚙ 아직 예측되지 않았습니다.")
        self.ai_result_label.setAlignment(Qt.AlignCenter)
        self.ai_result_label.setStyleSheet(
            "font-size:16px; color:#1A5276; background:#EBF5FB;"
            "padding:10px; border-radius:8px;"
        )
        layout.addWidget(self.ai_result_label)

        # 🔵 버튼 영역
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.btn_load = QPushButton("데이터 불러오기")
        self.btn_predict = QPushButton("AI 예측하기")
        self.btn_pdf = QPushButton("PDF로 저장")
        self.btn_detail = QPushButton("상세 분석 보기")

        for btn in [self.btn_load, self.btn_predict, self.btn_pdf, self.btn_detail]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498DB;
                    color: white;
                    border-radius: 8px;
                    padding: 10px 18px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #5DADE2;
                }
            """)
            btn_layout.addWidget(btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # 버튼 이벤트 연결
        self.btn_load.clicked.connect(self.load_csv)
        self.btn_predict.clicked.connect(self.predict)
        self.btn_pdf.clicked.connect(self.save_pdf)
        self.btn_detail.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

    # -------- 카드 UI 생성 함수 --------
    def _create_info_card(self, title, value):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("""
            background:#F8F9F9; border:1px solid #D5D8DC;
            border-radius:12px; padding:15px;
        """)
        layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size:16px; font-weight:bold; color:#34495E;")

        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("font-size:20px; color:#1F618D;")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        frame.setLayout(layout)
        return frame

    # -------- CSV 불러오기 --------
    def load_csv(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "CSV 파일 선택", "", "CSV Files (*.csv)")
        if file_name:
            try:
                df = pd.read_csv(file_name)
                self.chart_widget.update_chart(df)
                self.ai_result_label.setText("📁 CSV 불러오기 완료!")
            except Exception as e:
                self.ai_result_label.setText(f"❗ CSV 오류: {e}")

    # -------- AI 예측하기 --------
    def predict(self):
        # 실제에서는 predictor.predict(data) 연결됨
        predicted = "14:00 ~ 16:00"  # 예시

        self.focus_label.setText(f"📊 오늘의 집중 추천 시간: {predicted}")
        self.ai_result_label.setText(f"🤖 AI 예측 결과: 오늘은 {predicted} 집중이 가장 좋아요!")

    # -------- PDF 저장 --------
    def save_pdf(self):
        self.ai_result_label.setText("📄 PDF 저장 기능은 아직 준비 중입니다.")


# ---------------- DetailPage ----------------
class DetailPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 제목
        title = QLabel("📘 상세 분석 리포트")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:22px; font-weight:bold; color:#2E4053;")
        layout.addWidget(title)

        # 상세 레포트 박스
        report_text = (
            "📄 오늘의 전체 분석\n"
            "─────────────────────\n"
            "• 공부: 120분\n"
            "• SNS: 60분\n"
            "• 유튜브: 30분\n"
            "• 수면: 7시간\n\n"
            "🤖 AI 분석 결과:\n"
            "• 가장 집중 잘 되는 시간대: 14~16시\n"
            "• 추천 포모도로: 25분 집중 + 5분 휴식 × 6세트"
        )

        box = QLabel(report_text)
        box.setAlignment(Qt.AlignLeft)
        box.setStyleSheet("""
            background:#FBFCFC; border:1px solid #D6DBDF;
            border-radius:10px; padding:20px; font-size:15px;
        """)
        layout.addWidget(box)

        # 뒤로가기 버튼
        back_btn = QPushButton("뒤로가기")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C; color: white;
                border-radius: 8px; padding: 10px 15px; font-size: 14px;
            }
            QPushButton:hover { background-color: #EC7063; }
        """)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)


# ---------------- MainWindow ----------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Focus Recommender AI")
        self.setMinimumWidth(780)

        self.stacked_widget = QStackedWidget()
        self.dashboard = DashboardPage(self.stacked_widget)
        self.detail = DetailPage(self.stacked_widget)

        self.stacked_widget.addWidget(self.dashboard)
        self.stacked_widget.addWidget(self.detail)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
