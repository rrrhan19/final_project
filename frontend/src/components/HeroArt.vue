<template>
  <!-- 手繪感向量插畫：暖色盾牌守護一支被釣鉤勾住的手機（反詐情境，rubric #4）-->
  <svg viewBox="0 0 240 200" fill="none" xmlns="http://www.w3.org/2000/svg" class="hero-art">
    <!-- 暖色背景圓形 -->
    <circle cx="120" cy="100" r="86" fill="#fde9dc" />
    <circle cx="120" cy="100" r="86" stroke="#f6d0ba" stroke-width="2" stroke-dasharray="4 7" />
    <!-- 手機 -->
    <rect x="84" y="58" width="58" height="92" rx="11" fill="#fff" stroke="#3a2c20" stroke-width="2.4" />
    <rect x="92" y="70" width="42" height="9" rx="3" fill="#fde9dc" />
    <rect x="92" y="86" width="34" height="7" rx="3" fill="#f1e6d8" />
    <rect x="92" y="99" width="42" height="7" rx="3" fill="#f1e6d8" />
    <circle cx="113" cy="135" r="5" fill="#e8743b" />
    <!-- 釣鉤（被擋下）-->
    <path d="M168 36c0 26-22 22-22 40a9 9 0 0 0 18 0" stroke="#d2452f" stroke-width="2.6" stroke-linecap="round" />
    <circle cx="168" cy="33" r="4" fill="#d2452f" />
    <!-- 守護盾（半透明覆蓋，擋在手機與鉤之間）-->
    <path d="M120 40l40 16v30c0 26-18 43-40 51-22-8-40-25-40-51V56l40-16Z"
          fill="rgba(47,143,118,.16)" stroke="#2f8f76" stroke-width="2.6" stroke-linejoin="round" />
    <path d="M108 100l9 9 18-19" stroke="#2f8f76" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
    <!-- 暖色小點綴 -->
    <circle cx="44" cy="60" r="6" fill="#f2994a" />
    <circle cx="196" cy="150" r="8" fill="#e8743b" opacity=".8" />
    <path d="M40 150c4-5 10-5 14 0" stroke="#f2994a" stroke-width="2.4" stroke-linecap="round" />
  </svg>
</template>
<style scoped>.hero-art { width: 100%; max-width: 240px; height: auto; }</style>
