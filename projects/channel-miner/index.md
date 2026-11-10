# channel-miner: reading years of YouTube instead of watching them

> How I built channel-miner: a whole YouTube channel turned into searchable text, and a local AI that reports only what is new to you.

Read a YouTube channel instead of watching it.

## The problem

Some of the best knowledge on a niche topic sits in years of long YouTube videos and streams: hundreds of hours, no index, no search. Watching all of it isn't realistic, and skimming misses the one sentence that matters.

## What I built

Point it at a channel and it collects every video with its captions, transcribes the ones that have none on your own computer, and turns everything into plain text you can search or read.

Then you tell it what you already know, as a short list of topics. A local AI model reads the transcripts against that list, and a second pass judges each finding: keep, watch or discard, with a reason. The model proposes; it doesn't decide.

Another step uses plain counting, no AI, to surface ideas the channel keeps coming back to that match none of your topics.

## Results

- 377 hours of video across 179 videos turned into 237 MB of text.
- A search found one sentence 1 hour 39 minutes into a four-hour stream from 2024.
- A four-hour video without captions is transcribed in about 3 minutes on a graphics card.
- No accounts, no API keys, nothing to pay.

## Choices and why

### Why does everything run locally?

What you know and what you're looking for never leave your computer, and there is no bill per hour of video.

### Why is the AI part opt-in?

A couple of gigabytes should never start downloading by surprise. Without it, you still get a full, searchable archive of the channel.

### Why do scheduled runs complain loudly?

A broken downloader looks exactly like a quiet week with nothing new. So a run that fails to download says so, can pick up where it stopped, and can't overlap with another run.

## Limits

- On a small graphics card the bigger models fall back to the processor, at about 5 words a second, so the reading step is slow on modest machines.
- The model can be wrong, which is why it only proposes and a second pass judges every finding.

## Code and demo

[Code](https://github.com/anthonygozzini/channel-miner), [See it run](https://anthonygozzini.github.io/channel-miner/demo.html)

## If you need something like this

- [AI automation for marketing](https://anthonygozzini.github.io/services/ai-automation/index.md): Pipelines that take the volume out of localization, reporting and content, checked before anything ships.

[Book a 30-minute call](https://cal.com/anthony-gozzini-amzx2u/30min) · Email: anthony.gozzini@gmail.com

## Other case studies

- [GuardBot](https://anthonygozzini.github.io/projects/guardbot/index.md): Pre-trade safety for EVM, Solana and TRON, from simulated trades instead of a vendor API.
- [Telegram Gatekeeper Bot](https://anthonygozzini.github.io/projects/gatekeeper/index.md): Screens people before they join a private Telegram group.
- [Telegram Referral System](https://anthonygozzini.github.io/projects/referral/index.md): Referral links, points and a leaderboard for a Telegram community.
