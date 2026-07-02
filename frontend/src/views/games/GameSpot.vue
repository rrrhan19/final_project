<script setup>
import { ref, computed } from "vue";
import { spotItems } from "../../data/games.js";
import { recordGame } from "../../composables/useProgress.js";

const i = ref(0); const found = ref(new Set()); const done = ref(false); const score = ref(0);
const item = computed(() => spotItems[i.value]);
const parts = computed(() => {
  const esc = item.value.flags.map((f) => f.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  const re = new RegExp("(" + esc.join("|") + ")", "g");
  return item.value.text.split(re).filter((s) => s !== "").map((seg) => ({ seg, flag: item.value.flags.includes(seg) }));
});
function tap(seg, flag) { if (done.value || !flag) return; found.value = new Set(found.value).add(seg); }
function reveal() {
  done.value = true;
  if (found.value.size === item.value.flags.length) score.value++;
}
function next() {
  if (i.value + 1 >= spotItems.length) { i.value = -2; recordGame("spot", score.value, spotItems.length); return; }
  i.value++; found.value = new Set(); done.value = false;
}
function restart() { i.value = 0; found.value = new Set(); done.value = false; score.value = 0; }
</script>
<template>
  <div v-if="i === -2" class="fin">
    <h3>🎯 完成！</h3>
    <p>你全找出紅旗詞的關卡：<strong>{{ score }} / {{ spotItems.length }}</strong></p>
    <button class="btn" @click="restart">再玩一次</button>
  </div>
  <div v-else>
    <p class="muted">第 {{ i + 1 }} / {{ spotItems.length }} 關 — 點出這則訊息裡<strong>可疑的字句</strong>：</p>
    <div class="msg">
      <template v-for="(p, k) in parts" :key="k">
        <span v-if="p.flag" class="tok" :class="{ got: found.has(p.seg), bad: done && !found.has(p.seg) }" @click="tap(p.seg, p.flag)">{{ p.seg }}</span>
        <span v-else>{{ p.seg }}</span>
      </template>
    </div>
    <p class="muted">已找到 {{ found.size }} / {{ item.flags.length }} 個紅旗詞</p>
    <button v-if="!done" class="btn ghost" @click="reveal">對答案</button>
    <template v-else>
      <p class="tip">✅ 紅旗詞：{{ item.flags.join("、") }}　—　這些「保證、急迫、要你操作/匯款/點連結」的字眼就是警訊。</p>
      <button class="btn" @click="next">下一關</button>
    </template>
  </div>
</template>
<style scoped>
.msg { font-size: 1.2rem; line-height: 2.2; background: var(--cream-2); border: 1px solid var(--line); border-radius: 14px; padding: 1rem 1.2rem; margin: .6rem 0; }
.tok { cursor: pointer; border-bottom: 2px dashed #e0a88a; padding: .05rem .15rem; border-radius: 4px; }
.tok.got { background: #fde9dc; color: var(--brand-deep); border-bottom-color: var(--brand); font-weight: 700; }
.tok.bad { border-bottom-color: var(--danger); }
.tip { background: #e9f7f2; border-left: 3px solid var(--ok); padding: .6rem .8rem; border-radius: 0 8px 8px 0; }
.fin { text-align: center; }
</style>
