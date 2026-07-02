# 激光离子加速每日论文进展

这个项目每天自动检索 arXiv 上与激光离子加速相关的论文，做去重、关键词相关性排序，并生成中文 Markdown 日报。配置 `OPENAI_API_KEY` 后会调用 OpenAI 生成结构化摘要；未配置时会使用保守的本地摘要，不会编造摘要中没有的参数。

## 功能

- 从 arXiv API 抓取最近论文和更新
- 用关键词、学科分类和排除词进行相关性过滤
- SQLite 保存论文和摘要，避免重复处理
- 生成 `reports/YYYY/YYYY-MM-DD.md` 日报
- GitHub Actions 每天自动运行，也支持手动触发

## 本地运行

```bash
python -m pip install -e .
paper-digest --no-openai
```

如果你想调用 OpenAI 生成更高质量的结构化摘要：

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="gpt-5.5"
paper-digest
```

调试时可以只打印报告，不写入文件：

```bash
paper-digest --no-openai --dry-run --max-papers 5
```

如果只是做本地 smoke test，也可以临时跳过多关键词请求之间的等待：

```bash
paper-digest --no-openai --dry-run --max-papers 5 --lookback-days 90 --pause-seconds 0
```

## GitHub 自动化

1. 创建一个新的 GitHub 仓库，并把本项目推送上去。
2. 在仓库的 `Settings -> Secrets and variables -> Actions` 中添加：
   - `OPENAI_API_KEY`：可选；不配置也能生成保守摘要
   - `OPENAI_MODEL`：可选变量，默认 `gpt-5.5`
3. `.github/workflows/daily.yml` 已配置每日 `00:30 UTC` 运行，即北京时间 `08:30`。
4. 也可以在 GitHub Actions 页面点击 `Run workflow` 手动运行。

## 调整检索范围

编辑 `configs/queries.json`：

- `queries`：检索词
- `arxiv.categories`：arXiv 分类
- `arxiv.lookback_days`：回看天数
- `ranking.strong_terms`：强相关词
- `ranking.support_terms`：辅助相关词
- `ranking.exclude_terms`：排除无关方向
- `ranking.minimum_score`：入选阈值

建议先运行几天，人工抽查漏报和误报，再微调关键词。激光离子加速这个方向术语密集，关键词质量比模型本身更决定日报质量。

## 报告字段

每篇论文会尽量整理：

- 一句话结论
- 加速机制
- 研究类型
- 激光参数
- 靶材
- 离子种类
- 最高能量或关键结果
- 主要贡献
- 局限或注意点
- 为什么重要

如果摘要中没有对应信息，报告会写“摘要中未明确说明”。

## 注意事项

- arXiv 搜索结果通常按日更新，不需要高频请求。
- 连续检索多个关键词时，代码默认每次请求间隔 3 秒。
- 当前版本只解析标题、摘要和元数据；如果要做全文级总结，可以后续增加 PDF 下载与解析模块。
