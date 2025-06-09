import os
from flask import Flask, request, render_template
from openai import AzureOpenAI
import dotenv
import markdown
import re

app = Flask(__name__)
dotenv.load_dotenv()

# Azure 설정
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OAI_KEY"),
    api_version="2024-02-01"
)

def process_markdown_content(content):
    """마크다운 콘텐츠를 HTML로 변환하고 스타일을 개선"""
    if not content:
        return content
    
    # 마크다운을 HTML로 변환
    html_content = markdown.markdown(content, extensions=['extra', 'codehilite'])
    
    # 추가적인 스타일링을 위한 클래스 추가
    html_content = re.sub(r'<h1>', '<h1 class="md-h1">', html_content)
    html_content = re.sub(r'<h2>', '<h2 class="md-h2">', html_content)
    html_content = re.sub(r'<h3>', '<h3 class="md-h3">', html_content)
    html_content = re.sub(r'<p>', '<p class="md-p">', html_content)
    html_content = re.sub(r'<ul>', '<ul class="md-ul">', html_content)
    html_content = re.sub(r'<ol>', '<ol class="md-ol">', html_content)
    html_content = re.sub(r'<li>', '<li class="md-li">', html_content)
    html_content = re.sub(r'<code>', '<code class="md-code">', html_content)
    html_content = re.sub(r'<pre>', '<pre class="md-pre">', html_content)
    
    return html_content

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    citations = None
    question = ""
    
    if request.method == 'POST':
        question = request.form['question']
        show_citations = 'show_citations' in request.form
        
        try:
            completion = client.chat.completions.create(
                model=os.getenv("AZURE_OAI_DEPLOYMENT"),
                messages=[{
                    "role": "system", 
                    "content": "당신은 도움이 되는 AI 어시스턴트입니다. 답변은 마크다운 형식으로 작성해주세요. 제목, 부제목, 목록, 코드 블록 등을 적절히 사용하여 읽기 쉽게 구성해주세요."
                }, {
                    "role": "user", 
                    "content": question
                }],
                extra_body={
                    "data_sources": [{
                        "type": "azure_search",
                        "parameters": {
                            "endpoint": os.environ["AZURE_SEARCH_ENDPOINT"],
                            "index_name": os.environ["AZURE_SEARCH_INDEX"],
                            "authentication": {
                                "type": "api_key",
                                "key": os.environ["AZURE_SEARCH_KEY"]
                            }
                        }
                    }]
                }
            )
            
            # 마크다운 콘텐츠 처리
            raw_answer = completion.choices[0].message.content
            answer = process_markdown_content(raw_answer)
            
            if show_citations:
                citations = completion.choices[0].message.context
                
        except Exception as e:
            answer = f"<p class='error'>오류가 발생했습니다: {str(e)}</p>"
    
    return render_template('index.html',
                         answer=answer,
                         citations=citations,
                         question=question)

if __name__ == '__main__':
    app.run(debug=True)
