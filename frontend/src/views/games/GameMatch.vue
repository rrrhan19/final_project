<script setup>
import { ref } from "vue";
import { matchItems, matchTypes } from "../../data/games.js";
import { recordGame } from "../../composables/useProgress.js";

function shuffle(a) { a = [...a]; for (let k = a.length - 1; k > 0; k--) { const j = Math.floor(Math.random() * (k + 1)); [a[k], a[j]] = [a[j], a[k]]; } return a; }

const items = ref(shuffle(matchItems));
const types = ref(shuffle(matchTypes));
const picked = ref(null); const matched = ref({}); const wrong = ref(null); const errors = ref(0); const done = ref(false);

function pickItem(idx) { if (matched.value[idx]) return; picked.value = idx; }
function chooseType(t) {
  if (picked.value === null) return;
  const it = items.value[picked.value];
  if (it.type === t) {
    matched.value = { ...matched.value, [picked.value]: true };
    picked.value = null;
    if (Object.keys(matched.value).length === items.value.length) { done.value = true; recordGame("match", Math.max(0, items.value.length - errors.value), items.value.length); }
  } else { errors.value++; wrong.value = t; setTimeout(() => (wrong.value = null), 400); }
}
function restart() { items.value = shuffle(matchItems); types.value = shuffle(matchTypes); picked.value = null; matched.value = {}; errors.value = 0; done.value = false; }
</script>
<template>
  <div v-if="done" class="fin">
    <h3>🧩 全部配對成功！</h3>
    <p>失誤 {{ errors }} 次　·　{{ errors === 0 ? '完美！一次就全中 🎉' : '再玩一次挑戰零失誤！' }}</p>
    <button class="btn" @click="restart">再玩一次</button>
  </div>
  <div v-else>
    <p class="muted">點左邊<strong>話術卡</strong>，再點右邊它屬於的<strong>類型</strong>。失誤 {{ errors }} 次。</p>
    <div class="board">
      <div class="col">
        <button v-for="(it, idx) in items" :key="idx" class="it" :class="{ on: picked === idx, done: matched[idx] }" :disabled="matched[idx]" @click="pickItem(idx)">
          {{ matched[idx] ? "✅ " : "" }}{{ it.text }}
        </button>
      </div>
      <div class="col types">
        <button v-for="t in types" :key="t" class="ty" :class="{ shake: wrong === t }" @click="chooseType(t)">{{ t }}</button>
      </div>
    </div>
    <p class="muted prog">已配對 {{ Object.keys(matched).length }} / {{ items.length }}</p>
  </div>
</template>
<style scoped>
.board { display: grid; grid-template-columns: 1fr; gap: 1rem; margin: .8rem 0; }
@media (min-width: 560px) { .board { grid-template-columns: 1.4fr 1fr; } }
.col { display: flex; flex-direction: column; gap: .5rem; }
.types { justify-content: flex-start; }
.it { text-align: left; cursor: pointer; background: var(--cream-2); border: 1.5px solid var(--line); border-radius: 12px; padding: .7rem .9rem; font-size: .98rem; transition: all .12s; }
.it.on { border-color: var(--brand); background: var(--brand-soft); transform: scale(1.02); }
.it.done { opacity: .5; border-color: var(--ok); }
.ty { cursor: pointer; background: #fff; border: 1.6px solid var(--brand); color: var(--brand-deep); border-radius: 12px; padding: .7rem 1rem; font-weight: 700; }
.ty:hover { background: var(--brand-soft); }
.shake { animation: sh .4s; background: #fdecec; border-color: var(--danger); color: var(--danger); }
@keyframes sh { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-5px)} 75%{transform:translateX(5px)} }
.prog { text-align: center; }
.fin { text-align: center; }
</style>
