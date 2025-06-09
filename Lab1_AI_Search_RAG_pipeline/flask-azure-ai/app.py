import os
from flask import Flask, request, render_template
from openai import AzureOpenAI
import dotenv

app = Flask(__name__)
dotenv.load_dotenv()

# Azure 설정
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OAI_KEY"),
    api_version="2024-02-01"
)

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
                messages=[{"role": "user", "content": question}],
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
            
            answer = completion.choices[0].message.content
            if show_citations:
                citations = completion.choices[0].message.context

        except Exception as e:
            answer = f"Error: {str(e)}"

    return render_template('index.html', 
                         answer=answer,
                         citations=citations,
                         question=question)

if __name__ == '__main__':
    app.run(debug=True)
