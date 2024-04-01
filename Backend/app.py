from flask import Flask
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

app=Flask(__name__)

@app.route('/',methods=['GET'])
def summarizer():
  PAPER_PATH="doc.pdf"
  reader = PdfReader(PAPER_PATH)

  print(f"Number of pages:  {len(reader.pages)}")

  parts=[]
  def visitor_body(text,cm,tm,fontDict,fontSize):
    y=tm[5]
    if y>50 and y<720:
      parts.append(text)
  for page in reader.pages:
    page.extract_text(visitor_text=visitor_body)
  text_body="".join(parts)
  print(text_body)

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

  api_key="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"
  chat =ChatOpenAI(model_name="gpt-3.5-turbo",temperature=1,openai_api_key=api_key)

  summary_chain=LLMChain(llm=chat,prompt=chat_prompt_template)
  with get_openai_callback() as cb:
    output=summary_chain.run(text_body)

  print(output)


if __name__=='__main__':
  app.run(debug=True  )