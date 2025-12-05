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
llm = ChatOpenAI(
    temperature=0,
    model_name="openai/gpt-4.1",  # OpenRouter에서 제공하는 GPT-4.1 모델
    api_key=os.getenv("OPENROUTER_API_KEY"),  # OpenRouter API 키
    base_url=os.getenv("OPENROUTER_BASE_URL"),  # OpenRouter API URL
)

chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "너는 영화 전문가 AI야. 사용자가 원하는 장르의 영화를 리스트 형태로 추천해줘."
                'ex) Query: "SF 영화 3개 추천해줘" / 답변: ["인터스텔라", "스페이스 오디세이", "혹성탈출"]'
            )
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)

print("\n" + "#" * 50 + "\n")

messages = chat_template.format_messages(text="코미디 영화 3개 추천해줘")
response = llm.invoke(messages)
print("Raw LLM Output:", response.content)
print("\n" + "#" * 50 + "\n")
########################################################
print("\n" + "#" * 50 + "\n")






## 아래부터 Output Parser 예제 ##
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate

output_parser = CommaSeparatedListOutputParser()
format_instructions = output_parser.get_format_instructions()

# format_instructions 출력 예시
# print("Format Instructions:",format_instructions)
# Format Instructions: Your response should be a list of comma separated values, eg: `foo, bar, baz` or `foo,bar,baz`

prompt_csv = PromptTemplate(
    template="List {number} {subject}. answer in Korean \n{format_instructions}",
    input_variables=["number", "subject"],
    partial_variables={"format_instructions": format_instructions}
)

chain_csv = prompt_csv | llm | output_parser

result_csv = chain_csv.invoke({"number": 3, "subject": "액션 영화"})
print("CSV parser Output:", result_csv)
########################################################
print("\n" + "#" * 50 + "\n")







## Datetime Output Parser 예제 ##
from langchain.output_parsers import DatetimeOutputParser
from langchain.prompts import PromptTemplate

output_parser = DatetimeOutputParser()
format_instructions = output_parser.get_format_instructions()

# format_instructions 출력 예시
# print("Format Instructions:",format_instructions)

# Format Instructions: Write a datetime string that matches the following pattern: '%Y-%m-%dT%H:%M:%S.%fZ'.
# Examples: 2023-07-04T14:30:00.000000Z, 1999-12-31T23:59:59.999999Z, 2025-01-01T00:00:00.000000Z

template = """
    Answer the user question:
    {question}
    {format_instructions}
    """

prompt = PromptTemplate.from_template(
    template,
    # input_variables=["question"],
    partial_variables={"format_instructions": format_instructions},
)

chain = prompt | llm | output_parser
ouput = chain.invoke({"question":"비트코인은 언제 개발되었지?"})
print("Datetime parser Output:", ouput)
print("\n" + "#" * 50 + "\n")

########################################################

