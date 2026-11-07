# [Benchmark #1] 50-Block Autonomous Construction Challenge across South Korea

### 📌 Overview
Welcome to the official 50-block autonomous digital twin construction challenge!
Following the successful completion of Busan Haeundae-gu (#2), your mission is to autonomously research, construct, and submit block data packages for **50 unbuilt administrative districts across South Korea**.

---

### 📋 Key Instructions & Rules

1. **Assignment List**: Refer to [BATCH_50_TASKS.md](BATCH_50_TASKS.md) for the 50 district codes and names (Task 01 to Task 50).
2. **One Block = One Branch = One PR**:
   - For each block, create branch `add-<block_code>`.
   - Submit a separate Pull Request targeting `main` for each district: `[Block] Add <block_name> (<block_code>)`.
   - Sequential and parallel autonomous execution are both supported.
3. **Quality Standards**:
   - Minimum **5 prominent landmarks** per block.
   - Landmark `source_url` must point to an official detailed subpage (not root domain).
   - Validate locally via `python tools/validate_block.py incoming/<block_code>` before opening PR.
4. **Benchmark Goal**:
   - Let's see how many blocks you can complete and update over the next 24 hours!

Good luck, Agent Pimang! 🚀
