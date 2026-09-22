# Week 2 Prompt v1 → v1.1

保留：`prompts/test_points.v1.md`、`prompts/test_cases.v1.md`  
新版：`prompts/test_points.v1.1.md`、`prompts/test_cases.v1.1.md`

依据：`evaluation/manual/week02.csv` 登录 PRD 幻觉分 4。模型把「第 5 次失败仍提示账号或密码错误」写成确定测试点，但 PRD 没写死这次的文案。

## 改了哪一句

`test_points.v1.md` Task：

- 旧：`从需求提取测试点，至少 8 条。需求没有的功能写入 unknown_gaps，禁止编造。`
- 新：`从需求提取测试点。需求没有的功能、以及需求未写死的规则与文案，写入 unknown_gaps，禁止编造。`

Constraints 新增：

- `条数随需求，禁止为凑数量编造功能或场景`
- `需求未明确的提示文案、失败计数窗口、锁定提示等，不得写成确定测试点`

`test_cases.v1.md` 同样去掉 Task 里的「至少 8 条」，并加上：`expected 只写需求已写明的结果`。

## 为什么改

「至少 8 条」和「禁止编造」打架：短 PRD 会被逼出额外场景或把猜测写成确定点。去掉硬性条数，未写死的文案进 `unknown_gaps`，才能压住这类幻觉。

脚本默认仍指向 v1。要比对时把模板路径改成 `*.v1.1.md` 即可。
