"""
裸调大模型 API 示例
- 不用 openai SDK，不用 LangChain，只用 requests 直接发 HTTP 请求
- 演示图片里两个关键实验：System Prompt 拆掉会怎样 / Temperature 0 vs 1
- 以 DeepSeek 为例（OpenAI 兼容接口），换 OpenAI / 通义只需改 BASE_URL 和 API_KEY
"""

import requests

# ====== 1. 在哪里做：平台与 Key ======
# DeepSeek:  https://platform.deepseek.com        -> 注册 -> API Keys -> 创建 key
# 通义千问:   https://bailian.console.aliyun.com   -> 开通百炼 -> 创建 API-KEY
# OpenAI:    https://platform.openai.com           -> 需科学上网

# BASE_URL = "https://api.deepseek.com"   # 换 OpenAI: https://api.openai.com/v1
# API_KEY = "sk-你的key"                    # 填你自己的 key

BASE_URL = "https://naturist-nanny-breeder.ngrok-free.dev/v1/chat/completions"
# BASE_URL = "http://127.0.0.1:11434/v1/chat/completions"

HEADERS = {
    # "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def call(messages, temperature=0.7):
    """裸调：直接 POST /chat/completions，没有任何封装"""
    resp = requests.post(
        f"{BASE_URL}",
        headers=HEADERS,
        json={
            "model": "deepseek-r1:32b",  # OpenAI: gpt-4o-mini; 通义: qwen-plus
            "messages": messages,
            "temperature": temperature,
        },
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    q = "用一句话解释什么是递归。"

    # ====== 实验一：System Prompt 拆掉 vs 加上 ======
    without_sys = call([{"role": "user", "content": q}])
    with_sys = call([
        {"role": "system", "content": "只能用5个字回答下面的问题。"},
        {"role": "user", "content": q},
    ])
    print("【无 System Prompt】\n", without_sys, "\n")
    print("【有 System Prompt(杠精)】\n", with_sys, "\n")

    # # ====== 实验二：Temperature 0 vs 1，同一问多跑几次看差异 ======
    # print("【Temperature=0 连问 3 次】")
    # for _ in range(3):
    #     print(
    #         " ->",
    #         call(
    #             [{"role": "user", "content": "随机给我一个水果名字。"}], temperature=0
    #         ),
    #     )
    #
    # print("【Temperature=1 连问 3 次】")
    # for _ in range(3):
    #     print(
    #         " ->",
    #         call(
    #             [{"role": "user", "content": "随机给我一个水果名字。"}], temperature=0.1
    #         ),
    #     )
