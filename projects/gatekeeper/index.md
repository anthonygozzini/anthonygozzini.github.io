# Telegram Gatekeeper Bot: screening who joins a private group

> How I built a Telegram bot that screens applicants to private groups: a questionnaire, fake-account signals and single-use invites. Ran in 10 groups.

Screens people before they join a private Telegram group.

## The problem

Private crypto groups attract fake and farmed accounts as soon as there is something to gain. Admitting people by hand doesn't scale, and an open invite link gets forwarded everywhere.

## What I built

I built the first version in 2023 for private crypto groups: applicants answered a short questionnaire in a private chat, the admins reviewed it, and accepted people got an invite link that works only once. The early versions ran in 10 groups.

Version 3 is the rewrite for any community. Questions, rules and messages live in one config file. It checks social profile links on six platforms, looks for signs of fake or farmed accounts, and either admits people automatically or sends the request to the admins with Approve and Reject buttons.

Every decision, automatic or not, is posted to the admins and stored, and the same person can't apply again until a cooldown has passed.

## Results

- 10 private groups ran the early versions.
- 6 social platforms checked: X, Instagram, TikTok, YouTube, GitHub and LinkedIn.
- 40 tests on the rules, the configuration, the storage and the Telegram calls.
- 3 versions, from manual review to one bot configured from a single file.

## Choices and why

### Why single-use invite links?

A normal invite link gets forwarded. A link that works for one person, and can expire, keeps the group closed to anyone who wasn't screened.

### Why doesn't a warning sign reject people?

No username, or a name full of digits, is suspicious, not proof. Rejecting on that alone would turn real people away, so a warning sign sends the request to a human.

### Why one config file?

So the same bot works for any community without touching the code: admins change the questions and the rules, not the Python.

## Limits

- Version 3's rules and storage are covered by tests, but its Telegram flow hasn't yet run in a live group.

## Code and demo

[Code](https://github.com/anthonygozzini/telegram-gatekeeper-bot), [Releases](https://github.com/anthonygozzini/telegram-gatekeeper-bot/releases)

## If you need something like this

- [Custom Telegram bots](https://anthonygozzini.github.io/services/telegram-bots/index.md): Bots that screen new members, run referral programs or mirror channels, tested and released with versions.

[Book a 30-minute call](https://cal.com/anthony-gozzini-amzx2u/30min) · Email: anthony.gozzini@gmail.com

## Other case studies

- [GuardBot](https://anthonygozzini.github.io/projects/guardbot/index.md): Pre-trade safety for EVM, Solana and TRON, from simulated trades instead of a vendor API.
- [channel-miner](https://anthonygozzini.github.io/projects/channel-miner/index.md): Read a YouTube channel instead of watching it.
- [Telegram Referral System](https://anthonygozzini.github.io/projects/referral/index.md): Referral links, points and a leaderboard for a Telegram community.
