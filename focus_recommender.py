#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Focus Recommender AI - 최종 완성판 (Windows/macOS PDF 한글 + UI + 차트)
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.utils import simpleSplit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QFrame, QDialog, QTextEdit, QDialogButtonBox, QMessageBox
)
from PyQt5.QtCore import Qt

# ---------------------------
# PDF 한글 폰트 설정
# ---------------------------
def setup_korean_font():
    try:
        if sys.platform.startswith("win"):
            font_path = r"C:\Windows\Fonts\malgun.ttf"
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont("KRFont", font_path))
                return "KRFont"
        if sys.platform == "darwin":
            font_path = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont("KRFont", font_path))
                return "KRFont"
    except:
        pass
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    return "STSong-Light"

PDF_FONT = setup_korean_font()

# ---------------------------
# 리소스 경로 처리 (PyInstaller)
# ---------------------------
def resource_path(relative_path):
    try:
        base = sys._MEIPASS
    except Exception:
        base = os.path.abspath(".")
    return os.path.join(base, relative_path)

# ---------------------------
# 고정 카테고리
# ---------------------------
CATEGORIES = ["학습", "이동", "가정관리", "교제 및 참여활동", "문화 및 여가활동"]

# ---------------------------
# 시간→분 변환
# ---------------------------
def to_minutes(x):
    if pd.isna(x):
        return 0
    s = str(x).strip()
    if s in ("", "nan", "None"):
        return 0
    try:
        if ":" in s:
            h, m = s.split(":")[:2]
            return int(h) * 60 + int(m)
        return int(float(s))
    except:
        return 0

# ---------------------------
# 공공 데이터 전처리
# ---------------------------
def preprocess_public(df_raw):
    df = df_raw.copy()
    df.columns = [c.strip() for c in df.columns]
    df = df.fillna("")
    for col in df.columns[2:]:
        df[col] = df[col].apply(to_minutes)
    df.iloc[:, 2:] = df.iloc[:, 2:].clip(upper=300)
    df["총합"] = df.iloc[:, 2:].sum(axis=1)
    if "행동분류별" not in df.columns:
        raise ValueError("'행동분류별' 컬럼 없음")
    df["행동분류별"] = df["행동분류별"].astype(str).str.strip()
    ratio = df.groupby("행동분류별", as_index=False)["총합"].sum()
    total = ratio["총합"].sum()
    ratio["비율"] = (ratio["총합"] / total * 100).round(1) if total else 0
    ratio = ratio.set_index("행동분류별").reindex(CATEGORIES, fill_value=0).reset_index()
    return df, ratio, df["총합"].mean(), df["총합"].std()

# ---------------------------
# 사용자 데이터 전처리
# ---------------------------
def preprocess_user(df_raw):
    df = df_raw.copy()
    df.columns = [c.strip() for c in df.columns]
    df = df.fillna("")
    for col in df.columns[2:]:
        df[col] = df[col].apply(to_minutes)
    df.iloc[:, 2:] = df.iloc[:, 2:].clip(upper=300)
    df["총합"] = df.iloc[:, 2:].sum(axis=1)
    if "행동분류별" not in df.columns:
        raise ValueError("'행동분류별' 없음")
    df["행동분류별"] = df["행동분류별"].astype(str).str.strip()
    ratio = df.groupby("행동분류별", as_index=False)["총합"].sum()
    total = ratio["총합"].sum()
    ratio["비율"] = (ratio["총합"] / total * 100).round(1) if total else 0
    ratio = ratio.set_index("행동분류별").reindex(CATEGORIES, fill_value=0).reset_index()
    return df, df["총합"].mean(), ratio

# ---------------------------
# AI 추천
# ---------------------------
class AIPredictor:
    TIME_SLOTS = {
        "아침형": ["08:00~10:00", "10:00~12:00"],
        "저녁형": ["15:00~17:00", "17:00~19:00"],
        "일반": ["10:00~12:00", "13:00~15:00", "17:00~19:00"]
    }

    def predict(self, public_avg, _, user_avg, public_ratio_df, user_ratio_df):
        messages = []
        shortage = public_avg - user_avg

        # 패턴 결정
        if shortage > 30:
            chrono = "저녁형"
        elif user_ratio_df[user_ratio_df["행동분류별"] == "학습"]["비율"].iloc[0] > 40:
            chrono = "아침형"
        else:
            chrono = "일반"

        pred_time = self.TIME_SLOTS[chrono][0]

        # 메시지 작성
        if shortage > 0:
            messages.append(f"현재 학습량이 평균보다 {shortage:.0f}분 부족합니다.")
        else:
            messages.append("학습량이 평균 이상입니다!")

        messages.append(f"당신은 '{chrono}' 패턴에 가까워 보입니다.")
        messages.append(f"추천 학습 시작 시간: {pred_time}")
        messages.append("50분 집중 + 10분 휴식 사이클을 추천합니다.")

        return pred_time, "\n".join(messages)

