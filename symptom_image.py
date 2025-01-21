#!/usr/bin/env python
# coding: utf-8

# In[31]:


import gradio as gr
import google.generativeai as genai
from PIL import Image
from typing import Tuple
from config import GEMINI_API_KEY


# In[32]:


class SymptomImageAnalysis:
    def __init__(self):
        """증상 이미지 분석 모듈 초기화"""
        genai.configure(api_key=GEMINI_API_KEY)
        self.vision_model = genai.GenerativeModel('gemini-1.5-flash')
        
    def analyze_image(self, 
                     image_path: str,
                     additional_info: str = "") -> str:
        """이미지 분석 및 관련 정보 제공"""
        try:
            # 이미지 로드
            img = Image.open(image_path)
            
            # 분석을 위한 프롬프트 구성
            prompt = """
            이 이미지는 의료적 증상을 보여주고 있습니다. 다음 형식으로 분석해주세요:
            
            1. 관찰된 증상:
            - 주요 시각적 특징을 자세히 설명
            
            2. 예비 진단:
            - 가능성 있는 질환이나 상태
            - 주의: 이는 참고용이며 전문의의 진단을 대체할 수 없음
            
            3. 권장 사항:
            - 즉시 병원 방문이 필요한지 여부
            - 일반적인 주의사항
            
            4. 관련 전문의:
            - 진료가 필요한 전문의 과목
            
            추가 정보: {additional_info}
            """
            
            # Gemini Pro Vision으로 이미지 분석
            response = self.vision_model.generate_content([prompt, img])
            return response.text
            
        except Exception as e:
            return f"이미지 분석 중 오류 발생: {str(e)}"

    def create_interface(self) -> None:
        """Gradio 인터페이스 생성"""
        gr.Interface(
            fn=self.analyze_image,
            inputs=[
                gr.Image(label="증상 이미지 업로드", type="filepath"),
                gr.Textbox(
                    label="추가 정보 (선택사항)",
                    placeholder="증상이 시작된 시기, 통증 여부 등 추가 정보를 입력하세요.",
                    lines=3
                )
            ],
            outputs=gr.Textbox(label="분석 결과", lines=10),
            title="피부 증상 이미지 분석",
            description="""
            피부 관련 증상 이미지를 분석하여 관련 정보를 제공합니다.
            
            분석 가능한 증상:
            - 발진, 두드러기, 습진 등의 피부 질환
            - 벌레 물린 자국
            - 일광 화상
            - 접촉성 피부염
            - 가벼운 외상이나 찰과상
            
            주의사항:
            - 심각한 외상이나 응급 상황은 즉시 응급실을 방문하세요
            - 이 분석은 참고용이며 전문의의 진단을 대체할 수 없습니다
            - 이미지는 밝은 조명에서, 선명하게 촬영해주세요
            """,
            examples=[
                ["./image/example_cat.jpg", "팔에 발진이 발생. 3일 전부터 시작되었고 가려움증이 동반됨"],
                ["./image/example_dog.webp", "두드러기로 추정. 어제 저녁부터 시작되었고 약간의 붓기가 있음"]
            ]
        )


# In[33]:


if __name__ == "__main__":
    analyzer = SymptomImageAnalysis()
    with gr.Blocks() as demo:
        analyzer.create_interface()
    demo.launch()

