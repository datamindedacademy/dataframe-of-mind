<script setup lang="ts">
defineProps<{ label?: string }>()
</script>

<template>
  <div class="slidev-layout dm-default">
    <div v-if="label" class="dm-section-label">{{ label }}</div>
    <div class="dm-default-body">
      <slot />
    </div>
    <DmFooter :page="true" />
  </div>
</template>

<style scoped>
.dm-default {
  background: #ffffff;
  padding: 44px 56px 48px;
  height: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}
/* The body claims the whole area under the title bar so it has a height to
   centre against. min-height: 0 lets an over-full slide shrink instead of
   pushing the footer off the page. */
.dm-default-body {
  flex: 1 1 auto;
  min-height: 0;
  display: flex;
  flex-direction: column;
}
/* The first heading becomes the title with the signature hairline rule.
   padding-right keeps long two-line titles clear of the top-right section label. */
.dm-default-body :deep(h1:first-child) {
  border-bottom: 1px solid rgba(8, 6, 53, 0.85);
  padding-bottom: 12px;
  margin-bottom: 24px;
  width: 100%;
  padding-right: 120px;
  box-sizing: border-box;
}
/* Vertical centring. The title stays pinned under the top padding, where the
   hairline rule lines up from slide to slide; everything after it is one block
   that sits in the middle of the leftover height instead of hanging from the
   title. Two auto margins share the free space evenly, and both collapse to
   zero on a slide that already fills the page, so full slides are untouched. */
.dm-default-body :deep(> *) {
  flex: 0 0 auto;
}
/* !important because several content blocks in style.css set their own margins
   that way, and the two spacers have to win for the centring to hold. */
.dm-default-body :deep(> h1:first-child + *) {
  margin-top: auto !important;
}
.dm-default-body :deep(> :last-child) {
  margin-bottom: auto !important;
}
/* When one wrapper element holds the whole body, its own outermost children sit
   flush against the wrapper's edges, and a margin there is inside the box being
   centred: it shifts the visible content without shifting the box. Zero it. */
.dm-default-body :deep(> h1:first-child + :last-child > :first-child) {
  margin-top: 0 !important;
}
.dm-default-body :deep(> h1:first-child + :last-child > :last-child) {
  margin-bottom: 0 !important;
}
</style>
