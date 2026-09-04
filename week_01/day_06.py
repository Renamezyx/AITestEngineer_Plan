import json
from pathlib import Path

from render_review import write_review_md

from llm.client import LLMClient
from llm.schemas import TestPointResult

# 脚本在 week_01/，往上一级才是仓库根
repo_root = Path(__file__).resolve().parent.parent
prd = (repo_root / "docs" / "test_prd.md").read_text(encoding="utf-8")
sys_prompt = (repo_root / "prompts" / "test_points.v1.md").read_text(encoding="utf-8")
output_dir = repo_root / "output"
output_dir.mkdir(exist_ok=True)
out_file = output_dir / "week01-points.json"

client = LLMClient()
system_msg = {
    "role": "system",
    "content": (
        sys_prompt
    ),
}
user_msg = {
    "role": "user",
    "content": f"从下面需求提取测试点：最少8条\n\n{prd}",
}
messages = [system_msg, user_msg]
result = client.complete_json(messages, schema=TestPointResult)
payload = result["content"].model_dump()
out_file.write_text(
    json.dumps(payload, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
review_path = write_review_md(payload)

print(result["usage"])
print(result["content"])
print(f"review: {review_path}")
