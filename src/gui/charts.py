# src/gui/charts.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

# Mac 한글 폰트
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False


class ChartWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # 그림자 있는 카드 스타일
        self.setStyleSheet("""
            background-color: #FFFFFF;
            border-radius: 14px;
            padding: 10px;
        """)

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def smooth(self, y):
        """데이터를 부드럽게 보이도록 처리 (곡선형 라인)"""
        x = np.arange(len(y))
        z = np.polyfit(x, y, 3)
        p = np.poly1d(z)
        return p(x)

    def update_chart(self, df):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # 파스텔 색상
        colors = {
            '공부': '#4A90E2',     # 파란 파스텔
            'SNS': '#F5A623',      # 주황 파스텔
            '유튜브': '#7ED321'    # 연두 파스텔
        }

        # 각 항목 그래프 그리기
        for column in ['공부', 'SNS', '유튜브']:
            y = df[column].values
            y_smooth = self.smooth(y)

            ax.plot(
                df['날짜'],
                y_smooth,
                label=f"{column} 시간",
                linewidth=2.5,
                marker="o",
                markersize=7,
                color=colors[column],
            )

        # 제목 & 라벨
        ax.set_title("지난 7일 집중 패턴", fontsize=15, weight='bold', pad=15)
        ax.set_xlabel("날짜", fontsize=12)
        ax.set_ylabel("시간 (분)", fontsize=12)

        # 날짜 라벨 안 겹치게
        ax.tick_params(axis='x', rotation=20)

        # 그리드 라인
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.4)

        # 범례
        ax.legend(frameon=False, fontsize=11, loc='upper left')

        # 여백 줄이기
        self.figure.tight_layout()

        # 그리기
        self.canvas.draw()
