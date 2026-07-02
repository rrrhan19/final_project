<script setup>
import { ref, nextTick } from "vue";
import { chat } from "../api.js";

const msgs = ref([
  { role: "assistant", content: "嗨，我是防詐小助手。把你遇到的情況或可疑訊息告訴我，我幫你看看像不像詐騙、該怎麼處理。" },
]);
const input = ref("");
const loading = ref(false);
const box = ref(null);

const quick = ["有人邀我加LINE投資保證獲利", "收到包裹簡訊要我點連結", "自稱檢警說我帳戶涉案"];

async function send(text) {
  const m = (text ?? input.value).trim();
  if (!m || loading.value) return;
  msgs.value.push({ role: "user", content: m });
  input.value = "";
  loading.value = true;
  await scroll();
  try {
    const r = await chat(m, msgs.value.slice(0, -1));
    msgs.value.push({ role: "assistant", content: r.reply, engine: r.engine });
  } catch (e) {
    msgs.value.push({ role: "assistant", content: "抱歉，連線出了點問題：" + e.message });
  } finally {
    loading.value = false;
    await scroll();
  }
}
async function scroll() { await nextTick(); if (box.value) box.value.scrollTop = box.value.scrollHeight; }
</script>

<template>
  <div class="card">
    <h2>💬 AI 防詐問答助手</h2>
    <p class="muted">用聊天的方式問我任何防詐問題，可以追問。（未連 Gemini 時提供通用指引）</p>
    <div class="chatbox" ref="box">
      <div v-for="(m, i) in msgs" :key="i" :class="['bubble', m.role]">
        <span style="white-space:pre-wrap">{{ m.content }}</span>
      </div>
      <div v-if="loading" class="bubble assistant muted">思考中…</div>
    </div>
    <div class="quick"><span v-for="q in quick" :key="q" class="chip" @click="send(q)">{{ q }}</span></div>
    <div class="inputrow">
      <input v-model="input" class="inp" placeholder="輸入你的問題…" @keyup.enter="send()" />
      <button class="btn" :disabled="loading || !input.trim()" @click="send()">送出</button>
    </div>
    <p class="muted" style="font-size:.78rem;margin-top:.6rem">🔒 訊息會送至後端；若啟用 AI 會送交 Google Gemini。請勿輸入他人個資。</p>
  </div>
</template>

<style scoped>
.chatbox { background: #f7f9ff; border: 1px solid var(--line); border-radius: 12px; padding: 1rem; height: 360px; overflow-y: auto; margin: .8rem 0; }
.bubble { max-width: 85%; padding: .6rem .9rem; border-radius: 12px; margin: .4rem 0; line-height: 1.7; }
.bubble.user { background: var(--brand); color: #fff; margin-left: auto; border-bottom-right-radius: 3px; }
.bubble.assistant { background: #fff; border: 1px solid var(--line); border-bottom-left-radius: 3px; }
.quick { margin-bottom: .6rem; }
.inputrow { display: flex; gap: .5rem; }
.inputrow .inp { flex: 1; padding: .7rem 1rem; border: 1.5px solid var(--line); border-radius: 10px; font-size: 1.05rem; }
.inputrow .inp:focus { outline: none; border-color: var(--brand); }
</style>
