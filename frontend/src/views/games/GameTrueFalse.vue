<script setup>
import { ref, onMounted, onUnmounted, computed } from "vue";
import { tfItems } from "../../data/games.js";
import { recordGame } from "../../composables/useProgress.js";

const items = ref([]); const i = ref(0); const score = ref(0); const streak = ref(0); const best = ref(0);
const time = ref(8); const fb = ref(null); const done = ref(false); const pop = ref(0); let timer = null;

function shuffle(a) { a = [...a]; for (let k = a.length - 1; k > 0; k--) { const j = Math.floor(Math.random() * (k + 1)); [a[k], a[j]] = [a[j], a[k]]; } return a; }
const cur = computed(() => items.value[i.value]);

function tick() {
  time.value -= 1;
  if (time.value <= 0) answer(null);
}
function startTimer() { clearInterval(timer); time.value = 8; timer = setInterval(tick, 1000); }
function answer(guess) {
  if (fb.value) return;
  clearInterval(timer);
  const correct = guess !== null && guess === cur.value.isScam;
  const gain = correct ? 1 + Math.floor(streak.value / 3) : 0;  // 連對倍率
  fb.value = { correct, real: cur.value.isScam, gain };
  if (correct) { score.value += gain; streak.value++; best.value = Math.max(best.value, streak.value); pop.value++; }
  else streak.value = 0;
}
function next() {
  fb.value = null;
  if (i.value + 1 >= items.value.length) { done.value = true; clearInterval(timer); recordGame("tf", score.value, items.value.length * 2); return; }
  i.value++; startTimer();
}
function start() { items.value = shuffle(tfItems); i.value = 0; score.value = 0; streak.value = 0; best.value = 0; done.value = false; fb.value = null; startTimer(); }
onMounted(start);
onUnmounted(() => clearInterval(timer));
const grade = computed(() => { const r = score.value / items.value.length; return r >= 0.9 ? "防詐大師 🏆" : r >= 0.7 ? "火眼金睛 👏" : r >= 0.5 ? "繼續加油 💪" : "要小心囉 ⚠️"; });
</script>
<template>
  <div v-if="done" class="fin">
    <h3>{{ grade }}</h3>
    <p>答對 <strong>{{ score }} / {{ items.length }}</strong>　·　最高連對 {{ best }}</p>
    <button class="btn" @click="start">再來一局</button>
  </div>
  <div v-else-if="cur">
    <div class="hud"><span>第 {{ i + 1 }}/{{ items.length }}</span><span>🔥 連對 {{ streak }}{{ streak >= 3 ? ' ×' + (1 + Math.floor(streak/3)) : '' }}</span><span class="sc" :key="pop">得分 {{ score }}</span></div>
    <div class="timebar"><div class="tf" :style="{ width: (time / 8 * 100) + '%', background: time <= 3 ? 'var(--danger)' : 'var(--brand)' }"></div></div>
    <div class="msg">{{ cur.text }}</div>
    <div v-if="!fb" class="vs">
      <button class="big scam" @click="answer(true)">⚠️ 是詐騙</button>
      <button class="big ok" @click="answer(false)">✅ 正常</button>
    </div>
    <div v-else class="fbk">
      <p :style="{ color: fb.correct ? 'var(--ok)' : 'var(--danger)', fontWeight: 800, fontSize: '1.1rem' }">
        {{ fb.correct ? `答對了！ +${fb.gain}` : "答錯了" }}（正解：{{ fb.real ? "詐騙" : "正常" }}）
      </p>
      <button class="btn" @click="next">{{ i + 1 >= items.length ? "看結果" : "下一題" }}</button>
    </div>
  </div>
</template>
<style scoped>
.hud { display: flex; justify-content: space-between; font-weight: 700; color: var(--ink-soft); margin-bottom: .4rem; }
.sc { color: var(--brand-deep); animation: pop .3s; }
@keyframes pop { 0% { transform: scale(1); } 40% { transform: scale(1.35); } 100% { transform: scale(1); } }
.timebar { height: 8px; background: #eee; border-radius: 999px; overflow: hidden; margin-bottom: .8rem; }
.tf { height: 100%; transition: width 1s linear; }
.msg { font-size: 1.25rem; background: var(--cream-2); border: 1px solid var(--line); border-radius: 14px; padding: 1.4rem 1.2rem; min-height: 90px; display: grid; place-items: center; text-align: center; }
.vs { display: flex; gap: .8rem; margin-top: 1rem; }
.big { flex: 1; cursor: pointer; border: none; border-radius: 14px; padding: 1.1rem; font-size: 1.15rem; font-weight: 800; color: #fff; }
.big.scam { background: var(--danger); } .big.ok { background: var(--ok); }
.fbk { margin-top: 1rem; text-align: center; }
.fin { text-align: center; }
</style>
