#!/usr/bin/env python
# coding: utf-8

# In[19]:


import gradio as gr
import google.generativeai as genai
from typing import List, Tuple
from config import GEMINI_API_KEY, MEDICAL_SYSTEM_PROMPT


# In[20]:


class GeneralConsultation:
    def __init__(self):
        """일반 상담 모듈 초기화"""
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        self.system_prompt = MEDICAL_SYSTEM_PROMPT
    
    def get_medical_response(self, message: str, history) -> str:
        """의료 상담 응답 생성"""
        chat = self.model.start_chat()
        full_prompt = f"{self.system_prompt}\n\n사용자: {message}"
        response = chat.send_message(full_prompt)
        return response.text
    
    def create_interface(self) -> None:
        """Gradio 인터페이스 생성"""
        demo = gr.ChatInterface(
            fn=self.get_medical_response,
            title="의료 상담 챗봇",
            description="의료 관련 질문에 대해 답변해드립니다. (전문의와 상담을 대체할 수 없습니다)",
            examples=[
                ["당뇨병의 초기 증상은 무엇인가요?"],
                ["고혈압을 예방하기 위한 생활 수칙을 알려주세요."],
                ["편두통과 일반 두통의 차이점은 무엇인가요?"]
            ]
        )
        return demo


# In[21]:


if __name__ == "__main__":
    consultation = GeneralConsultation()
    demo = consultation.create_interface()
    demo.launch()

