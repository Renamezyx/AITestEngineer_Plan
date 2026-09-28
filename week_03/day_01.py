import json
from pathlib import Path

from llm.client import LLMClient

repo_root = Path(__file__).resolve().parent.parent
logs = (repo_root / "docs" / "week03-fake-log.txt").read_text(encoding="utf-8")

user_prompt = (repo_root / "prompts" / "log_analyze.v1.md").read_text(encoding="utf-8")
output_dir = repo_root / "output"
output_dir.mkdir(exist_ok=True)
out_file = output_dir / "week03-log_analysis.txt"

client = LLMClient()

user_msg = {
    "role": "user",
    "content": user_prompt.replace("{{log}}", logs),
}
messages = [user_msg]
result = client.complete_text(messages)
payload = result["content"]
if hasattr(payload, "model_dump"):
    payload = payload.model_dump()
payload = json.loads(payload)
out_file.write_text(
    json.dumps(payload, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print(result["usage"])
print(result["content"])
