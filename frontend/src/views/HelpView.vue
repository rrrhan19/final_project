<template>
  <div class="card urgent">
    <h2>🆘 我可能被詐騙了，怎麼辦？</h2>
    <p>別慌、別自責，立刻照做能把損失降到最低：</p>
    <ol>
      <li><strong>立即撥打 165</strong> 反詐騙諮詢專線（24 小時），或 <strong>110</strong> 報案。</li>
      <li><strong>已匯款</strong>：馬上打給你的<strong>銀行客服</strong>或臨櫃辦理「<strong>圈存/警示帳戶</strong>」，越快越有機會攔截。</li>
      <li><strong>個資/帳號外洩</strong>：更改密碼、開啟雙重驗證，必要時辦理銀行帳戶約定轉帳關閉。</li>
      <li><strong>保留證據</strong>：截圖對話、匯款紀錄、對方帳號/電話，報案時提供。</li>
      <li>到 <strong>165 全民防騙網</strong> 線上檢舉，幫助阻止下一個受害者。</li>
    </ol>
  </div>

  <div class="card">
    <h2>📞 求助與檢舉管道</h2>
    <ul class="links">
      <li>📱 <strong>165 反詐騙專線</strong>：直撥 <a href="tel:165">165</a>（諮詢/檢舉/查證）</li>
      <li>🚓 <strong>報案專線</strong>：<a href="tel:110">110</a></li>
      <li>🌐 <strong>165 全民防騙網</strong>：<a href="https://165.npa.gov.tw/" target="_blank" rel="noopener">165.npa.gov.tw</a></li>
      <li>📊 <strong>165 打詐儀錶板</strong>：<a href="https://165dashboard.tw/" target="_blank" rel="noopener">165dashboard.tw</a></li>
    </ul>
  </div>

  <div class="card tips">
    <h2>🛡️ 三句保命口訣</h2>
    <p class="big">「保證獲利」是詐騙　·　「操作 ATM／安全帳戶」是詐騙　·　不確定就撥 165</p>
    <p class="muted">在按下匯款前，多停三秒、打給家人或 165 問一句，往往就能擋下整場詐騙。</p>
  </div>
</template>

<style scoped>
.urgent { border-left: 5px solid var(--danger); }
.urgent ol { line-height: 2; }
.links { list-style: none; padding: 0; line-height: 2.4; font-size: 1.05rem; }
.links a { color: var(--brand); font-weight: 700; }
.tips .big { font-size: 1.15rem; font-weight: 800; color: var(--brand); line-height: 1.9; }
</style>
