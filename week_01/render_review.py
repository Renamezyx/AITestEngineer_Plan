"""把测试点 JSON 转成可手填的 Markdown 批注表。判定列留空，由人对照 PRD 填写。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JSON = REPO_ROOT / "output" / "week01-points.json"
DEFAULT_REVIEW = REPO_ROOT / "docs" / "week01-d6-review.md"


def _cell(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def _table(items: list[dict]) -> str:
    lines = [
        "| ID | title | 判定 | 依据 |",
        "| --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(f"| {_cell(item['id'])} | {_cell(item['title'])} |  |  |")
    return "\n".join(lines)


def render_review_md(
    payload: dict,
    *,
    prd_path: str = "docs/test_prd.md",
    points_path: str = "output/week01-points.json",
    prompt_path: str = "prompts/test_points.v1.md",
) -> str:
    test_points = payload.get("test_points") or []
    unknown_gaps = payload.get("unknown_gaps") or []
    return "\n".join(
        [
            "# Week 1 Day 6 人工批注",
            "",
            f"- PRD: `{prd_path}`",
            f"- 生成结果: `{points_path}`",
            f"- Prompt: `{prompt_path}`",
            "",
            "判定只填：`对` / `错` / `幻觉` / `遗漏`。依据里引用 PRD 原句，或写「PRD 未提及」。",
            "重新跑生成会覆盖本文件，请先填完再提交。",
            "",
            "## 测试点抽检",
            "",
            _table(test_points),
            "| — | （PRD 写了但上表没有，手写内容） |  |  |",
            "",
            "## unknown_gaps（需求缺口，供对照，可不逐条打判定）",
            "",
            _table(unknown_gaps),
            "",
            "## 本轮结论",
            "",
            f"- 生成条数：test_points={len(test_points)}，unknown_gaps={len(unknown_gaps)}",
            "- 抽检 n 条：对 x / 错 y / 幻觉 z / 遗漏 w",
            "- 必须改 Prompt 的一句话：（没有就写「暂无」）",
            "",
        ]
    )


def write_review_md(payload: dict, review_path: Path | None = None) -> Path:
    path = review_path or DEFAULT_REVIEW
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_review_md(payload), encoding="utf-8")
    return path


def main() -> int:
    json_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_JSON
    review_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_REVIEW
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    out = write_review_md(payload, review_path)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
