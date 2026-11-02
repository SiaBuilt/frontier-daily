# Frontier 早报 · 生成与发布规范

定时任务每次运行都会先读这份文件。想改规则，直接改这里即可。

## 0. 位置
- 仓库：`~/Desktop/Cowork/PLAYGROUND/frontier-daily`（GitHub `Charleyxx1209/frontier-daily`，分支 main，GitHub Pages）
- 线上：https://frontier.siabuilt.com
- 只改 `briefs/YYYY-MM-DD.json`、`briefs/index.json`，必要时改 `pulse.json`、`revenue.json`。不动 index.html 等其他文件。
- 提交身份：`git -c user.name="Charleyxx1209" -c user.email="chengxi1209@gmail.com"`，提交信息用中文，如「新增 2026-10-28 早报」；由 Codex 执行，不添加 Claude 署名。

## 1. 取材（日期 = 运行当天，北京时间）
1. X 上的 builder：下载 https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-x.json（过去 24 小时推文）。
2. 播客：同仓库 `feed-podcasts.json`（含文字稿）；`feed-blogs.json`。另外逐个检查这些播客 7 天内有无新集（官网或 YouTube 频道，浏览与搜索工具），有就读简介和能拿到的文字稿：
   - Acquired（https://www.acquired.fm）
   - All-In（https://allin.com）、BG2、Dwarkesh Podcast、No Priors、Training Data、Unsupervised Learning、The MAD Podcast、Latent Space、AI & I、Lenny's Podcast
3. 一手长文：用浏览工具检查 36 小时内有无新文：simonwillison.net、oneusefulthing.org、interconnects.ai、importai.substack.com、hamel.dev、eugeneyan.com、newsletter.semianalysis.com、lennysnewsletter.com、latent.space、dwarkesh.com。
4. 官方一手：anthropic.com/news、anthropic.com/engineering、openai.com/news、deepmind.google/blog；必要时 WebSearch 核实当天大事件。
5. 去重：读前一期 brief，已收录过的 url 不再收。
6. 抓不到的源如实写进 stats 的「失败的源」，不要编造。

## 2. 选材
- 只要和 AI / 产品 / 算力 / 资本相关、有信息量的；闲聊、纯转发、玩笑、广告不收。
- 一般 10 到 16 条。分三栏：`x`「Builders 在说什么」、`pod`「一手长文与播客」、`industry`「典型事实」。
- 事实类（发布、财报、融资、监管）优先用官方一手来源，媒体报道注明「报道」且写清未确认。

## 3. JSON 结构
```
{
 "date": "YYYY-MM-DD",
 "generatedAt": "ISO 时间 +08:00",
 "headline": "一句话总结今天，≤40 字",
 "themes": ["主题 1", "主题 2", "主题 3"],
 "stats": "X：N 位 builder · N 条 ｜ 一手长文：… ｜ 播客：… ｜ 事实新闻：N 条（来源）｜ 失败的源：…",
 "sections": [{"id":"x","title":"Builders 在说什么","items":[…]}, {"id":"pod","title":"一手长文与播客","items":[…]}, {"id":"industry","title":"典型事实","items":[…]}],
 "question": "留给读者的一个问题"
}
```
每个 item：
- `id`：x1…、p1…、i1…
- `who`：「姓名，身份」，如「Aaron Levie，Box CEO」。页面显示姓名 + 身份 + 头像（头像按 X 账号自动匹配 Builders 名单）。身份要短，≤12 字。
- `tag`：2–4 字主题
- `url`：原文链接；`sourceLabel`：如「X @levie」「simonwillison.net」「Anthropic 官方公告」
- `title`：中文标题，具体，带数字更好
- `summary`：中文 1–2 句，≤90 字，第三人称概括
- `ctx`（必填）：一句背景，≤40 字，交代「这条是在回应什么 / 由什么引发」：哪件事、哪份文件、哪篇文章、哪次发布。读者不看原文也要知道来龙去脉。查不到背景的推文宁可不收。
- `quote`：**英文原话，必须逐字摘自原文**，不得改写或编造；没有合适原话就留空字符串
- `quoteZh`：quote 的中文翻译
- `gist`（有 quote 的条目必填）：一段完整的论证，2–4 句，≤120 字，按「结论 → 依据 → 所以呢」写，不要罗列数字碎片。**不用第三人称**（不写「他说」「他认为」），直接陈述观点本身。只保留支撑结论的 1–2 个关键数字，专有名词第一次出现时用几个字解释它是什么。
- `weight`：1–3。3 = 当天头等大事（最多 2 条）；2 = 值得想一想；1 = 一般信息。
- `soWhat`：只在 weight ≥ 2 时写，一句话点出启发或影响，克制、不鸡汤；weight 1 不写这个字段。

