<script setup>
import { ref, onMounted, computed } from "vue";
import { getAlerts, getStats } from "../api.js";
import { scams } from "../data/scams.js";
import ScamArt from "../components/ScamArt.vue";
import SourceCard from "../components/SourceCard.vue";
import Icon from "../components/Icon.vue";

const alerts = ref([]); const alertSrc = ref(""); const stats = ref(null); const err = ref("");
const open = ref(scams[0].id);

onMounted(async () => {
  try { const a = await getAlerts(8); alerts.value = a.alerts; alertSrc.value = a.source; } catch (e) {}
  try { stats.value = await getStats(2020, 2025); } catch (e) { err.value = "統計載入失敗：" + e.message; }
});

const maxYear = computed(() => stats.value?.by_year?.length ? Math.max(...stats.value.by_year.map(y => y.case_count)) : 1);
const sampleCount = (statType) => {
  const m = stats.value?.by_sample_type?.find(t => t.scam_type === statType);
  return m ? m.count : 0;
};
const toYi = (n) => n ? (n / 1e8).toFixed(0) + " 億" : "—";
function toggle(id) { open.value = open.value === id ? null : id; }
</script>

<template>
  <h1 class="page-h">詐騙情報中心</h1>
  <p class="page-sub muted">最新手法、官方數據，與六大詐騙的完整拆解——看懂套路，就不容易上當。</p>

  <div class="intel-layout">
    <!-- 主欄 -->
    <div class="main">
      <!-- 警示牆 -->
      <section class="card">
        <h2><Icon name="alert" :size="22" /> 最新詐騙手法警示牆</h2>
        <p class="muted srcline">{{ alertSrc || '載入中…' }}</p>
        <a v-for="(a, i) in alerts" :key="i" class="alert" :href="a.link || 'https://165.npa.gov.tw/'" target="_blank" rel="noopener">
          <span class="adate">{{ a.date }}</span>
          <span class="abody"><strong>{{ a.title }}</strong><span class="muted asum">{{ a.summary }}</span><span class="more">閱讀全文 ↗</span></span>
        </a>
        <p v-if="!alerts.length" class="muted">（警示資料載入中…）</p>
      </section>

      <!-- 手法圖鑑：左右交錯、可展開 -->
      <section class="card">
        <h2><Icon name="book" :size="22" /> 六大詐騙手法拆解</h2>
        <p class="muted">點任一種，讀懂它怎麼騙、怎麼防。</p>
        <article v-for="(s, idx) in scams" :key="s.id" class="scam" :class="{ rev: idx % 2 }">
          <div class="scam-art-wrap"><ScamArt :name="s.art" /></div>
          <div class="scam-body">
            <h3>{{ s.title }}</h3>
            <p class="oneliner">{{ s.oneLiner }}</p>
            <p class="collected">本平台已收集 <strong>{{ sampleCount(s.statType) }}</strong> 筆此類官方案例</p>
            <button class="btn ghost sm" @click="toggle(s.id)">{{ open === s.id ? '收合 ▲' : '看真實案例與自保 ▼' }}</button>

            <div v-if="open === s.id" class="detail">
              <p v-for="(p, k) in s.story" :key="k" class="story">{{ p }}</p>
              <h4>🎣 他們會這樣說</h4>
              <div v-for="(sc, k) in s.scripts" :key="k" class="bubble">「{{ sc }}」</div>
              <h4>🚩 破綻</h4>
              <ul><li v-for="(f, k) in s.redFlags" :key="k">{{ f }}</li></ul>
              <h4>🛡️ 怎麼自保</h4>
              <ul class="defend"><li v-for="(d, k) in s.defend" :key="k">{{ d }}</li></ul>
              <p class="realcase">📌 {{ s.realCase }}</p>
              <SourceCard :label="s.official.label" sub="官方資源" :href="s.official.href" icon="shield" />
            </div>
          </div>
        </article>
      </section>
    </div>

    <!-- 側欄（sticky）-->
    <aside class="side">
      <div class="card" v-if="stats">
        <h3><Icon name="intel" :size="20" /> 年度詐騙趨勢</h3>
        <div v-for="y in stats.by_year" :key="y.year" class="row">
          <span class="rl">{{ y.year }}</span>
          <div class="trk"><div class="fl" :style="{ width: (y.case_count/maxYear*100)+'%' }"></div></div>
          <span class="rv">{{ (y.case_count/10000).toFixed(1) }}萬</span>
        </div>
        <p class="note">2024：{{ stats.by_year.find(y=>y.year===2024)?.case_count.toLocaleString() }} 件、財損 {{ toYi(stats.by_year.find(y=>y.year===2024)?.loss_amount) }}。{{ stats.note }}</p>
      </div>
      <div class="card">
        <h3>看更多官方情報</h3>
        <div class="side-srcs">
          <SourceCard label="165 打詐儀錶板" sub="官方即時統計" href="https://165dashboard.tw/" icon="intel" />
          <SourceCard label="165 全民防騙網" sub="最新手法宣導" href="https://165.npa.gov.tw/" icon="link" />
        </div>
      </div>
      <div class="card help-card">
        <h3>已經遇到狀況？</h3>
        <p class="muted">別慌，先撥 165、保留證據、聯絡銀行圈存。</p>
        <RouterLink to="/help" class="btn ghost sm">看求助步驟 →</RouterLink>
      </div>
    </aside>
  </div>
