# Projects — Anthony Gozzini

> What I build outside my job, published with the code: GuardBot, channel-miner, Telegram bots for crypto communities and Sgamers, my first Unity game.

Things I've built outside my job. Some started as work for paying clients, some are my own; all of them are published with their code.

## GuardBot (2026)

Pre-trade safety for EVM, Solana and TRON, from simulated trades instead of a vendor API.

Before you buy a token, GuardBot simulates a real buy and a real sell against live liquidity, so a honeypot shows up as a sell that fails instead of a green badge from someone else's API. One paste field then audits a wallet's token approvals across EVM, Solana and TRON and revokes the risky ones, simulating every revoke before signing. It runs locally, uses only Python's standard library and includes an MCP server, so AI agents can call it as a tool.

Tags: Python, MCP, Side project

Links: [Code](https://github.com/anthonygozzini/guardbot), [35-second demo](https://anthonygozzini.github.io/guardbot/demo.html)

## channel-miner (2026)

Read a YouTube channel instead of watching it.

Point it at a YouTube channel and it collects every video and turns it into text you can search, grep or read at your own pace. Tell it what you already know and an AI reads the lot and hands back only what is new to you. Everything runs on your own computer, with no accounts, no API keys and nothing to pay. On one channel it turned 377 hours across 179 videos into 237 MB of text.

Tags: Python, Shell, Side project

Links: [Code](https://github.com/anthonygozzini/channel-miner), [See it run](https://anthonygozzini.github.io/channel-miner/demo.html)

## Telegram Gatekeeper Bot (2023 – 2026)

Screens people before they join a private Telegram group.

Applicants answer a short questionnaire in a private chat. The bot checks the answers and looks for signs of fake or farmed accounts, such as no username, a name full of digits or a social profile already used by someone else. Then it either admits them with a single-use invite link or sends the request to the admins with Approve and Reject buttons. Questions, rules and messages live in one config file, so the same bot works for any community. Version 3 is the generic rewrite of a bot I first built for private crypto groups in 2023.

Tags: Python, SQLite, 40 tests, v3.0.0

Links: [Code](https://github.com/anthonygozzini/telegram-gatekeeper-bot), [Releases](https://github.com/anthonygozzini/telegram-gatekeeper-bot/releases)

## Sgamers (2018 · 2026)

My first game, made in Unity in 2018 and rebuilt in 2026.

A short 3D game with a main menu, one level and a credits screen, made while learning Unity with Brackeys' tutorials. The project folder was lost and only the compiled game survived, so in 2026 I rebuilt the project from that build, upgraded it to Unity 6 and brought it back to life in the browser. You can play it right here with a keyboard: arrow keys or A and D to move, Space to jump. The original Windows build is attached to the release.

Tags: Unity, C#, Playable in the browser

Links: [Play in your browser](https://anthonygozzini.github.io/play/sgamers/index.md), [Code](https://github.com/anthonygozzini/sgamers), [Windows build](https://github.com/anthonygozzini/sgamers/releases/tag/v1.0.0), [How I rebuilt it](https://anthonygozzini.github.io/writing/rebuilding-sgamers/index.md)

## Telegram Referral System (2024)

Referral links, points and a leaderboard for a Telegram community.

Members join the channel and the group, submit their wallet address and get a personal referral link. Every person they bring in earns them points, and admins can see the top referrers at any time. I built it for a crypto creator's community in 2024; version 1.1.0 restores the join checks and wallet submission from the full client version.

Tags: Python, Client work, v1.1.0

Links: [Code](https://github.com/anthonygozzini/Telegram-Referral-System), [Releases](https://github.com/anthonygozzini/Telegram-Referral-System/releases)

## Telegram Channel Message Copier (2024)

Mirrors posts from one Telegram channel to others.

A production bot that copies messages from a source channel to several destination channels and can schedule sends. It ran for a client who cross-posted to six channels; version 1.0.1 fixes a formatting slip that stopped it from starting.

Tags: Python, Client work, v1.0.1

Links: [Code](https://github.com/anthonygozzini/Telegram-Channel-Message-Copier-Bot), [Releases](https://github.com/anthonygozzini/Telegram-Channel-Message-Copier-Bot/releases)

## The Legend of Dragoon in Italian (2026)

An Italian language mod for the fan-made PC version of a 1999 PlayStation RPG.

Severed Chains is the fan-made PC version of The Legend of Dragoon. I'm adding Italian to it: 611 text strings are in the mod so far, and another 339 are hardcoded and need changes to the engine itself. It hasn't been tested in game yet, so there's no public release.

Tags: Localization, Modding, In progress
