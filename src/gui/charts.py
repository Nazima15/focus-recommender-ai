# ------------------------------
# ✨ 진호 씨 해야 할 작업
# 1) Matplotlib 추가해서 그래프 실제 그리기
# 2) df 받아서 공부시간/SNS시간 트렌드 그래프 그리기
# 3) UI에 그래프 표시
# ------------------------------

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


class ChartWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # 기본 안내 문구
        self.label = QLabel("그래프 영역 (아직 데이터 없음)")
        layout.addWidget(self.label)

        self.setLayout(layout)

    # --------------------------
    # ✨ df 받아서 그래프 업데이트
    # --------------------------
    def update_chart(self, df):
        # ❗ Matplotlib 임베드해서 그래프 그리기
        # ❗ 공부 시간 / SNS 시간 / 유튜브 시간 패턴 시각화
        pass
