<script setup>
import { ref, computed } from "vue";
import { stories } from "../../data/games.js";
import { recordGame } from "../../composables/useProgress.js";

const sIdx = ref(0);
const story = computed(() => stories[sIdx.value]);
const cur = ref(stories[0].start);
const risk = ref(0);
const node = computed(() => story.value.nodes[cur.value]);
const ended = computed(() => !!node.value.end);

function pick(c) { risk.value = Math.min(100, risk.value + (c.risk || 0)); cur.value = c.to; if (story.value.nodes[c.to].end) recordGame("story", story.value.nodes[c.to].end === "good" ? 1 : 0, 1); }
function restart(next) {
  if (next) sIdx.value = (sIdx.value + 1) % stories.length;
  cur.value = story.value.start; risk.value = 0;
}
</script>
<template>
  <p class="muted">情境：<strong>{{ story.title }}</strong> — 你的每個選擇，決定會不會被騙到匯款。</p>
  <!-- 被騙風險儀錶 -->
  <div class="risk">
    <span class="rk-l">被騙風險</span>
    <div class="rk-bar"><div class="rk-fl" :style="{ width: risk + '%', background: risk > 60 ? 'var(--danger)' : risk > 30 ? 'var(--warn)' : 'var(--ok)' }"></div></div>
    <span class="rk-v">{{ risk }}%</span>
  </div>

  <div v-if="ended" class="end" :class="node.end">
    <svg viewBox="0 0 120 90" class="end-art" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" fill="none">
      <circle cx="60" cy="45" r="36" :fill="node.end==='good' ? '#e7f3ee' : '#fdecec'" />
      <template v-if="node.end==='good'">
        <path d="M60 26l13 5v10c0 9-6 15-13 17-7-2-13-8-13-17V31l13-5Z" fill="rgba(47,143,118,.18)" stroke="#2f8f76" />
        <path d="M53 45l5 5 11-11" stroke="#2f8f76" />
      </template>
      <template v-else>
        <path d="M45 38c0-8 30-8 30 0v18c0 4-30 4-30 0V38Z" fill="#fff" stroke="#d2452f" />
        <path d="M45 44h30" stroke="#d2452f" /><path d="M70 30l8-6M74 34l9-2" stroke="#e8743b" />
      </template>
    </svg>
    <h3>{{ node.end === 'good' ? '你守住了！' : '糟糕，被騙了…' }}</h3>
    <p>{{ node.text }}</p>
    <div class="endbtns">
      <button class="btn" @click="restart(false)">重玩這題</button>
      <button class="btn ghost" @click="restart(true)">換個情境 →</button>
    </div>
  </div>
  <div v-else>
    <div class="npc">{{ node.npc }}</div>
    <div class="choices">
      <button v-for="(c, k) in node.choices" :key="k" class="choice" @click="pick(c)">{{ c.label }}</button>
    </div>
  </div>
</template>
<style scoped>
.risk { display: flex; align-items: center; gap: .6rem; margin: .6rem 0 1rem; }
.rk-l { font-size: .82rem; color: var(--ink-soft); white-space: nowrap; }
.rk-bar { flex: 1; height: 12px; background: #f1e6d8; border-radius: 999px; overflow: hidden; }
.rk-fl { height: 100%; border-radius: 999px; transition: width .4s, background .4s; }
.rk-v { font-weight: 700; font-size: .85rem; }
.npc { background: #fff; border: 1px solid var(--line); border-radius: 16px 16px 16px 3px; padding: 1rem 1.2rem; font-size: 1.1rem; line-height: 1.8; box-shadow: var(--shadow); margin-bottom: 1rem; }
.choices { display: flex; flex-direction: column; gap: .6rem; }
.choice { text-align: left; cursor: pointer; background: var(--brand-soft); color: var(--brand-deep); border: 1.5px solid #f4cdb6; border-radius: 14px; padding: .9rem 1.1rem; font-size: 1.05rem; font-weight: 600; transition: all .12s; }
.choice:hover { background: #fbdcca; transform: translateX(3px); }
.end { text-align: center; padding: .5rem; }
.end-art { width: 140px; height: auto; }
.end.bad h3 { color: var(--danger); } .end.good h3 { color: var(--ok); }
.endbtns { display: flex; gap: .6rem; justify-content: center; margin-top: 1rem; }
</style>
