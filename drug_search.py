#!/usr/bin/env python
# coding: utf-8

# In[41]:


import gradio as gr
import requests
import google.generativeai as genai
from config import GEMINI_API_KEY
from typing import List, Dict
from config import OPENFDA_API_KEY, OPENFDA_API_URL


# In[42]:


class DrugSearch:
    def __init__(self):
        """약물 검색 모듈 초기화"""
        genai.configure(api_key=GEMINI_API_KEY)
        self.api_key = OPENFDA_API_KEY
        self.model = genai.GenerativeModel('gemini-pro')
    
    def translate_condition(self, text: str) -> str:
        """한글 질병/증상명을 영어로 번역"""
        try:
            if text.isascii():  # 이미 영어면 번역하지 않음
                return text
                
            prompt = f"Translate this medical condition to English (one word only): {text}"
            response = self.model.generate_content(prompt)
            return response.text.strip()
                
        except Exception as e:
            print(f"번역 오류: {e}")
            return text
    
    def search_drugs(self, condition: str) -> str:
        """질병/증상에 따른 약물 검색"""
        try:
            if not condition.strip():
                return "검색어를 입력해주세요."
            
            # 한글 입력을 영어로 번역
            condition = self.translate_condition(condition)
                
            url = f"{OPENFDA_API_URL}event.json"
            params = {
                "api_key": self.api_key,
                "search": f"patient.drug.drugindication:{condition}",
                "count": "patient.drug.medicinalproduct.exact",
                "limit": 10
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if "results" not in data:
                return "검색 결과가 없습니다."
            
            result_text = f"'{condition}'에 대한 약물 검색 결과:\n\n"
            
            for i, drug in enumerate(data["results"], 1):
                result_text += f"{i}. {drug['term']}\n"
                result_text += f"   처방 건수: {drug['count']:,}건\n\n"
            
            return result_text
            
        except Exception as e:
            return f"검색 중 오류가 발생했습니다: {str(e)}"
    
    def create_interface(self) -> gr.Blocks:
        """Gradio 인터페이스 생성"""
        with gr.Blocks() as interface:
            gr.Markdown("""
                ## 질병/증상별 약물 검색
                질병이나 증상을 한글 또는 영문으로 입력하면 관련된 약물 정보를 검색합니다.
                
                입력 예시:
                - 감기 / cold
                - 당뇨병 / diabetes
                - 고혈압 / hypertension
                - 소화불량 / dyspepsia
                - 알레르기 / allergy
                - 비염 / rhinitis
                - 불면증 / insomnia
                - 관절염 / arthritis
            """)
            
            with gr.Row():
                condition_input = gr.Textbox(
                    label="질병/증상 입력",
                    placeholder="질병이나 증상을 입력하세요 (예: 감기, cold)"
                )
                search_button = gr.Button("약물 검색")
            
            result_output = gr.Textbox(label="검색 결과", lines=10)
            
            search_button.click(
                fn=self.search_drugs,
                inputs=condition_input,
                outputs=result_output
            )
            
        return interface


# In[43]:


if __name__ == "__main__":
    DSearch = DrugSearch()
    demo = DSearch.create_interface()
    demo.launch()
