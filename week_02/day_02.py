import json
from pathlib import Path

from llm.client import LLMClient
from llm.schemas import TestCasesInfo
from render_review import write_review_md

repo_root = Path(__file__).resolve().parent.parent
prd = (repo_root / "docs" / "test_prd.md").read_text(encoding="utf-8")
user_prompt = (repo_root / "prompts" / "test_cases.v1.md").read_text(encoding="utf-8")
output_dir = repo_root / "output"
output_dir.mkdir(exist_ok=True)
out_file = output_dir / "week01-case-v1.json"

client = LLMClient()

user_msg = {
    "role": "user",
    "content": user_prompt.replace("{{prd}}", prd),
}
messages = [user_msg]
result = client.complete_json(messages, schema=TestCasesInfo)
payload = result["content"].model_dump()
out_file.write_text(
    json.dumps(payload, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
review_path = write_review_md(
    payload, repo_root / "docs" / "week02-d2-review.md"
)

print(result["usage"])
print(result["content"])
print(f"review: {review_path}")