# ---------------------------
# 차트 위젯
# ---------------------------
class ChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.fig = Figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_chart(self, p_df, u_df):
        self.fig.clear()
        plt.rc('font', family='Malgun Gothic' if sys.platform.startswith("win") else "AppleGothic")
        ax = self.fig.add_subplot(111)
        x = np.arange(len(CATEGORIES))
        w = 0.35
        ax.bar(x - w/2, p_df["총합"], w, label="공공")
        ax.bar(x + w/2, u_df["총합"], w, label="사용자")
        ax.set_xticks(x)
        ax.set_xticklabels(CATEGORIES, rotation=20)
        ax.set_title("항목별 총합 비교")
        ax.legend()
        self.canvas.draw()

# ---------------------------
# 상세 보기 창
# ---------------------------
class DetailDialog(QDialog):
    def __init__(self, pred, reason, p_df, u_df):
        super().__init__()
        self.setWindowTitle("상세 보기")
        layout = QVBoxLayout()
        header = QLabel(f"📌 추천 시간: {pred}")
        header.setStyleSheet("font-size:18px;font-weight:bold;")
        layout.addWidget(header)
        box = QTextEdit()
        box.setReadOnly(True)
        box.setText(reason)
        layout.addWidget(box)
        chart = ChartWidget()
        chart.update_chart(p_df, u_df)
        layout.addWidget(chart)
        btn = QDialogButtonBox(QDialogButtonBox.Close)
        btn.rejected.connect(self.reject)
        layout.addWidget(btn)
        self.setLayout(layout)