## 4. 顶栏数据（revenue.json、pulse.json）
- 顶栏显示 Anthropic、OpenAI 年化营收和 OpenRouter 周 token 量。
- 只有拿到一手可核实的新数字（官方公告、财报 / S-1、OpenRouter Rankings 页面）才追加新数据点，不要估算。
- 追加的点加上 `"addedAt": "<今天日期>"`，页面会在这一期的顶栏上标「更新」。

## 5. 发布
1. `git pull`，写入 `briefs/<date>.json`；在 `briefs/index.json` 头部插入 `{"date","headline","count"}`（count = 条目总数，同日期则替换）。
2. 用 python 校验所有改动的 JSON 都能解析，且每个 quote 非空的条目都有 quoteZh、gist 和 ctx。
3. 提交、推送到 origin main。
4. 等 1–2 分钟，`curl https://frontier.siabuilt.com/briefs/index.json` 确认第一条是今天。
5. 如果当天已存在该日期的 brief，不要覆盖，直接结束并说明。


## 6. Codex 执行约定
- 每日北京时间 07:41 在本聊天运行，由 Codex 自动生成并发布；时间来自现有页面出刊提示。电脑需开机，Codex 应用需保持运行。
- 先确认当前目录和 origin，执行 `git status --short`；工作区有未提交改动时停止发布并报告，不覆盖、暂存或提交用户改动。干净时 `git pull --ff-only`；冲突或拉取失败则停止。
- 读取本规范、最新一期及最近 7 期去重。按 Asia/Shanghai 计算当天日期，generatedAt 写真实完成时间，不预填固定时间。
- 已有当天文件则不覆盖；仍检查线上当天文件与本地是否一致。若此前已提交但未推送，只在确认差异全部属于当天早报且校验通过后重试推送；其他差异报告处理。
- feed 是发现线索的入口。检查 generatedAt 和每条发布日期；过期内容不可当成当天新消息。无法独立核对的转述要明确标注，未检查与抓取失败分别记录。
- 逐字核对引文并遵守来源引用长度限制；优先短引文，其余用中文概括。背景不得推测补全；没有可靠材料可以少于 10 条，不凑数。完全无可核实内容时不创建空早报。
- 先写好日报，再更新索引；运行 `python3 scripts/validate_briefs.py --date YYYY-MM-DD` 和 `git diff --check`。校验通过才能提交。
- 只 stage 当天 JSON、索引及确有一手新数字的 pulse/revenue 文件，禁止 `git add .`。推送前再 fetch；远程前进则停止并报告，禁止 force push。
- 仅提交数据文件至 origin main。使用现有 Git 认证，不迁移 Claude 凭据或权限设置。
- 发布后每隔 30 秒检查线上 index 和当天 JSON，最多 4 次；必须与本地解析后内容一致才报告上线成功，否则写清“已推送，线上未验证”。
- 在本聊天汇报日期、标题、条数、最多两条头条、来源缺口、提交及线上验证结果和链接。当天已发布且内容一致时保持安静；失败或需用户处理时报告具体阻碍。不调用 Claude PushNotification，不向邮件或其他聊天发送消息。
