<script setup>
import { RouterLink, RouterView } from "vue-router";
import Icon from "./components/Icon.vue";

const tabs = [
  { to: "/", label: "首頁", icon: "home" },
  { to: "/detect", label: "偵測中心", icon: "detect" },
  { to: "/chat", label: "AI問答", icon: "chat" },
  { to: "/game", label: "防詐練習", icon: "game" },
  { to: "/intel", label: "詐騙情報", icon: "intel" },
  { to: "/help", label: "我被騙了", icon: "help" },
  { to: "/about", label: "關於我們", icon: "heart" },
];
</script>

<template>
  <div class="app">
    <header class="topbar">
      <RouterLink to="/" class="brand">
        <!-- 品牌標誌：盾牌+心，與插畫同一套線條語言 -->
        <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6l7-3Z" fill="rgba(255,255,255,.15)" />
          <path d="M12 16s-3.2-2-3.2-4.2A1.8 1.8 0 0 1 12 10.4a1.8 1.8 0 0 1 3.2 1.4C15.2 14 12 16 12 16Z" fill="#fff" stroke="#fff" />
        </svg>
        <div>
          <div class="title">安心盾 <span class="tw">·防詐夥伴</span></div>
          <div class="subtitle">在按下匯款前，先讓我陪你看一眼</div>
        </div>
      </RouterLink>
    </header>

    <nav class="tabs">
      <div class="tabs-inner">
        <RouterLink v-for="t in tabs" :key="t.to" :to="t.to" class="tab" active-class="on">
          <Icon :name="t.icon" :size="19" /><span>{{ t.label }}</span>
        </RouterLink>
      </div>
    </nav>

    <main class="content"><RouterView /></main>

    <footer class="footer full-bleed">
      <div class="bleed-inner fcols">
        <div class="fbrand">
          <div class="title" style="color:var(--brand-deep)">安心盾 · 防詐夥伴</div>
          <p class="muted">偵測、學習、求助，陪你遠離詐騙。</p>
        </div>
        <div>
          <h4>功能</h4>
          <RouterLink to="/detect">偵測中心</RouterLink>
          <RouterLink to="/game">防詐練習</RouterLink>
          <RouterLink to="/intel">詐騙情報</RouterLink>
        </div>
        <div>
          <h4>求助管道</h4>
          <a href="tel:165">165 反詐騙專線</a>
          <a href="tel:110">110 報案</a>
          <RouterLink to="/help">我被騙了怎麼辦</RouterLink>
        </div>
        <div>
          <h4>官方資源</h4>
          <a href="https://165.npa.gov.tw/" target="_blank" rel="noopener">165 全民防騙網 ↗</a>
          <a href="https://165dashboard.tw/" target="_blank" rel="noopener">165 打詐儀錶板 ↗</a>
        </div>
      </div>
      <div class="bleed-inner fcopy">資料來源：內政部警政署 165 反詐騙開放資料　·　本平台為學生專題，僅供參考，遇詐請撥 165 查證。</div>
    </footer>
  </div>
</template>

<style>
:root {
  /* 暖人文色票（rubric #2：暖橘 × 米白，禁藍色冷調）*/
  --cream: #fbf6ee;
  --cream-2: #fffaf3;
  --card: #ffffff;
  --ink: #3a2c20;          /* 暖棕文字 */
  --ink-soft: #7a6a5b;
  --line: #efe3d3;
  --brand: #e8743b;        /* 暖橘 */
  --brand-deep: #c85a28;
  --brand-soft: #fde9dc;
  --accent: #2f8f76;       /* 安定綠（輔色）*/
  --danger: #d2452f;
  --warn: #e0982a;
  --ok: #2f8f76;
  --radius: 18px;
  --shadow: 0 10px 30px rgba(140,90,50,.10);
  /* 寬度軸線（rubric #3：填滿畫面、三層對齊同軸）*/
  --maxw: 1200px;
  --maxw-read: 720px;
  --gutter: clamp(1rem, 4vw, 2.5rem);
}
/* 全幅 band：背景滿版、內容置中 */
.full-bleed { width: 100vw; margin-inline: calc(50% - 50vw); }
.bleed-inner { max-width: var(--maxw); margin-inline: auto; padding-inline: var(--gutter); }
* { box-sizing: border-box; }
html, body { margin: 0; }
body {
  font-family: "Noto Sans TC", "Microsoft JhengHei", "PingFang TC", system-ui, sans-serif;
  background: var(--cream);
  color: var(--ink);
  font-size: 17px;
  line-height: 1.75;
}
.app { min-height: 100vh; display: flex; flex-direction: column; }

