import json
from pathlib import Path

from llm.client import LLMClient
from llm.schemas import TestPointResult
from render_review import write_review_md

repo_root = Path(__file__).resolve().parent.parent
prd = (repo_root / "docs" / "test_prd.md").read_text(encoding="utf-8")
user_prompt = (repo_root / "prompts" / "test_points.v1.md").read_text(encoding="utf-8")
output_dir = repo_root / "output"
output_dir.mkdir(exist_ok=True)
out_file = output_dir / "week01-points.json"

client = LLMClient()

user_msg = {
    "role": "user",
    "content": user_prompt.replace("{{prd}}", prd),
}
messages = [user_msg]
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
