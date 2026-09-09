import json
from pathlib import Path

from llm.client import LLMClient

repo_root = Path(__file__).resolve().parent.parent
bug_info = json.loads(
    (repo_root / "docs" / "week-02-test_bug_haslog.json").read_text(encoding="utf-8")
)
user_prompt = (repo_root / "prompts" / "bug_analyze.v1.md").read_text(encoding="utf-8")
output_dir = repo_root / "output"
output_dir.mkdir(exist_ok=True)
out_file = output_dir / "week02-bug_for_haslog_analysis.txt"

client = LLMClient()

user_msg = {
    "role": "user",
    "content": user_prompt.replace("{{description}}", bug_info["description"]).replace("{{environment}}", bug_info["environment"]).replace("{{log_slice}}", bug_info["log_slice"]),
}
messages = [user_msg]
result = client.complete_text(messages)
payload = result["content"]
if hasattr(payload, "model_dump"):
    payload = payload.model_dump()
out_file.write_text(
    json.dumps(payload, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print(result["usage"])
print(result["content"])
