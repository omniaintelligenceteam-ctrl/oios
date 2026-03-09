# OIOS Cron Schedule

Configure these crons in the client's OpenClaw instance. Each cron triggers a skill at the specified time in the client's timezone.

| Cron | Schedule | Skill | What It Does | Output |
|------|----------|-------|-------------|--------|
| Morning Briefing | 6:30 AM daily | `/daily-briefing` | Summarizes today's jobs, follow-ups, leads, pipeline | Telegram message to owner |
| Follow-Up Runner | 9:00 AM daily | `/follow-up` | Checks pending.jsonl for due follow-ups, drafts messages | Draft messages for owner approval |
| Stale Deal Check | 10:00 AM daily | `/check-stale` | Scans pipeline and follow-ups for items going cold | Telegram alert (only if stale items found) |
| End of Day Wrap | 5:00 PM daily | _(inline)_ | Archives completed jobs, logs today's activity | Activity summary saved to briefings/ |
| Weekly Report | Friday 4:00 PM | `/weekly-report` | Full week metrics, trends, recommendations | Telegram summary + full report in briefings/ |
| License Watch | Monday 8:00 AM | _(inline)_ | Checks context/tools.md for upcoming expirations | Telegram alert (only if expirations found) |

## Timezone
All times are in **[CLIENT_TIMEZONE]**. Set this during onboarding.

## End of Day Wrap (Inline Logic)
Since this doesn't have a dedicated skill, here's what it does:
1. Scan `jobs/in-progress/` — move any marked complete to `jobs/completed/`
2. Count today's activity: calls logged, proposals sent, follow-ups completed
3. Save summary to `briefings/YYYY-MM-DD-eod.md`
4. No Telegram message unless something unusual happened

## License Watch (Inline Logic)
1. Read `context/tools.md`
2. Check for any tools with expiration dates within 14 days
3. If found, alert owner via Telegram: "ALERT: [Tool] expires [date]"
4. If nothing expiring, no message

## Setup Notes
- Crons should be configured to run in the client's timezone
- All crons that send Telegram messages require the bot to be connected first
- Test each cron manually before activating the schedule
- The Follow-Up Runner depends on `follow-ups/pending.jsonl` having entries
