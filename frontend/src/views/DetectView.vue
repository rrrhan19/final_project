<script setup>
import { ref } from "vue";
import { detect, checkUrl, checkPhone, report } from "../api.js";

const tab = ref("text");
const tabs = [
  { k: "text", label: "訊息偵測" },
  { k: "url", label: "網址檢查" },
  { k: "phone", label: "電話查詢" },
  { k: "image", label: "截圖偵測" },
];

const badge = {
  scam: { label: "⚠️ 高風險 / 疑似詐騙", color: "var(--danger)", bg: "#fdecec" },
  legit: { label: "✅ 看起來正常", color: "var(--ok)", bg: "#e9f7ef" },
  uncertain: { label: "❓ 需要留意", color: "var(--warn)", bg: "#fff6e6" },
};
function pct(r) { return Math.round((r.confidence ?? r.risk ?? 0) * 100); }

// ── 訊息（分類真實範例，一鍵帶入）──
const text = ref("");
const examples = [
  { t: "假投資", v: "老師帶單保證獲利30%，加LINE進VIP群，名額有限速進場" },
  { t: "假冒公務", v: "這裡是地檢署，您帳戶涉及洗錢案，請將存款匯入安全帳戶配合調查" },
  { t: "解除分期", v: "您先前購物被誤設成12期分期，請依語音操作ATM解除，否則每月扣款" },
  { t: "釣魚簡訊", v: "您的包裹地址有誤無法配送，請點 http://reurl-fake.xyz 更新收件資料" },
  { t: "假交友", v: "親愛的我在國外執行任務，包裹被海關扣留，能先幫我付手續費嗎" },
  { t: "正常訊息", v: "媽我晚點回家，晚餐不用等我" },
];
const tRes = ref(null); const tLoad = ref(false); const tErr = ref("");
async function runText() {
  if (!text.value.trim()) return;
  tLoad.value = true; tErr.value = ""; tRes.value = null;
  try { tRes.value = await detect(text.value); } catch (e) { tErr.value = "偵測失敗：" + e.message; } finally { tLoad.value = false; }
}

// ── 網址 ──
const url = ref(""); const uRes = ref(null); const uLoad = ref(false); const uErr = ref("");
const urlEx = [
  { t: "官方黑名單", v: "bbhhshf.cc" },
  { t: "仿冒品牌", v: "paypal-verify.top" },
  { t: "IP 網址", v: "http://192.168.0.5/pay" },
  { t: "正常網站", v: "https://www.google.com" },
];
async function runUrl() {
  if (!url.value.trim()) return;
  uLoad.value = true; uErr.value = ""; uRes.value = null;
  try { uRes.value = await checkUrl(url.value); } catch (e) { uErr.value = "檢查失敗：" + e.message; } finally { uLoad.value = false; }
}

// ── 電話 ──
const phone = ref(""); const pRes = ref(null); const pLoad = ref(false); const pErr = ref(""); const reported = ref(false);
const phoneEx = [
  { t: "國際偽冒(+886)", v: "+886912345678" },
  { t: "市話", v: "0277123456" },
  { t: "一般手機", v: "0912345678" },
];
async function runPhone() {
  if (!phone.value.trim()) return;
  pLoad.value = true; pErr.value = ""; pRes.value = null; reported.value = false;
  try { pRes.value = await checkPhone(phone.value); } catch (e) { pErr.value = "查詢失敗：" + e.message; } finally { pLoad.value = false; }
}
async function reportPhone() {
  try { await report("phone", phone.value, "使用者回報"); reported.value = true; } catch (e) { pErr.value = e.message; }
}

// ── 截圖 OCR ──
const ocrText = ref(""); const ocrStatus = ref(""); const iRes = ref(null); const iLoad = ref(false);
async function onFile(ev) {
  const file = ev.target.files?.[0];
  if (!file) return;
  ocrText.value = ""; iRes.value = null; ocrStatus.value = "載入文字辨識引擎…"; iLoad.value = true;
  try {
    const T = await import("https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.esm.min.js");
    ocrStatus.value = "辨識圖片文字中（首次需下載語言檔，請稍候）…";
    const { data } = await T.default.recognize(file, "chi_tra+eng");
    ocrText.value = (data.text || "").trim();
    if (ocrText.value) { ocrStatus.value = "辨識完成，分析中…"; iRes.value = await detect(ocrText.value); ocrStatus.value = ""; }
    else ocrStatus.value = "未辨識到文字，請換清楚一點的截圖，或改用『訊息偵測』貼上文字。";
  } catch (e) {
    ocrStatus.value = "文字辨識載入失敗，請改用『訊息偵測』直接貼上文字。（" + e.message + "）";
  } finally { iLoad.value = false; }
}

