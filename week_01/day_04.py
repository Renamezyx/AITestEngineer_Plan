import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ValidationError

from llm.schemas import TestPointResult

load_dotenv()  # 先于 os.environ.get
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com"
)
prd = """
        用户使用邮箱和密码登录。
        密码错误时提示「账号或密码错误」，不泄露是邮箱错还是密码错。
        连续失败 5 次锁定 15 分钟。
        需求未提及验证码、第三方登录。
    """
system_msg = {
                "role": "system",
                "content": (
                    """
                    你是软件测试工程师，不是产品经理。\n
                    只根据用户提供的需求工作。需求没有的功能写入 unknown_gaps，禁止编造。\n
                    输出 JSON，不要 Markdown 围栏。 必须是如下结构：\n
                    {"test_points":[{"id":"TP-001","title":"..."},{"id":"TP-002","title":"..."}, ...],"unknown_gaps":[{"id":"UG-001","title":"..."},{"id":"UG-002","title":"..."}, ...]}
                    注意：
                    test_points 的 id 以 'TP-' 开头，
                    unknown_gaps 的 id 以 'UG-' 开头，
                    不要改我的命名规范
                    """
                ),
            }
user_msg = {
                "role": "user",
                "content": f"从下面需求提取测试点：\n\n{prd}",
            }
messages = [system_msg, user_msg]
last_error = None
for attempt in (1, 2):
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages,
        stream=False,
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    raw = response.choices[0].message.content
    try:
        data = json.loads(raw)
        # 故意破坏第一次 schema
        if attempt == 1:
            data["unknown_gaps"] = [i["title"] for i in data["unknown_gaps"]]
        
        # 校验数据格式严格符合要求
        result = TestPointResult.model_validate(data)
        print(result)
        sys.exit(0)
    except (json.JSONDecodeError, ValidationError) as e:
        last_error = e
        print(f"attempt={attempt} schema 失败: {e}")
        messages.append({"role": "assistant", "content": raw})
        messages.append({
            "role": "user",
            "content": f"按 schema 修正 json，错误：{e}",
        })
print("两次均未通过 schema")
sys.exit(1)