# How I rebuilt my first game from its only surviving build

By Anthony Gozzini · Published 15 Sep 2026 · 5 min read

> The project folder of my 2018 Unity game was gone; the compiled game wasn't. How an AI agent and I turned it back into a project, and the two bugs that almost stopped us.

In 2018 I made my first game in Unity, following Brackeys' beginner tutorials: a short 3D runner with a main menu, one level and a credits screen. Years later the project folder was gone. The only thing left was the compiled Windows game.

This September I decided to get it back, as a real project I could open, change and publish. I did it with an AI coding agent. The agent did the digging; my job was to decide what to try and to check every result before believing it.

## 1. From a build back to a project

AssetRipper, an open-source tool, can read a Unity build and export a project from it. Scenes, materials, textures, fonts and animations came back as they were. The C# scripts came back decompiled from the game's main assembly: they do what the originals did, but the comments and the formatting are gone.

The game was made with Unity 2018.2. Instead of hunting down an old editor, I moved it to Unity 6 LTS. The import finished with zero compile errors. That sounded too good, so we checked that the game's assembly had really been built from all nine scripts. It had.

## 2. The first bug: an empty setting

The first browser build failed at the very last step, with an "index out of range" error deep inside Unity's WebGL post-processing. The cause was a single empty field: the export had left the WebGL template name blank, and Unity 6 expects a name it can split in two. Setting it to the default template fixed it.

## 3. The second bug: an interface that wasn't there

The build warnings pointed at something worse. In 2018 Unity's UI components lived in a DLL; in Unity 6 they are source code inside a package. Every text, button and canvas in my three scenes, 31 references in all, still pointed at a DLL that no longer existed. The game would have started without a menu.

Unity identifies a script inside a DLL with a number derived from an MD4 hash of its namespace and class name. Instead of guessing which number meant Button and which meant Text, we computed the hash for every UI class in Unity 6, after first testing the formula on a reference whose answer we already knew. All eleven unknown numbers matched a real class. We rewrote 35 references, confirmed that none were left, and built again.

## 4. Proof, not a loading bar

The first automated test captured only Unity's loading bar, which proved nothing. So we drove a real browser through its DevTools protocol: the menu appeared, a click on Start loaded the level, and the console showed no errors. Later, Quit did nothing in the browser, because a web page can't close its own tab. In the browser version Quit now takes you back to the main menu, tested all the way from the credits screen.

## What I took from it

Almost every step had a moment where the easy answer was wrong: zero errors that needed checking, a test that only showed a loading bar, a mapping that could have been guessed. The agent is fast; the checking is the job. It's the same rule I follow in marketing operations.

You can [play Sgamers in your browser](https://anthonygozzini.github.io/play/sgamers/). You'll need a keyboard.
