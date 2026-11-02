# Frontier Daily

Frontier 早报，部署在 https://frontier.siabuilt.com 。

## 每日更新

由 Codex 每日北京时间 07:41 在接手聊天中执行，生成、校验并推送当天早报。电脑和 Codex 应用需保持运行。规范见 [DAILY_BRIEF.md](DAILY_BRIEF.md)，项目入口见 [AGENTS.md](AGENTS.md)。

```sh
python3 scripts/validate_briefs.py --date YYYY-MM-DD
```

日报存放在 `briefs/`，`briefs/index.json` 按日期倒序；前端自动读取最新一期。只在可靠一手来源有新数据时更新顶栏。当天已有内容不覆盖。

2026-11-02 接手时：远程最新提交 `1b88154`，线上最新一期为 2026-11-01；旧 Claude 本地任务表为空，手机专有推送未迁移。Codex 运行结果返回接手聊天，首个定时执行结果仍需观察。


2026-11-02 后续：分类排版与 Google 事实解释已上线核验。AIs / Dot 已确认「Frontier 早报推送」启用，从 11 月 3 日起北京时间 09:00 检查，未更新则每小时重试至 12:00，每天最多通知一次；首次运行及手机系统通知待验收。Codex 出刊，AIs 通知，详见生成规范第 7 节。
