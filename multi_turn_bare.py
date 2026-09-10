# 多轮对话裸调：看上下文窗口怎么被吃掉的
# - 依然只用 requests，不用任何 SDK
# - 关键：模型无记忆，每轮请求都要把整段历史 messages 重发一遍
# - 用 API 返回的 usage.prompt_tokens 观察"上下文"逐轮变大（这是真实 token 数）
# - 超过设定阈值时，手动丢弃最早消息 -> 演示"失忆"机制


import requests

BASE_URL = "https://naturist-nanny-breeder.ngrok-free.dev"          # OpenAI: https://api.openai.com/v1
# API_KEY = "sk-你的key"                           # 填你自己的 key
HEADERS = {
    # "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

MODEL_WINDOW = 64000      # deepseek-chat 真实上下文窗口约 64K
DEMO_TRUNCATE_AT = 1500   # 演示用：超过这个就丢最早消息，提前看失忆效果


def call(messages):
    """裸调，返回 (回复文本, prompt_tokens)。prompt_tokens 就是这轮送进去的上下文大小"""
    resp = requests.post(
        f"{BASE_URL}/v1/chat/completions",
        headers=HEADERS,
        json={"model": "deepseek-r1:32b", "messages": messages},
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"], data["usage"]["prompt_tokens"]


def bar(now, total, width=28):
    filled = int(width * now / total)
    return "[" + "█" * filled + "░" * (width - filled) + f"] {now}/{total} tok"


if __name__ == "__main__":
    # 一段会越聊越长的对话（每轮内容都比上一轮长，prompt_tokens 涨得更快）
    conversation = [
        "用 100 字介绍一下 Python 装饰器",
        "再展开讲讲闭包和装饰器的关系，要详细点",
        "给三个有实际意义的装饰器例子并逐行解释",
        "把这些整合成一个带参数的装饰器，输出完整代码并注释",
        "最后总结装饰器适合用在哪些场景，列要点说明",
    ]

    messages = [{"role": "system", "content": "你是一个耐心的 Python 老师。"}]

    for i, user_input in enumerate(conversation, 1):
        messages.append({"role": "user", "content": user_input})
        reply, prompt_tok = call(messages)          # 整段历史重发 -> prompt_tok 逐轮变大
        messages.append({"role": "assistant", "content": reply})

        print(f"第{i}轮  prompt_tokens={prompt_tok:<6} {bar(prompt_tok, MODEL_WINDOW)}")

        # 演示截断：超过阈值就丢最早的(非 system)消息，下一轮模型就"忘了"它
        if prompt_tok > DEMO_TRUNCATE_AT:
            for m in messages:
                if m["role"] != "system":
                    print(f"   -> 超过 {DEMO_TRUNCATE_AT}，丢弃最早消息: {m['content'][:24]}...")
                    messages.remove(m)
                    break

    print("\n关键：每轮 prompt_tokens 都比上一轮大 -> 上下文就是这样被吃掉的")
    print("真实撞到模型窗口(64K)时，要么报错，要么厂商自动截断最早消息 = 失忆")
    print("对策：自己维护 messages，快到上限时主动删旧消息/做摘要，别等它丢")
