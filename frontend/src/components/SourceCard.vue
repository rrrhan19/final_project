<script setup>
import Icon from "./Icon.vue";
defineProps({
  label: { type: String, required: true },
  sub: { type: String, default: "" },
  href: { type: String, required: true },
  icon: { type: String, default: "link" },
});
</script>
<template>
  <a class="gov-card" :href="href" target="_blank" rel="noopener">
    <span class="g-ic"><Icon :name="icon" :size="22" /></span>
    <span><span class="g-t">{{ label }}</span><br /><span class="g-s">{{ sub }} ↗</span></span>
  </a>
</template>
<style scoped>
.g-ic { width: 40px; height: 40px; border-radius: 12px; background: #e7f3ee; color: var(--accent); display: grid; place-items: center; flex-shrink: 0; }
</style>
