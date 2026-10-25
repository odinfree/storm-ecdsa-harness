---
tags:
  - research-loop
---

# 🔁 Research Loop

This vault **is one research loop**, scaffolded by the `research-loop` skill and driven
by an auto-expanding research cycle.

- **[[Config]]**: set the `seed`, the depth/breadth caps, and the **Research method**;
  flip `status` to `paused` to stop.
- **[[Queue]]**: the live, self-expanding list of topics.
- **[[Log]]**: one row per researched topic.
- **[[Map]]**: index of every note; pair with the graph view.
- **Findings.md**: the rolling digest, the one note to read to follow progress.
- **Research/**: this loop's generated notes.

## Run it

```
/research-loop cycle <loop-name>          # one cycle
/loop /research-loop cycle <loop-name>    # run continuously, self-paced
/research-loop status                     # overview of all loops
```

Obsidian is optional: the engine writes plain files, so open this folder as a vault to
watch the notes and graph grow live.