function ResultCard(r) { return r; } // placeholder for template clarity
</script>

<template>
  <div class="card">
    <h2>🔍 偵測中心</h2>
    <div class="subtabs">
      <button v-for="t in tabs" :key="t.k" :class="['st', { on: tab === t.k }]" @click="tab = t.k">{{ t.label }}</button>
    </div>

    <!-- 訊息 -->
    <div v-show="tab === 'text'">
      <p class="muted">貼上可疑訊息，AI（自訓模型 + Gemini）判斷是否詐騙並解釋理由。</p>
      <textarea v-model="text" placeholder="例如：老師帶單保證獲利30%，加LINE進VIP群…"></textarea>
      <div class="ex"><span class="muted">點一個真實範例試試：</span><br />
        <span v-for="e in examples" :key="e.t" class="chip" @click="text = e.v">{{ e.t }}</span>
      </div>
      <button class="btn" :disabled="tLoad || !text.trim()" @click="runText">{{ tLoad ? "分析中…" : "開始偵測" }}</button>
      <p v-if="tErr" class="err">{{ tErr }}</p>
    </div>

    <!-- 網址 -->
    <div v-show="tab === 'url'">
      <p class="muted">貼上網址，比對 165 官方涉詐網站清單 + 仿冒/可疑特徵分析。</p>
      <input v-model="url" class="inp" placeholder="例如：http://paypal-verify.top/login" />
      <div class="ex"><span class="muted">點一個範例試試：</span><br />
        <span v-for="e in urlEx" :key="e.t" class="chip" @click="url = e.v">{{ e.t }}</span>
      </div>
      <button class="btn" :disabled="uLoad || !url.trim()" @click="runUrl">{{ uLoad ? "檢查中…" : "檢查網址" }}</button>
      <p v-if="uErr" class="err">{{ uErr }}</p>
    </div>

    <!-- 電話 -->
    <div v-show="tab === 'phone'">
      <p class="muted">查號碼是否被社群回報為詐騙。⚠️ 官方電話開放資料已下架，本查詢為社群回報 + 風險提示。</p>
      <input v-model="phone" class="inp" placeholder="例如：+886912345678 或 0277123456" />
      <div class="ex"><span class="muted">點一個範例試試：</span><br />
        <span v-for="e in phoneEx" :key="e.t" class="chip" @click="phone = e.v">{{ e.t }}</span>
      </div>
      <button class="btn" :disabled="pLoad || !phone.trim()" @click="runPhone">{{ pLoad ? "查詢中…" : "查詢號碼" }}</button>
      <p v-if="pErr" class="err">{{ pErr }}</p>
    </div>

    <!-- 截圖 -->
    <div v-show="tab === 'image'">
      <p class="muted">上傳詐騙訊息「截圖」，自動辨識文字後偵測（適合長輩轉傳的圖）。</p>
      <input type="file" accept="image/*" @change="onFile" />
      <p v-if="ocrStatus" class="muted" style="margin-top:.6rem">{{ ocrStatus }}</p>
      <p v-if="ocrText" style="margin-top:.6rem"><strong>辨識到的文字：</strong>{{ ocrText.slice(0, 200) }}</p>
    </div>
  </div>

  <!-- 共用結果卡片 -->
  <div v-if="tab==='text' && tRes" class="card">
    <div class="vd" :style="{ background: badge[tRes.verdict]?.bg }">
      <span class="vl" :style="{ color: badge[tRes.verdict]?.color }">{{ badge[tRes.verdict]?.label || tRes.verdict }}</span>
      <span class="vc">風險 {{ pct(tRes) }}%</span>
    </div>
    <div class="bar"><div class="bf" :style="{ width: pct(tRes)+'%', background: badge[tRes.verdict]?.color }"></div></div>
    <p style="margin-top:1rem">{{ tRes.reasoning }}</p>
    <p class="muted sm">判定引擎：{{ tRes.engine }}</p>
    <template v-if="tRes.similar_examples?.length">
      <h4>資料庫中相似的歷史案例</h4>
      <ul class="sims"><li v-for="(ex,i) in tRes.similar_examples" :key="i"><span class="tg">{{ ex.scam_type || '一般' }}</span>{{ ex.content.slice(0,46) }}…</li></ul>
    </template>
  </div>

  <div v-if="tab==='image' && iRes" class="card">
    <div class="vd" :style="{ background: badge[iRes.verdict]?.bg }">
      <span class="vl" :style="{ color: badge[iRes.verdict]?.color }">{{ badge[iRes.verdict]?.label || iRes.verdict }}</span>
      <span class="vc">風險 {{ pct(iRes) }}%</span>
    </div>
    <p style="margin-top:1rem">{{ iRes.reasoning }}</p>
  </div>

  <div v-if="tab==='url' && uRes" class="card">
    <div class="vd" :style="{ background: badge[uRes.verdict]?.bg }">
      <span class="vl" :style="{ color: badge[uRes.verdict]?.color }">{{ badge[uRes.verdict]?.label || uRes.verdict }}</span>
      <span class="vc">風險 {{ pct(uRes) }}%</span>
    </div>
    <p class="muted sm" style="margin-top:.6rem">網域：{{ uRes.domain }}　·　已比對官方黑名單 {{ uRes.blocklist_size?.toLocaleString() }} 筆</p>
    <ul class="sims"><li v-for="(r,i) in uRes.reasons" :key="i">{{ r }}</li></ul>
  </div>

  <div v-if="tab==='phone' && pRes" class="card">
    <div class="vd" :style="{ background: badge[pRes.verdict]?.bg }">
      <span class="vl" :style="{ color: badge[pRes.verdict]?.color }">{{ badge[pRes.verdict]?.label || pRes.verdict }}</span>
      <span class="vc">風險 {{ pct(pRes) }}%</span>
    </div>
    <ul class="sims"><li v-for="(r,i) in pRes.reasons" :key="i">{{ r }}</li></ul>
    <p class="muted sm">{{ pRes.disclaimer }}</p>
    <button v-if="!reported" class="btn ghost" @click="reportPhone">🚩 回報此號碼為詐騙</button>
    <p v-else class="muted">✅ 已回報，謝謝你幫助大家！</p>
  </div>
