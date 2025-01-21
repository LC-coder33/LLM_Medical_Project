#!/usr/bin/env python
# coding: utf-8

# In[1]:


import gradio as gr
import requests
import plotly.graph_objects as go
from config import OPENFDA_API_KEY, OPENFDA_API_URL


# In[7]:


class DrugInfo:
    def __init__(self):
        """의약품 정보 모듈 초기화"""
        self.api_key = OPENFDA_API_KEY
        
    def visualize_side_effects(self, drug_name: str):
        """부작용 데이터 시각화"""
        try:
            if not drug_name.strip():
                return None
                
            # OpenFDA에서 부작용 데이터 가져오기
            url = f"{OPENFDA_API_URL}event.json"
            params = {
                "api_key": self.api_key,
                "search": f"patient.drug.medicinalproduct:{drug_name}",
                "count": "patient.reaction.reactionmeddrapt.exact",
                "limit": 10  # 상위 10개 부작용만 가져오기
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if "results" not in data or not data["results"]:
                return go.Figure().add_annotation(
                    text="데이터를 찾을 수 없습니다.",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, showarrow=False
                )
                
            # 상위 10개 부작용 추출
            effects = [(item["term"], item["count"]) 
                      for item in data["results"]]
            
            # Plotly로 바 차트 생성
            fig = go.Figure([
                go.Bar(
                    x=[count for _, count in effects],
                    y=[term for term, _ in effects],
                    orientation='h',
                    marker_color='indianred'
                )
            ])
            
            fig.update_layout(
                title=f"{drug_name}의 주요 부작용 보고 현황",
                xaxis_title="보고 건수",
                yaxis_title="부작용",
                height=600,
                font=dict(size=12),
                margin=dict(l=200)  # 긴 부작용 이름을 위한 여백
            )
            
            return fig
            
        except Exception as e:
            print(f"부작용 데이터 시각화 오류: {e}")
            return go.Figure().add_annotation(
                text="데이터를 가져오는 중 오류가 발생했습니다.",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
    
    def create_interface(self) -> None:
        """Gradio 인터페이스 생성"""
        with gr.Blocks() as interface:
            gr.Markdown("""
                ## 의약품 부작용 통계
                영문 약물명을 입력하면 해당 약물의 주요 부작용 통계를 보여줍니다.
                
                예시 약물명:
                - aspirin
                - ibuprofen
                - acetaminophen
                - omeprazole
                - metformin
            """)
            
            with gr.Row():
                drug_name_input = gr.Textbox(
                    label="약물명 입력",
                    placeholder="영문 약물명을 입력하세요 (예: aspirin)",
                    scale=2
                )
                search_button = gr.Button(
                    "부작용 통계 검색",
                    scale=1
                )
            
            plot_output = gr.Plot(label="부작용 통계")
            
            search_button.click(
                fn=self.visualize_side_effects,
                inputs=drug_name_input,
                outputs=plot_output
            )


# In[8]:


if __name__ == "__main__":
    # 모듈 단독 실행용 코드
    drug_info = DrugInfo()
    with gr.Blocks() as demo:
        drug_info.create_interface()
    demo.launch()
