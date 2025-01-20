import gradio as gr
from modules.general_consultation import GeneralConsultation
from modules.drug_info import DrugInfo
from modules.symptom_checker import SymptomChecker
from modules.paper_analysis import PaperAnalysis
from config import GEMINI_API_KEY

def create_app():
    """메인 Gradio 애플리케이션 생성"""
    
    # 각 모듈 초기화
    general_consultation = GeneralConsultation(GEMINI_API_KEY)
    drug_info = DrugInfo()
    symptom_checker = SymptomChecker(GEMINI_API_KEY)
    paper_analysis = PaperAnalysis(GEMINI_API_KEY)
    
    # Gradio 인터페이스 생성
    with gr.Blocks() as app:
        gr.Markdown("# 의료 상담 시스템")
        
        with gr.Tabs():
            # 일반 상담 탭
            with gr.Tab("일반 상담"):
                general_consultation.create_interface()
            
            # 의약품 정보 탭
            with gr.Tab("의약품 정보"):
                drug_info.create_interface()
            
            # 증상 체크 탭
            with gr.Tab("증상 체크"):
                symptom_checker.create_interface()
            
            # 의학 논문 탭
            with gr.Tab("의학 논문"):
                paper_analysis.create_interface()
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.launch()