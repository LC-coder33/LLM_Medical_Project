#!/usr/bin/env python
# coding: utf-8

# In[2]:


import gradio as gr
import google.generativeai as genai
import requests
from typing import List, Tuple, Optional
from config import (
    GEMINI_API_KEY, 
    PUBMED_API_KEY, 
    PUBMED_API_URL, 
    MEDICAL_SYSTEM_PROMPT
)


# In[3]:


class GeneralConsultation:
    def __init__(self):
        """일반 상담 모듈 초기화"""
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        self.system_prompt = MEDICAL_SYSTEM_PROMPT
    
    def get_medical_response(self, message: str, history: List[Tuple[str, str]]) -> str:
        """의료 상담 응답 생성"""
        history = history or []
        
        # 채팅 컨텍스트 설정
        chat = self.model.start_chat(history=[])
        
        # 시스템 프롬프트와 사용자 메시지 결합
        full_prompt = f"{self.system_prompt}\n\n사용자: {message}"
        
        # 응답 생성
        response = chat.send_message(full_prompt)
        
        # 관련 논문 검색
        papers = self.search_pubmed(message)
        
        # 응답과 관련 논문 정보 결합
        full_response = response.text + "\n\n관련 논문:\n"
        for paper in papers[:3]:  # 상위 3개 논문만 표시
            full_response += f"- {paper['title']}\n"
        
        return full_response  # history는 반환하지 않음
    
    def search_pubmed(self, query: str, max_results: int = 3) -> List[dict]:
        """PubMed API로 관련 논문 검색"""
        try:
            # 검색 요청
            search_url = f"{PUBMED_API_URL}esearch.fcgi"
            params = {
                "db": "pubmed",
                "term": query,
                "api_key": PUBMED_API_KEY,
                "retmax": max_results,
                "retmode": "json"
            }
            
            response = requests.get(search_url, params=params)
            data = response.json()
            
            if "esearchresult" not in data:
                return []
                
            id_list = data["esearchresult"]["idlist"]
            
            # 논문 상세 정보 조회
            papers = []
            for pmid in id_list:
                summary_url = f"{PUBMED_API_URL}esummary.fcgi"
                params = {
                    "db": "pubmed",
                    "id": pmid,
                    "api_key": PUBMED_API_KEY,
                    "retmode": "json"
                }
                
                response = requests.get(summary_url, params=params)
                paper_data = response.json()["result"][pmid]
                
                papers.append({
                    "title": paper_data["title"],
                    "authors": paper_data.get("authors", []),
                    "pubdate": paper_data.get("pubdate", ""),
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}"
                })
            
            return papers
            
        except Exception as e:
            print(f"PubMed API 오류: {e}")
            return []
    
    def create_interface(self) -> None:
        """Gradio 인터페이스 생성"""
        gr.ChatInterface(
            self.get_medical_response,
            chatbot=gr.Chatbot(height=400),
            textbox=gr.Textbox(
                placeholder="의료 관련 질문을 입력하세요...",
                lines=2
            ),
            title="의료 상담 챗봇",
            description="의료 관련 질문에 대해 답변해드립니다. (전문의와 상담을 대체할 수 없습니다)",
            examples=[
                ["당뇨병의 초기 증상은 무엇인가요?"],
                ["고혈압을 예방하기 위한 생활 수칙을 알려주세요."],
                ["편두통과 일반 두통의 차이점은 무엇인가요?"]
            ]
        )


# In[4]:


if __name__ == "__main__":
    # 모듈 단독 실행용 코드
    consultation = GeneralConsultation()
    with gr.Blocks() as demo:
        consultation.create_interface()
    demo.launch()

