# Frontier 早报 · 生成与发布规范

定时任务每次运行都会先读这份文件。想改规则，直接改这里即可。

## 0. 位置
- 仓库：`~/Desktop/Cowork/PLAYGROUND/frontier-daily`（GitHub `SiaBuilt/frontier-daily`，分支 main，GitHub Pages）
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
- `kind`：`voice`（Builder 观点）、`podcast`（播客）、`article`（长文）、`fact`（事实报道），按内容类型填写，不以是否有 quote 决定排版。
- `who`：voice 填「姓名，身份」；podcast 填嘉宾姓名与身份，多位嘉宾如实列出；article 填作者；fact 填发布机构或媒体名称，不虚构人物身份。仅 voice 显示头像。
- `program`：podcast 的节目名；`takeaways`：podcast 可用 2–3 条简短讨论要点，不能与摘要重复，不凭简介虚构节目结论。
- `verification`：事实报道的核实状态，如「官方公告」「媒体报道，未核对财报原文」，须据实际取材填写，不把未核实报道写成定论。
- `tag`：2–4 字主题
- `url`：原文链接；`sourceLabel`：如「X @levie」「simonwillison.net」「Anthropic 官方公告」
- `title`：中文标题，具体，带数字更好
- `summary`：中文 1–2 句，≤90 字，第三人称概括。事实条目的 summary 只负责说明发生什么，不能替代下面的解释。
- `explanation`：重要 fact 条目必填，数组，每项含 `label` 和 `text`。用 2–3 个短段交代为什么、作用机制、证据与未知；一般合计 180–320 字，复杂事件可适当超出。事实、媒体转述与编辑推论分清，不为凑字重复摘要。
- `sources`：可附多条 `{label,url}`，让解释中的数字和机制可回到不同原始来源。
- `ctx`（必填）：一句背景，≤40 字，交代「这条是在回应什么 / 由什么引发」：哪件事、哪份文件、哪篇文章、哪次发布。读者不看原文也要知道来龙去脉。查不到背景的推文宁可不收。
- `quote`：**英文原话，必须逐字摘自原文**，不得改写或编造；没有合适原话就留空字符串
- `quoteZh`：quote 的中文翻译
- `gist`（有 quote 的条目必填）：一段完整的论证，2–4 句，≤120 字，按「结论 → 依据 → 所以呢」写，不要罗列数字碎片。**不用第三人称**（不写「他说」「他认为」），直接陈述观点本身。只保留支撑结论的 1–2 个关键数字，专有名词第一次出现时用几个字解释它是什么。
- `weight`：1–3。3 = 当天头等大事（最多 2 条）；2 = 值得想一想；1 = 一般信息。
- `soWhat`：只在 weight ≥ 2 时写，一句话点出启发或影响，克制、不鸡汤；weight 1 不写这个字段。

### 呈现方式
- Builder：人物头像、姓名与身份 → 短原话及翻译 → 背景和完整观点。引用必须来自该人物。
- Podcast：节目名 → 中文讨论主题 → 嘉宾 → 背景、核心要点 → 具体单集链接。不用频道首页冒充单集链接；未找到单集则在来源缺口中记录。原话可选，不能占据主标题。
- 长文：中文文章标题 → 作者 → 背景与论点 → 原文来源。
- 典型事实：中文事件标题 → 事实摘要、必要背景 → 克制的影响判断（如适用）→ 来源与核实状态。无头像，无大段引语；即使保留 quote，前端也不套用人物样式。事实摘要独立完整，不依赖 gist 才能读懂。无法确认的因果不要写进 soWhat。

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


## 7. AIs / Dot 通知
- 2026-11-02 已通过 ChatGPT 的 AIs 聊天配置「Frontier 早报推送」，AIs 确认任务已创建并启用；首次计划运行 2026-11-03。
- AIs 每天北京时间 09:00 只读检查线上 index.json 及当天日报；未更新则 10:00、11:00、12:00 重试，12:00 仍未更新提醒一次。
- 每天最多发送一条到 AIs 聊天：日期、headline、最多两条头条及当天链接；不推旧报，不生成日报、不操作仓库。
- Codex 保留 07:41 生成与发布任务，不重复创建通知任务或自行再向 AIs 发同一早报。
- AIs 已确认调度配置；实际首次运行和手机系统通知尚未验收。手机弹窗取决于应用与系统通知设置，调度可能延迟。
