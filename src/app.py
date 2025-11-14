# ------------------------------
# ✨ 진호 씨 해야 할 것
# - GUI 실행 구조 유지
# - 나중에 나지마 씨가 만든 AI 모델 연결될 예정
# ------------------------------

from PyQt5.QtWidgets import QApplication
import sys
from gui.main_window import MainWindow


def main():
    # ❗ 기본 GUI 실행 코드 (수정 거의 없음)
    app = QApplication(sys.argv)

    # 메인 창 불러오기
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
