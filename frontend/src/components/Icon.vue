<script setup>
// 統一線性 icon 系統：同 viewBox、同線寬、圓頭線端（暖人文調性）
const props = defineProps({ name: String, size: { type: [Number, String], default: 22 } });
const paths = {
  home: ["M3 11.5 12 4l9 7.5", "M5 10v9h14v-9", "M10 19v-5h4v5"],
  detect: ["M11 4a7 7 0 1 0 0 14 7 7 0 0 0 0-14Z", "M16 16l4.5 4.5", "M8.5 11h5M11 8.5v5"],
  chat: ["M4 5h16v11H9l-4 3v-3H4Z", "M8 10h8M8 13h5"],
  game: ["M7 8h10a4 4 0 0 1 4 4v0a4 4 0 0 1-4 4c-1.5 0-2.2-1-3-2H10c-.8 1-1.5 2-3 2a4 4 0 0 1-4-4v0a4 4 0 0 1 4-4Z", "M7 11v3M5.5 12.5h3", "M16 12h.01M18 14h.01"],
  intel: ["M4 20V10M9 20V4M14 20v-7M19 20V8"],
  help: ["M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18Z", "M9.2 9.2a2.8 2.8 0 0 1 5.4 1c0 1.8-2.6 2.3-2.6 4", "M12 17.5h.01"],
  heart: ["M12 20s-7-4.5-9.2-8.6C1.2 8.3 2.6 5 5.8 5 8 5 9.3 6.4 12 9c2.7-2.6 4-4 6.2-4 3.2 0 4.6 3.3 3 6.4C19 15.5 12 20 12 20Z"],
  shield: ["M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6l7-3Z", "M9 12l2 2 4-4"],
  phone: ["M6 3h4l2 5-3 2a12 12 0 0 0 5 5l2-3 5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 4 5a2 2 0 0 1 2-2Z"],
  link: ["M10 13a4 4 0 0 0 6 .5l2-2a4 4 0 0 0-6-6l-1 1", "M14 11a4 4 0 0 0-6-.5l-2 2a4 4 0 0 0 6 6l1-1"],
  alert: ["M12 4l9 16H3L12 4Z", "M12 10v4", "M12 17h.01"],
  book: ["M5 4h11a2 2 0 0 1 2 2v14H7a2 2 0 0 0-2 2V4Z", "M5 4v18", "M9 8h6M9 11h5"],
  trophy: ["M7 4h10v4a5 5 0 0 1-10 0V4Z", "M7 6H4v1a3 3 0 0 0 3 3M17 6h3v1a3 3 0 0 1-3 3", "M10 14h4M9 20h6M12 14v6"],
  spark: ["M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3Z"],
};
</script>
<template>
  <svg :width="size" :height="size" viewBox="0 0 24 24" fill="none"
       stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
       aria-hidden="true" class="icon">
    <path v-for="(d, i) in paths[name]" :key="i" :d="d" />
  </svg>
</template>
<style scoped>.icon { display: inline-block; vertical-align: -0.18em; }</style>
