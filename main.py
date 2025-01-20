import gradio as gr
from general_consultation import GeneralConsultation
# 아래는 추후 구현될 다른 모듈들입니다
# from drug_info import DrugInfo
# from symptom_checker import SymptomChecker
# from paper_analysis import PaperAnalysis

def create_app():
    """메인 Gradio 애플리케이션 생성"""
    
    # 각 모듈 초기화
    general_consultation = GeneralConsultation()
    
    # Gradio 인터페이스 생성
    with gr.Blocks() as app:
        gr.Markdown("# 의료 상담 시스템")
        
        with gr.Tabs():
            # 일반 상담 탭
            with gr.Tab("일반 상담"):
                general_consultation.create_interface()
            
            # 향후 추가될 다른 탭들
            with gr.Tab("의약품 정보"):
                gr.Markdown("## 준비 중입니다...")
            
            with gr.Tab(""):
                gr.Markdown("## 준비 중입니다...")
            
            with gr.Tab(""):
                gr.Markdown("## 준비 중입니다...")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.launch()