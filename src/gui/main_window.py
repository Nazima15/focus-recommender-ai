# ------------------------------
# ✨ 진호 씨 해야 할 작업
# 1) 버튼·레이아웃 디자인 꾸미기
# 2) CSV 불러오기 버튼 누르면 → data_loader 호출하도록 연결 (나지마 코드)
# 3) "예측하기" 버튼 → predictor 연결 (나지마 코드)
# 4) 그래프 업데이트 기능 → charts.py 사용
# 5) 전체 UI 디자인
# ------------------------------

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from gui.charts import ChartWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Focus Recommender AI")
        self.setMinimumWidth(600)

        # --------------------------
        # ✨ 여기서 전체 UI 배치 구성
        # --------------------------
        layout = QVBoxLayout()

        # 제목 영역
        title = QLabel("📊 집중 시간 추천 AI (GUI)")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # CSV 불러오기 버튼
        self.btn_load_csv = QPushButton("CSV 불러오기")
        layout.addWidget(self.btn_load_csv)

        # 예측 버튼
        self.btn_predict = QPushButton("예측하기")
        layout.addWidget(self.btn_predict)

        # 예측 결과 출력 라벨
        self.result_label = QLabel("예측 결과: 없음")
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)

        # 그래프 자리
        self.chart_widget = ChartWidget()
        layout.addWidget(self.chart_widget)

        self.setLayout(layout)

        # --------------------------
        # ✨ 여기서 버튼 기능 연결해야 함
        # self.btn_load_csv.clicked.connect(???)
        # self.btn_predict.clicked.connect(???)
        # --------------------------

    # --------------------------
    # ✨ CSV 불러오기 함수 — 기능은 나지마 코드와 연결해줘야 함
    # --------------------------
    def load_csv_file(self):
        pass  # ❗ 나중에 data_loader.load_csv() 사용

    # --------------------------
    # ✨ 예측 함수 — predictor.predict() 연결
    # --------------------------
    def update_prediction(self):
        pass  # ❗ 나중에 AI 예측 결과 출력

    # --------------------------
    # ✨ 그래프 업데이트 — charts.py에서 작업
    # --------------------------
    def show_charts(self, df):
        pass  # ❗ df 넣어서 그래프 그리도록 만들기