# ---------------------------
# 메인 페이지
# ---------------------------
class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.public_ratio = pd.DataFrame({"행동분류별": CATEGORIES, "총합":[0]*5, "비율":[0]*5})
        self.user_ratio = pd.DataFrame({"행동분류별": CATEGORIES, "총합":[0]*5, "비율":[0]*5})
        self.public_avg = 0
        self.user_avg = 0
        self.last_pred = "-"
        self.last_reason = "-"
        self.ai = AIPredictor()

        layout = QVBoxLayout()
        title = QLabel("Focus Recommender AI")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:22px;font-weight:bold;color:#4A90E2;")
        layout.addWidget(title)

        self.focus_label = QLabel("오늘의 추천: -")
        self.focus_label.setAlignment(Qt.AlignCenter)
        self.focus_label.setStyleSheet("font-size:18px;font-weight:bold;")
        layout.addWidget(self.focus_label)

        row = QHBoxLayout()
        self.card_pub = self._card("공공 평균", "-")
        self.card_usr = self._card("사용자 평균", "-")
        row.addWidget(self.card_pub)
        row.addWidget(self.card_usr)
        layout.addLayout(row)

        self.chart = ChartWidget()
        layout.addWidget(self.chart)

        btn_row = QHBoxLayout()
        self.btn_load_public = QPushButton("공공 데이터 불러오기")
        self.btn_load_user = QPushButton("사용자 CSV 불러오기")
        self.btn_predict = QPushButton("AI 예측")
        self.btn_pdf = QPushButton("PDF 저장")
        for b in (self.btn_load_public, self.btn_load_user, self.btn_predict, self.btn_pdf):
            b.setStyleSheet("background:#4A90E2;color:white;padding:6px;border-radius:6px;")
            btn_row.addWidget(b)
        layout.addLayout(btn_row)

        self.btn_load_public.clicked.connect(self.load_public)
        self.btn_load_user.clicked.connect(self.load_user)
        self.btn_predict.clicked.connect(self.on_predict)
        self.btn_pdf.clicked.connect(self.save_pdf)

        self.setLayout(layout)
        self.resize(1000, 700)

    def _card(self, title, value):
        f = QFrame()
        f.setStyleSheet("background:#F7F7F7;border:1px solid #aaa;padding:8px;border-radius:8px;")
        v = QVBoxLayout()
        t = QLabel(title)
        t.setAlignment(Qt.AlignCenter)
        val = QLabel(value)
        val.setAlignment(Qt.AlignCenter)
        val.setStyleSheet("font-size:16px;font-weight:bold;")
        f.value = val
        v.addWidget(t)
        v.addWidget(val)
        f.setLayout(v)
        return f

    def load_public(self):
        path = resource_path(os.path.join("data", "study_stats.csv"))
        if not os.path.exists(path):
            QMessageBox.warning(self, "오류", "data/study_stats.csv 없음")
            return
        raw = pd.read_csv(path, dtype=str)
        _, ratio, avg, _ = preprocess_public(raw)
        self.public_ratio = ratio
        self.public_avg = avg
        self.card_pub.value.setText(f"{avg:.1f}")
        self.chart.update_chart(self.public_ratio, self.user_ratio)

    def load_user(self):
        fname, _ = QFileDialog.getOpenFileName(self, "CSV 선택", "", "CSV Files (*.csv)")
        if not fname:
            return
        raw = pd.read_csv(fname, dtype=str)
        _, avg, ratio = preprocess_user(raw)
        self.user_ratio = ratio
        self.user_avg = avg
        self.card_usr.value.setText(f"{avg:.1f}")
        self.chart.update_chart(self.public_ratio, self.user_ratio)

    def on_predict(self):
        pred, reason = self.ai.predict(self.public_avg, 0, self.user_avg,
                                       self.public_ratio, self.user_ratio)
        self.last_pred = pred
        self.last_reason = reason
        self.focus_label.setText(f"오늘의 추천: {pred}")
        dlg = DetailDialog(pred, reason, self.public_ratio, self.user_ratio)
        dlg.exec_()

    def save_pdf(self):
        fname, _ = QFileDialog.getSaveFileName(
            self, "PDF 저장", "focus_report.pdf", "PDF Files (*.pdf)"
        )
        if not fname:
            return
        c = canvas.Canvas(fname, pagesize=A4)
        w, h = A4
        c.setFont(PDF_FONT, 12)

        # 텍스트
        text = f"""
Focus Recommender AI 보고서

📌 추천 집중 시간: {self.last_pred}

📌 추천 이유:
{self.last_reason}

📊 공공 평균: {self.public_avg:.1f}분
📊 사용자 평균: {self.user_avg:.1f}분
"""
        lines = simpleSplit(text, PDF_FONT, 12, w - 80)
        y = h - 60
        for line in lines:
            c.drawString(40, y, line)
            y -= 20

        # 막대그래프
        fig1 = Figure(figsize=(6, 4))
        ax1 = fig1.add_subplot(111)
        x = np.arange(len(CATEGORIES))
        w_b = 0.35
        ax1.bar(x - w_b/2, self.public_ratio["총합"], w_b, label="공공")
        ax1.bar(x + w_b/2, self.user_ratio["총합"], w_b, label="사용자")
        ax1.set_xticks(x)
        ax1.set_xticklabels(CATEGORIES, rotation=20)
        ax1.set_title("항목별 총합 비교")
        ax1.legend()
        fig1.tight_layout()
        temp1 = "temp_bar.png"
        fig1.savefig(temp1, dpi=200)
        c.showPage()
        c.drawImage(temp1, 50, 250, width=500, preserveAspectRatio=True)

        # 파이차트
        fig2 = Figure(figsize=(6, 4))
        ax2 = fig2.add_subplot(111)
        ax2.pie(self.user_ratio["비율"], labels=CATEGORIES, autopct="%1.1f%%")
        fig2.tight_layout()
        temp2 = "temp_pie.png"
        fig2.savefig(temp2, dpi=200)
        c.showPage()
        c.drawImage(temp2, 70, 250, width=400, preserveAspectRatio=True)

        c.save()
        if os.path.exists(temp1):
            os.remove(temp1)
        if os.path.exists(temp2):
            os.remove(temp2)

        QMessageBox.information(self, "완료", "PDF가 저장되었습니다!")

# ---------------------------
# 실행
# ---------------------------
def main():
    app = QApplication(sys.argv)
    w = DashboardPage()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
