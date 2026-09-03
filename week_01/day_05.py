from llm.client import LLMClient
from llm.schemas import TestPointResult

client = LLMClient()
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
result = client.complete_json(messages, schema=TestPointResult)
print(result["usage"])
print(result["content"])