## 1️⃣ 지금까지 한 일 (GUI 쪽)
* **메인 윈도우(MainWindow) 설계**
  * `DashboardPage` → 메인 화면, 데이터 시각화, 버튼 UI
  * `DetailPage` → 상세 분석 화면, 포모도로 추천 등
    
* **그래프 표시**
  * `ChartWidget` 만들고, Pandas DataFrame 기반으로 공부/SNS/유튜브 시간 시각화
  * Matplotlib로 깔끔한 라인 차트
    
* **버튼 기능**
  * CSV 불러오기 (`QFileDialog` 사용)
  * AI 예측 버튼 → 현재는 더미 텍스트 출력
  * PDF 저장 버튼 → 아직 기능 미구현
  * 상세 분석 보기 → `DetailPage`로 이동
 
* **디자인**
  * 카드 UI, 컬러, 폰트, 배경, 버튼 스타일링
  * Mac 한글 폰트 설정 완료
    
* **앱 실행**
  * `app.py`에서 `QApplication` 생성 후 MainWindow 실행
    
* **Git**
  * GitHub `nazima-dev` 브랜치에 커밋 완료 (`📦 GUI 컴포넌트 구조 정리`)

---
## 2️⃣ 앞으로 AI 쪽 연결 방법
1. **AI 모듈 준비 (진호씨 담당)**
   ```
   ai/
   ├─ predictor.py       # predict(data) 함수
   ├─ model_manager.py   # 모델 로드, 학습/평가
   └─ preprocessing.py   # CSV/데이터 전처리
   ```
2. **GUI → AI 연결**
   * DashboardPage에서 **AI 예측 버튼 클릭** 시
   ```python
   from ai.predictor import predict
   def predict(self):
       # CSV 데이터 불러오기 후 df 전달
       recommended_time = predict(self.df)  # AI가 추천 시간 반환
       self.focus_label.setText(f"📊 오늘의 집중 추천 시간: {recommended_time}")
       self.ai_result_label.setText(f"🤖 AI 예측 결과: 오늘은 {recommended_time} 집중이 가장 좋아요!")
   ```
3. **AI → GUI 결과**
   * 예측된 집중 시간, 포모도로 플랜 등을 GUI에 표시
   * 필요 시 DetailPage에서도 같은 데이터 보여주기

---
## 3️⃣ GitHub 관리
* **브랜치 나누기**
  * `nazima-dev` → GUI 개발
  * `jinho-dev` → AI 기능 개발
  * `main` → 안정 버전 배포
* 나중에 GUI와 AI 브랜치 병합 시 `predict()` 함수 연결

---
💡 **정리**
* 지금까지 GUI 구조 완성 + CSV 불러오기 + 예측 버튼 UI + 그래프
* 앞으로 해야 할 일은 **AI 모듈 구현** + GUI와 연결
* Git으로 브랜치 관리하고 나중에 병합
