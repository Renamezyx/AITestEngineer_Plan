import json
import os

from dotenv import load_dotenv
from openai import OpenAI

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
response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {
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
        },
        {
            "role": "user",
            "content": f"从下面需求提取测试点：\n\n{prd}",
        },
    ],
    stream=False,
    response_format={"type": "json_object"},
    temperature=0.2,
)
row = response.choices[0].message.content
data = json.loads(row)
# 校验数据格式严格符合要求
result = TestPointResult.model_validate(data)
print(result)
