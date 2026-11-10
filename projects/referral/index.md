# Telegram Referral System: from an empty group to about 2,000 members

> How I built a Telegram referral bot for a crypto creator: join checks, wallets, points and a leaderboard. About 2,000 members from an empty group.

Referral links, points and a leaderboard for a Telegram community.

## The problem

A crypto creator was starting a Telegram channel and group from nothing, and wanted to reward the members who brought other people in, without counting invites by hand.

## What I built

Members start the bot, which first checks that they have joined both the channel and the group. Then they submit their wallet address and get a personal referral link.

Every person they bring in earns them points, and the admins can see the top ten referrers at any time with one command.

Version 1.1.0, the public one, restores the join checks and the wallet submission from the full version I built for the client.

## Results

- About 2,000 members, starting from a group with nobody in it.

## Choices and why

### Why check membership before giving out a link?

Points only mean something if the people are really in the community. Checking the channel and the group first makes a referral a member, not a click.

### Why collect wallets inside the bot?

So each member's wallet is linked to their points from the start, with no separate form to chase later.

## Code and demo

[Code](https://github.com/anthonygozzini/Telegram-Referral-System), [Releases](https://github.com/anthonygozzini/Telegram-Referral-System/releases)

## If you need something like this

- [Custom Telegram bots](https://anthonygozzini.github.io/services/telegram-bots/index.md): Bots that screen new members, run referral programs or mirror channels, tested and released with versions.

[Book a 30-minute call](https://cal.com/anthony-gozzini-amzx2u/30min) · Email: anthony.gozzini@gmail.com

## Other case studies

- [GuardBot](https://anthonygozzini.github.io/projects/guardbot/index.md): Pre-trade safety for EVM, Solana and TRON, from simulated trades instead of a vendor API.
- [channel-miner](https://anthonygozzini.github.io/projects/channel-miner/index.md): Read a YouTube channel instead of watching it.
- [Telegram Gatekeeper Bot](https://anthonygozzini.github.io/projects/gatekeeper/index.md): Screens people before they join a private Telegram group.
