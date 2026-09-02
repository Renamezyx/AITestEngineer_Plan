import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # 先于 os.environ.get
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com"
)
prd = """用户使用邮箱和密码登录。
密码错误时提示「账号或密码错误」，不泄露是邮箱错还是密码错。
连续失败 5 次锁定 15 分钟。
需求未提及验证码、第三方登录。"""
for temperature in [0.1, 0.8]:
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是软件测试工程师，不是产品经理。\n"
                    "只根据用户提供的需求工作。需求没有的功能写入 unknown_gaps，禁止编造。\n"
                    "输出 JSON，不要 Markdown 围栏。"
                ),
            },
            {
                "role": "user",
                "content": f"固定 JSON 字段名（只要 id, title)，从下面需求提取测试点：\n\n{prd}",
            },
        ],
        stream=False,
        temperature = temperature
    )
    print(response.choices[0].message.content)

"""
此脚本的作用是：验证 DeepSeek 的测试生成能力 0.1 和 0.8 的温度对比
结论： 
用低温度，是为了少跳一点（少换壳、少加 14 分钟这种精度、少一会儿 9 条一会儿 6 条），方便人审和以后对黄金集。
低温度不是答案。 0.1 两次照样换数组/对象、照样编「成功登录打断连续失败」。
可回归不能靠温度，要靠固定 JSON 示例 + 程序校验（Pydantic），未写明的规则强制进 unknown_gaps。

个人感觉：0.8温度下 测试生成更加全面 但是不可控 容易让ai自己编造一些case（虽然这些case大多存在）
过程见：/docs/week01-temp-compare.md
"""