</template>

<style scoped>
.page-h { margin: 0 0 .2rem; font-size: clamp(1.5rem, 3vw, 2.1rem); }
.page-sub { margin: 0 0 1.4rem; }
.intel-layout { display: grid; gap: 1.2rem; }
@media (min-width: 1024px) { .intel-layout { grid-template-columns: minmax(0, 1fr) 320px; align-items: start; } }
.side { display: flex; flex-direction: column; gap: 1.2rem; }
@media (min-width: 1024px) { .side { position: sticky; top: 70px; } }

.srcline { font-size: .8rem; }
.alert { display: flex; gap: .8rem; padding: .75rem 0; border-top: 1px solid var(--line); text-decoration: none; color: var(--ink); }
.alert:first-of-type { border-top: none; }
.alert:hover .more { opacity: 1; }
.adate { color: var(--brand-deep); font-size: .78rem; white-space: nowrap; font-weight: 700; padding-top: .2rem; }
.abody { display: flex; flex-direction: column; gap: .2rem; }
.asum { font-size: .88rem; }
.more { font-size: .8rem; color: var(--brand-deep); opacity: .6; }

.scam { display: flex; gap: 1.2rem; align-items: flex-start; padding: 1.2rem 0; border-top: 1px solid var(--line); }
.scam.rev { flex-direction: row-reverse; }
.scam-art-wrap { flex-shrink: 0; width: 120px; }
.scam-body { flex: 1; }
.scam-body h3 { margin: 0 0 .2rem; }
.oneliner { margin: 0 0 .4rem; color: var(--ink); font-weight: 600; }
.collected { font-size: .82rem; color: var(--accent); margin: 0 0 .6rem; }
.btn.sm { padding: .45rem 1rem; font-size: .9rem; }
.detail { margin-top: .9rem; padding-top: .9rem; border-top: 1px dashed var(--line); }
.detail h4 { margin: 1rem 0 .4rem; font-size: .98rem; }
.story { line-height: 1.9; margin: .3rem 0; }
.bubble { background: var(--cream-2); border: 1px solid var(--line); border-radius: 12px 12px 12px 3px; padding: .6rem .85rem; margin: .4rem 0; color: var(--danger); font-size: .95rem; }
.detail ul { margin: .2rem 0; padding-left: 1.2rem; line-height: 1.9; }
.defend li { color: var(--ok); }
.realcase { background: #fff7ec; border-left: 3px solid var(--warn); padding: .55rem .8rem; border-radius: 0 8px 8px 0; font-size: .9rem; margin: .8rem 0; }
@media (max-width: 560px) { .scam, .scam.rev { flex-direction: column; align-items: center; text-align: center; } .scam-body { text-align: left; } }

.row { display: flex; align-items: center; gap: .5rem; margin: .4rem 0; }
.rl { width: 2.6rem; font-weight: 700; font-size: .85rem; }
.trk { flex: 1; height: 14px; background: #f1e6d8; border-radius: 999px; overflow: hidden; }
.fl { height: 100%; background: var(--brand); border-radius: 999px; }
.rv { width: 3rem; text-align: right; font-size: .8rem; color: var(--ink-soft); }
.note { font-size: .76rem; color: var(--ink-soft); margin-top: .6rem; }
.side-srcs { display: flex; flex-direction: column; gap: .6rem; }
.help-card { background: #fff7ec; }
</style>