/* 頂部：暖橘，非藍漸層 */
.topbar { background: linear-gradient(120deg, #e8743b, #f2994a); color: #fff; padding: 1.05rem 1.25rem; }
.brand { display: flex; align-items: center; gap: .8rem; max-width: var(--maxw); margin: 0 auto; width: 100%; color: #fff; text-decoration: none; }
.title { font-size: 1.4rem; font-weight: 800; letter-spacing: .5px; }
.title .tw { font-size: .9rem; font-weight: 600; opacity: .9; }
.subtitle { font-size: .9rem; opacity: .92; }

/* 頁簽：米白底、暖橘選中，icon+字 */
.tabs { background: var(--cream-2); border-bottom: 1px solid var(--line); position: sticky; top: 0; z-index: 10; }
.tabs-inner { max-width: var(--maxw); margin: 0 auto; display: flex; gap: .2rem; flex-wrap: wrap; padding: .35rem var(--gutter); }
.tab { display: inline-flex; align-items: center; gap: .35rem; color: var(--ink-soft); text-decoration: none;
  padding: .5rem .75rem; border-radius: 999px; font-weight: 600; font-size: .95rem; transition: all .15s; white-space: nowrap; }
.tab:hover { background: var(--brand-soft); color: var(--brand-deep); }
.tab.on { background: var(--brand); color: #fff; }

.content { flex: 1; width: 100%; max-width: var(--maxw); margin: 1.8rem auto; padding-inline: var(--gutter); }
/* 長文閱讀區塊可在頁內自行收窄 */
.readable { max-width: var(--maxw-read); }
.footer { color: var(--ink-soft); padding: 2.4rem 0 1.4rem; font-size: .9rem; background: var(--cream-2); border-top: 1px solid var(--line); margin-top: 1.5rem; }
.fcols { display: grid; grid-template-columns: 1fr; gap: 1.4rem; }
@media (min-width: 720px) { .fcols { grid-template-columns: 1.6fr 1fr 1fr 1fr; } }
.footer h4 { margin: 0 0 .5rem; color: var(--ink); font-size: .95rem; }
.footer a { display: block; color: var(--ink-soft); text-decoration: none; padding: .15rem 0; }
.footer a:hover { color: var(--brand-deep); }
.fbrand .title { font-size: 1.15rem; font-weight: 800; }
.fcopy { font-size: .78rem; opacity: .85; margin-top: 1.4rem; padding-top: 1rem; border-top: 1px solid var(--line); }

/* 共用元件 */
.card { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: 1.4rem 1.5rem; box-shadow: var(--shadow); margin-bottom: 1.2rem; }
.card h2 { margin: 0 0 .5rem; font-size: 1.35rem; }
.card h3 { margin: 0 0 .6rem; }
.muted { color: var(--ink-soft); }
.btn { cursor: pointer; border: none; border-radius: 999px; padding: .72rem 1.5rem; background: var(--brand); color: #fff; font-size: 1.05rem; font-weight: 700; transition: filter .15s, transform .1s; box-shadow: 0 6px 16px rgba(232,116,59,.3); }
.btn:hover:not(:disabled) { filter: brightness(1.05); transform: translateY(-1px); }
.btn:disabled { opacity: .5; cursor: default; box-shadow: none; }
.btn.ghost { background: #fff; color: var(--brand-deep); border: 1.6px solid var(--brand); box-shadow: none; }
textarea, .inp { width: 100%; padding: .8rem 1rem; border: 1.6px solid var(--line); border-radius: 14px; font-size: 1.05rem; font-family: inherit; background: var(--cream-2); }
textarea { min-height: 110px; resize: vertical; }
textarea:focus, .inp:focus { outline: none; border-color: var(--brand); background: #fff; }
.chip { display: inline-block; cursor: pointer; user-select: none; background: var(--brand-soft); color: var(--brand-deep); border: 1px solid #f6d6c1; border-radius: 999px; padding: .35rem .8rem; margin: .25rem .3rem 0 0; font-size: .88rem; transition: background .12s; }
.chip:hover { background: #fbdcca; }

/* 官方資源連結卡（rubric #5）*/
.gov-card { display: flex; align-items: center; gap: .8rem; background: var(--cream-2); border: 1px solid var(--line); border-left: 4px solid var(--accent); border-radius: 12px; padding: .8rem 1rem; text-decoration: none; color: var(--ink); transition: transform .12s, box-shadow .12s; }
.gov-card:hover { transform: translateY(-2px); box-shadow: var(--shadow); }
.gov-card .g-emoji { font-size: 1.6rem; }
.gov-card .g-t { font-weight: 700; }
.gov-card .g-s { font-size: .82rem; color: var(--ink-soft); }
</style>
