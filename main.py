import gradio as gr
from general_consultation import GeneralConsultation
from symptom_image import SymptomImageAnalysis
from drug_search import DrugSearch
from drug_info import DrugInfo

def create_app():
    """메인 Gradio 애플리케이션 생성"""
    
    # 각 모듈 초기화
    general_consultation = GeneralConsultation()
    symptom_image = SymptomImageAnalysis()
    drug_search = DrugSearch()
    drug_info = DrugInfo()
    
    # Gradio 인터페이스 생성
    with gr.Blocks() as app:
        gr.Markdown("# 의료 상담 시스템")
        
        with gr.Tabs():
            with gr.Tab("일반 상담"):
                general_consultation.create_interface()
            
            with gr.Tab("증상 이미지 분석"):
                symptom_image.create_interface()
            
            with gr.Tab("약물 검색"):
                drug_search.create_interface()
            
            with gr.Tab("약물 부작용 정보"):
                drug_info.create_interface()
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.launch(share=True)