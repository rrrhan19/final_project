<script setup>
defineProps({ name: String });
// 一致風格情境插畫：暖橘 #e8743b、安定綠 #2f8f76、米白底、線寬2.4 圓頭（與 HeroArt 同語言）
</script>
<template>
  <svg viewBox="0 0 120 100" fill="none" class="scam-art" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="60" cy="50" r="42" fill="#fde9dc" />
    <!-- 假投資：上升假線圖 + 餌 -->
    <g v-if="name==='invest'" stroke="#3a2c20">
      <path d="M38 64l10-12 8 6 14-20" stroke="#e8743b" />
      <circle cx="80" cy="38" r="3" fill="#e8743b" stroke="#e8743b" />
      <path d="M38 70h44" /><path d="M38 64V34" />
      <path d="M50 34c0-6 14-6 14 0" stroke="#d2452f" />
    </g>
    <!-- 假檢警：警徽盾 + 話筒 -->
    <g v-else-if="name==='gov'" stroke="#3a2c20">
      <path d="M60 30l12 5v10c0 9-6 14-12 16-6-2-12-7-12-16V35l12-5Z" fill="rgba(210,69,47,.15)" stroke="#d2452f" />
      <path d="M55 47l3 3 7-7" stroke="#d2452f" />
    </g>
    <!-- ATM：機台 + 卡 -->
    <g v-else-if="name==='atm'" stroke="#3a2c20">
      <rect x="44" y="30" width="32" height="42" rx="4" fill="#fff" />
      <rect x="50" y="36" width="20" height="9" rx="2" fill="#fde9dc" />
      <path d="M50 52h8M50 58h12" stroke="#e8743b" />
      <rect x="70" y="62" width="14" height="9" rx="2" fill="#e8743b" stroke="#e8743b" />
    </g>
    <!-- 假網拍：購物車 + 價標 -->
    <g v-else-if="name==='cart'" stroke="#3a2c20">
      <path d="M42 38h6l4 22h22l4-14H52" stroke="#e8743b" />
      <circle cx="56" cy="68" r="3" /><circle cx="72" cy="68" r="3" />
      <path d="M68 32l10 2 1 8-8 4-5-9 2-5Z" fill="#fff" /><circle cx="71" cy="37" r="1.5" fill="#d2452f" />
    </g>
    <!-- 假交友：愛心對話泡 -->
    <g v-else-if="name==='love'" stroke="#3a2c20">
      <path d="M44 36h26a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4H54l-8 6v-6a4 4 0 0 1-2-4V40a4 4 0 0 1 4-4Z" fill="#fff" />
      <path d="M57 42s-5-3-5 1 5 6 5 6 5-2 5-6-5-1-5-1Z" fill="#e8743b" stroke="#e8743b" />
      <path d="M70 64c4 0 6 3 6 6" stroke="#d2452f" />
    </g>
    <!-- 釣魚簡訊：信封 + 鉤 -->
    <g v-else-if="name==='sms'" stroke="#3a2c20">
      <rect x="40" y="40" width="36" height="26" rx="3" fill="#fff" />
      <path d="M40 42l18 13 18-13" />
      <path d="M84 28c0 14-12 10-12 22a6 6 0 0 0 12 0" stroke="#d2452f" /><circle cx="84" cy="26" r="3" fill="#d2452f" stroke="#d2452f" />
    </g>
    <!-- 預設盾 -->
    <g v-else stroke="#2f8f76">
      <path d="M60 32l12 5v10c0 9-6 14-12 16-6-2-12-7-12-16V37l12-5Z" fill="rgba(47,143,118,.15)" />
      <path d="M54 49l4 4 9-9" />
    </g>
  </svg>
</template>
<style scoped>.scam-art { width: 100%; max-width: 120px; height: auto; }</style>
