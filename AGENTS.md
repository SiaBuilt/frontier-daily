# Frontier Daily

这是已有 GitHub Pages 早报项目，线上 https://frontier.siabuilt.com 。

- 每日生成与发布先完整阅读 `DAILY_BRIEF.md`，参考 `briefs/` 最新一期。
- 日报数据与网站 UI 分离；日常任务不修改 `index.html` 等界面文件。
- 日期使用 Asia/Shanghai。已存在的日报不覆盖，不编造引文、背景或统计。
- 提交前运行 `python3 scripts/validate_briefs.py --date YYYY-MM-DD`、`git diff --check`。
- 保留用户改动，禁止强推；发布是否成功以线上 JSON 核验为准。
