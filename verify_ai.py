from openai import OpenAI
import os
import sys


def main() -> None:
    api_key = os.getenv("AI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("未设置 AI_API_KEY/OPENAI_API_KEY，已退出。")
        sys.exit(1)

    base_url = os.getenv("AI_BASE_URL") or os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1"
    model = os.getenv("AI_MODEL", "gpt-5.2-codex")

    client = OpenAI(api_key=api_key, base_url=base_url)

    print("正在测试 AI API 连接...")
    print(f"Base URL: {client.base_url}")
    print(f"Model: {model}")
    print("-" * 30)

    try:
        print("尝试调用 responses.create 接口...")
        resp = client.responses.create(
            model=model,
            input="hello",
        )
        print("✓ responses.create 调用成功!")
        print(f"回复内容: {resp.output_text}")
        return
    except Exception as e1:
        print(f"✗ responses.create 调用失败: {e1}")

    try:
        print("\n尝试调用 chat.completions 接口...")
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "hello"}],
        )
        print("✓ chat.completions 调用成功!")
        print(f"回复内容: {resp.choices[0].message.content}")
    except Exception as e2:
        print(f"✗ chat.completions 调用失败: {e2}")
        print("\n所有尝试均失败，请检查 API 配置或网络连接。")


if __name__ == "__main__":
    main()
