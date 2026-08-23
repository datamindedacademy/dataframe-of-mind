<script setup lang="ts">
/** The 2000 to 2018 data processing milestones, as a horizontal timeline. */
const eras = [
  { year: '2000', label: 'Oracle & IBM', tone: 'navy' },
  { year: '2004', label: 'MapReduce', tone: 'navy' },
  { year: '2008', label: 'Hadoop', tone: 'navy' },
  { year: '2014', label: 'Spark', tone: 'violet' },
  { year: '2015', label: 'Snowflake', tone: 'violet' },
  { year: '2016', label: 'Databricks', tone: 'violet' },
  { year: '2018', label: 'Spark on Kubernetes', tone: 'violet' },
]
</script>

<template>
  <div class="era">
    <div class="era-rule" />
    <div class="era-row">
      <div v-for="e in eras" :key="e.year" class="era-item">
        <div class="era-dot" :class="`era-dot--${e.tone}`" />
        <div class="era-year">{{ e.year }}</div>
        <div class="era-label">{{ e.label }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.era { position: relative; margin-top: 40px; }
.era-rule { height: 3px; background: var(--dm-connecting); opacity: 0.35; margin: 0 12px; }
.era-row { display: flex; justify-content: space-between; margin-top: -9px; }
.era-item { flex: 1; text-align: center; }
.era-dot { width: 15px; height: 15px; border-radius: 50%; margin: 0 auto; }
.era-dot--navy { background: var(--dm-premium); }
.era-dot--violet { background: var(--dm-connecting); }
.era-year { font-weight: 700; margin-top: 10px; }
.era-label { font-size: 14px; opacity: 0.8; }
</style>
