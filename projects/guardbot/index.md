# GuardBot: checking a token by trading it, not by trusting a badge

> How I built GuardBot: token checks that simulate a real buy and sell on 8 chains, scored on a public benchmark that names every error.

Pre-trade safety for EVM, Solana and TRON, from simulated trades instead of a vendor API.

## The problem

Trading bots and AI agents that buy tokens on their own usually act on someone else's verdict: an API returns a green badge and the bot buys. When the badge is wrong the money is gone, and nobody can see why the API said safe.

## What I built

Before a buy, GuardBot runs the trade itself in a simulation: a real buy and a real sell against the live pool, pinned to one block. A honeypot shows up as a sell that fails, with the failing call as evidence, not as a score.

One paste field then audits a wallet's token approvals on EVM chains, Solana and TRON and revokes the risky ones. Only three kinds of revoke can ever be built, each is simulated before signing, and the exact call is shown first.

It runs on your own computer with Python's standard library only: nothing to install, no keys, no account. It has its own transaction signer and an MCP server, so an AI agent can call it as a tool.

## Results

- 8 chains: Ethereum, Arbitrum, Polygon, Base, Optimism, BSC, Solana and TRON.
- Public benchmark of 19 September 2026: 5 of 5 live honeypots blocked, and none of 21 major tokens wrongly blocked or flagged.
- 51 offline tests, plus 19 that run against real chains.
- About 2 seconds for a live scan across chains.

## Choices and why

### Why simulate instead of calling a safety API?

Because an API's answer can't be checked. A sell that fails in a simulation is evidence anyone can reproduce. Outside labels are used only as hints, never as the verdict.

### Why only Python's standard library?

A tool that guards a wallet should be easy to read and have nothing to install. Fewer dependencies means fewer places where something can break or be swapped.

### Why publish the errors?

The first benchmark run caught a real bug: Ethereum USDT came back as a honeypot, because of a stranger's leftover 4 USDT allowance that Tether's contract refuses to overwrite. The fix went in the same day. A number nobody can check isn't worth publishing.

## Limits

- Five live honeypots is a small set: of 155 pools launched on BSC and Base on 19 September, only two still had a pool twelve hours later.
- Liquidity is measured on the native-coin pair only, so a token that trades mostly against USDT can look thinner than it is.

## Code and demo

[Code](https://github.com/anthonygozzini/guardbot), [35-second demo](https://anthonygozzini.github.io/guardbot/demo.html), [Project page](https://anthonygozzini.github.io/guardbot/)

## If you need something like this

- [AI automation for marketing](https://anthonygozzini.github.io/services/ai-automation/index.md): Pipelines that take the volume out of localization, reporting and content, checked before anything ships.

[Book a 30-minute call](https://cal.com/anthony-gozzini-amzx2u/30min) · Email: anthony.gozzini@gmail.com

## Other case studies

- [channel-miner](https://anthonygozzini.github.io/projects/channel-miner/index.md): Read a YouTube channel instead of watching it.
- [Telegram Gatekeeper Bot](https://anthonygozzini.github.io/projects/gatekeeper/index.md): Screens people before they join a private Telegram group.
- [Telegram Referral System](https://anthonygozzini.github.io/projects/referral/index.md): Referral links, points and a leaderboard for a Telegram community.
