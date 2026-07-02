<template>
  <div class="card">
    <h2>💙 我們為什麼做這個</h2>
    <p>
      詐騙不只是數字。每一件背後，可能是一位把退休金匯出去的長輩、一個相信「穩賺不賠」的年輕人、
      一段被假感情掏空的關係。當我們查資料時看到「2024 年財損 502 億」，想到的不是統計，是 12 萬個受傷的人。
    </p>
    <p>
      我們是學生，能做的有限，但我們相信科技可以站在受害者這一邊——
      讓辨識詐騙不再需要專業知識，只要把可疑訊息貼上來，就有人（和 AI）幫你看一眼。
    </p>
    <p class="quote">「如果這個工具能讓哪怕一個人，在按下匯款前多停三秒——它就值得做。」</p>
  </div>

  <div class="card">
    <h2>🛠️ 我們怎麼做的</h2>
    <ul>
      <li><strong>真實資料</strong>：偵測模型用內政部警政署 165 反詐騙開放資料訓練，不是憑空想像。</li>
      <li><strong>AI 是放大器</strong>：自訓詐騙分類器負責判斷、Google Gemini 負責解釋為什麼，讓結果看得懂。</li>
      <li><strong>守法與尊重</strong>：爬蟲遵守 robots.txt、資料入庫前去除個資，只用公開合法來源。</li>
      <li><strong>誠實</strong>：模型基於有限樣本，我們在介面標明限制與資料來源，不誇大。</li>
    </ul>
  </div>

  <div class="card">
    <h2>🌱 未來</h2>
    <p>
      希望這不只是期末專題：未來可串接更多官方資料源、做成手機 App 與長輩衛教教材、
      甚至接上邊緣裝置（Jetson + 攝像頭）在現場即時辨識可疑畫面。讓防詐，離每個人更近一點。
    </p>
  </div>
</template>

<style scoped>
.card p { line-height: 1.9; }
.quote { font-size: 1.15rem; font-weight: 700; color: var(--brand); border-left: 4px solid var(--brand); padding-left: 1rem; }
ul { line-height: 2; }
</style>
