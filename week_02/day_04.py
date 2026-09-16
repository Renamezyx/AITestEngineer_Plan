import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from llm.client import LLMClient
from llm.schemas import TestCasesInfo
from prompts.render import render_prompt

repo_root = Path(__file__).resolve().parent.parent
prd = (repo_root / "docs" / "test_prd.md").read_text(encoding="utf-8")
user_prompt = (repo_root / "prompts" / "test_cases.v1.md").read_text(encoding="utf-8")
output_dir = repo_root / "output"
(output_dir / "debug").mkdir(exist_ok=True)
out_prompt_file = output_dir / "debug" /"week02-day04-test_cases.prompt.md"

render_1 = render_prompt(user_prompt, {"prd": prd}),
render_2 = render_prompt(user_prompt, {"prd": prd}),
assert render_1 == render_2, "render_prompt 结果不一致"

out_prompt_file.write_text(
    json.dumps(render_2, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
