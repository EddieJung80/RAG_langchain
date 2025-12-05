import os

# API KEY를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv
# API KEY 정보로드
load_dotenv(override=True)

from langchain.prompts import HumanMessagePromptTemplate, PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

# ChatOpenAI 객체 생성
chat = ChatOpenAI(
    temperature=0.8,
    model_name="openai/gpt-4.1",  # OpenRouter에서 제공하는 GPT-4.1 모델
    api_key=os.getenv("OPENROUTER_API_KEY"),  # OpenRouter API 키
    base_url=os.getenv("OPENROUTER_BASE_URL"),  # OpenRouter API URL
)

prompt = (
    """
    너는 요리사야. 사용자가 제공한 재료들로 만들 수 있는 요리를 {개수}개 추천하고,
    그 요리의 레시피를 제시해줘. 내가 가진 재료는 다음과 같아: {재료}
    """
)

# print(prompt.format(개수=3, 재료="닭고기, 감자, 당근, 양파"))

response = chat.invoke(prompt.format(개수=3, 재료="닭고기, 감자, 당근, 양파"))

print(response.content)

########################################################
print("\n" + "#" * 50 + "\n")
# 부분 프롬프트 템플릿과 동적 값 삽입 예제
from datetime import datetime

def _get_datetime():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
prompt_time = PromptTemplate(
    template="{시간}에 맞는 {부사}한 농담을 알려줘.",
    input_variables=["시간", "부사"]
)

partial_prompt = prompt_time.partial(부사="재미있는")  
formatted_prompt = partial_prompt.format(시간=_get_datetime())

respose_time = chat.invoke(formatted_prompt)
print(respose_time.content)

