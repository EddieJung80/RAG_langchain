import os

# API KEY를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv
# API KEY 정보로드
load_dotenv(override=True)

from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# ChatOpenAI 객체 생성
chat = ChatOpenAI(
    temperature=0.1,
    model_name="openai/gpt-4.1",  # OpenRouter에서 제공하는 GPT-4.1 모델
    api_key=os.getenv("OPENROUTER_API_KEY"),  # OpenRouter API 키
    base_url=os.getenv("OPENROUTER_BASE_URL"),  # OpenRouter API URL
)

# 챗 프롬프트 템플릿 정의
chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "당신은 공부 계획을 세워주는 스터디 플래너 머신입니다."
                "사용자가 제공한 정보를 바탕으로 효과적인 공부 계획을 세워주세요."
            )
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)

# 사용자 입력에 따른 메시지 생성
messages = chat_template.format_messages(text="저는 이번 학기에 인공지능, 데이터 과학, 그리고 프로그래밍을 공부하고 싶습니다.")


# 스트리밍 모드로 챗봇 응답 받기
for chunk in chat.stream(messages):
    print(chunk.content, end="", flush=True)  # 스트리밍된 응답 출력




# ############### 아래는 마크다운 렌더링을 위한 추가 코드 ###############

# from rich.console import Console
# from rich.markdown import Markdown

# # Rich 콘솔 객체 생성

# console = Console()
# full_response = "" # 전체 응답을 저장할 변수

# console.print("\n[bold blue]--- 모델 응답 (스트리밍 시작) ---[/bold blue]")

# # # 스트리밍 모드로 챗봇 응답 받기 (LangChain의 chat.stream() 가정)
# # 'chat' 및 'messages' 객체는 이미 준비되어 있다고 가정합니다.
# for chunk in chat.stream(messages):
#     # 1. 스트리밍되는 조각을 실시간으로 터미널에 출력
#     if chunk.content:
#         print(chunk.content, end="", flush=True)
#         # 2. 전체 응답 변수에 조각을 누적
#         full_response += chunk.content

# # 3. 스트리밍 종료 후 줄바꿈
# print("\n")

# # 4. 전체 응답에 대해 마크다운 렌더링 적용 및 출력
# if full_response:
#     console.print("\n[bold blue]--- 최종 응답 (마크다운 렌더링) ---[/bold blue]")
    
#     # 마크다운 객체 생성
#     md = Markdown(full_response.strip())
    
#     # Rich를 사용하여 최종 마크다운을 예쁘게 출력
#     console.print(md)

# console.print("\n[bold yellow]--- 요청 종료 ---[/bold yellow]")