from flask import Flask,request
import os
import requests
from pypdf import PdfReader
import tiktoken
from langchain.prompts import(
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import(
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
from flask_cors import CORS
import json

app=Flask(__name__)
CORS(app) 

with open('api.json', 'r') as f:
    api_key = json.load(f)

f.close()
api_key=api_key['api_key']
print(api_key)

@app.route('/',methods=['GET'])
def summarizer(file):
  PAPER_PATH="doc.pdf"
  reader = PdfReader(file)

  print(f"Number of pages:  {len(reader.pages)}")

  parts=[]
  def visitor_body(text,cm,tm,fontDict,fontSize):
    y=tm[5]
    if y>50 and y<720:
      parts.append(text)
  for page in reader.pages:
    page.extract_text(visitor_text=visitor_body)
  text_body="".join(parts)
  # print(text_body)

  def num_tokens_from_string(string: str,encoding_name:str) -> int:
    """Returns the number of tokens in a text string."""
    encoding=tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens=len(encoding.encode(string))
    return num_tokens
  num_tokens=num_tokens_from_string(text_body,"gpt-3.5-turbo")
  print(num_tokens)

  context_template="You are a helpful AI Resarcher that specializes in analyzing ML,AI and LLM papers.\
  Please use all your expertise to approach this task. Output your content in markdown format and include titles where relevant"

  system_message_prompt=SystemMessagePromptTemplate.from_template(context_template)

  system_message_prompt

  human_template = "Please summarize this paper focusing on the key important takeaways for each section. \
  Expand the summary on methods so they can be clearly understood. \n\n PAPER: \n\n{paper_content}"

  human_message_prompt=HumanMessagePromptTemplate(
      prompt=PromptTemplate(
          template=human_template,
          input_variables=["Paper Content"]
      )
  )

  chat_prompt_template =ChatPromptTemplate.from_messages([system_message_prompt,human_message_prompt])

  
  chat =ChatOpenAI(model_name="gpt-3.5-turbo",temperature=1,openai_api_key=api_key)

  summary_chain=LLMChain(llm=chat,prompt=chat_prompt_template)
  with get_openai_callback() as cb:
    output=summary_chain.run(text_body)

  return output


@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    data=summarizer(file)
    return data

if __name__=='__main__':
  app.run(debug=True)