</template>

<style scoped>
.subtabs { display: flex; gap: .4rem; flex-wrap: wrap; margin-bottom: 1rem; }
.st { background: #eef2ff; color: #3147b8; border: 1px solid #d9e0ff; border-radius: 999px; padding: .4rem .9rem; font-size: .95rem; font-weight: 600; }
.st.on { background: var(--brand); color: #fff; border-color: var(--brand); }
.inp { width: 100%; padding: .75rem 1rem; border: 1.5px solid var(--line); border-radius: 10px; font-size: 1.05rem; margin-bottom: .8rem; }
.inp:focus { outline: none; border-color: var(--brand); }
.ex { margin: .6rem 0; }
.err { color: var(--danger); margin-top: .8rem; }
.vd { display: flex; align-items: center; justify-content: space-between; padding: .9rem 1.1rem; border-radius: 10px; }
.vl { font-size: 1.3rem; font-weight: 800; }
.vc { color: var(--muted); font-weight: 700; }
.bar { height: 10px; background: #eef0f5; border-radius: 999px; margin-top: .6rem; overflow: hidden; }
.bf { height: 100%; border-radius: 999px; transition: width .4s; }
.sm { font-size: .82rem; }
.sims { list-style: none; padding: 0; margin: .5rem 0; }
.sims li { padding: .5rem 0; border-top: 1px solid var(--line); font-size: .95rem; }
.tg { display: inline-block; background: #eef2ff; color: #3147b8; border-radius: 6px; padding: .1rem .5rem; margin-right: .5rem; font-size: .8rem; }
.btn.ghost { background: #fff; color: var(--brand); border: 1.5px solid var(--brand); margin-top: .8rem; }
</style>
