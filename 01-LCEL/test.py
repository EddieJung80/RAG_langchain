import requests
import json
import time
from rich.console import Console
from rich.markdown import Markdown


# 나노초(ns)를 초(s)로 변환하는 상수
NS_TO_S = 1_000_000_000

# 1. 설정 정의
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "exaone3.5:7.8b"
PROMPT = "우주의 생성과정에 대해서 순차적으로 설명해봐"
# PROMPT = input("모델에게 질문할 내용을 입력하세요: ") #사용자 입력 프롬프트

# 2. 요청 데이터(Payload) 구성
payload = {
    "model": MODEL_NAME,
    "prompt": PROMPT,
    "stream": False 
}

# Rich 콘솔 객체 생성, 마크다운 출력 준비
console = Console()
console.print("\n[bold yellow]--- Ollama API 요청 시작 ---[/bold yellow]")
console.print(f"[green]모델:[/green] {MODEL_NAME}")
console.print(f"[green]프롬프트:[/green] {PROMPT}\n")

print("-" * 70)
print(f"{MODEL_NAME} 모델 응답:")

try:
    # 3. POST 요청 전송
    response = requests.post(OLLAMA_API_URL, json=payload)

    # 4. 응답 확인 및 파싱
    if response.status_code == 200:
        data = response.json()
        
        # --- 모델 응답 출력 ---
        if 'response' in data:
            
            # print(data['response'].strip()) # 기존 출력 방식

            # Rich 라이브러리를 사용한 마크다운 형식 출력
            model_output = data['response'].strip()
            md = Markdown(model_output) # Markdown 객체 생성
            console.print(md) # Rich 콘솔에 출력
        
        # --- 5. 상세 리소스 사용량 및 성능 지표 (이전 섹션) ---
        
        print("\n" + "=" * 70)
        print("🚀 모델 리소스 사용량 및 성능 지표")
        print("=" * 70)
        
        # 5-1. 토큰 사용량
        prompt_tokens = data.get('prompt_eval_count', 0)
        output_tokens = data.get('eval_count', 0)
        
        # 5-2. 소요 시간 (나노초 -> 초 변환)
        total_duration = data.get('total_duration', 0) / NS_TO_S
        prompt_eval_duration = data.get('prompt_eval_duration', 0) / NS_TO_S
        eval_duration = data.get('eval_duration', 0) / NS_TO_S

        # 5-3. 속도 (토큰/초 계산)
        if eval_duration > 0 and output_tokens > 0:
            eval_rate = output_tokens / eval_duration
        else:
            eval_rate = 0.0
        
        # 6. 결과 표 형식 출력 (주요 지표)
        print(f"{'지표':<35}{'값':>35}")
        print("-" * 70)
        
        # 토큰 정보
        print(f"{'1. 입력 토큰 수 (Prompt Tokens)':<35}{prompt_tokens:>35,} 토큰")
        print(f"{'2. 출력 토큰 수 (Output Tokens)':<35}{output_tokens:>35,} 토큰")
        print("-" * 70)
        
        # 시간 및 속도 정보
        print(f"{'3. 총 요청 소요 시간 (Total)':<35}{total_duration:>34.3f} 초")
        print(f"{'4. 응답 생성 속도 (Tokens/Sec)':<35}{eval_rate:>34.2f} t/s")
        print("-" * 70)
        
        #########################################################
        # # --- 7. 응답 JSON의 모든 항목 출력 (추가된 섹션) ---
        
        # print("\n" + "=" * 70)
        # print("🔍 Ollama 응답 JSON 전체 항목 (Key: Value)")
        # print("=" * 70)
        
        # # JSON 응답의 모든 Key-Value 쌍을 반복하여 출력
        # # 응답이 크면 많은 정보가 출력될 수 있습니다.
        # for key, value in data.items():
        #     # 'response' 키는 이미 앞에서 출력했으므로 제외하거나 간략하게 출력
        #     if key == 'response':
        #         print(f"{key:<35} : (답변 텍스트, 위에서 출력됨)")
        #     elif key.endswith('_duration') or key.endswith('_count'):
        #          # duration 값은 나노초로 너무 길기 때문에 초(s)로 변환하여 출력
        #         if key.endswith('_duration'):
        #             time_in_s = value / NS_TO_S
        #             print(f"{key:<35} : {time_in_s:.6f} 초")
        #         else:
        #             print(f"{key:<35} : {value:,}")
        #     else:
        #         print(f"{key:<35} : {value}")

        # print("=" * 70)
        ##########################################################

    else:
        # 요청 실패 시 오류 메시지를 출력합니다.
        print(f"API 요청 실패. 상태 코드: {response.status_code}")
        print(f"에러 메시지: {response.text}")

except requests.exceptions.ConnectionError:
    print("\n[오류 발생] Ollama 서버에 연결할 수 없습니다.")
    print("Ollama 서버(http://localhost:11434)가 켜져 있는지 확인해 주세요.")
except Exception as e:
    print(f"\n[예기치 않은 오류] {e}")