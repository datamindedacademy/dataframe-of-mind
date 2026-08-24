<script setup lang="ts">
/**
 * Apache Arrow as the interchange layer: the engines above and around it, the
 * formats and clouds it reads from below. Positions follow slide 43 of the
 * original deck, scaled to fit a Slidev content area.
 */
const engines = [
  { src: '/img/logo-duckdb-badge.png', x: 157, y: 9, w: 62, alt: 'DuckDB' },
  { src: '/img/logo-polars-mark.png', x: 316, y: 12, w: 120, alt: 'Polars' },
  { src: '/img/logo-spark.png', x: 11, y: 110, w: 126, alt: 'Apache Spark' },
  { src: '/img/logo-pandas.png', x: 468, y: 118, w: 152, alt: 'pandas' },
]
const sources = [
  { src: '/img/icon-sqlstore.png', x: 113, y: 248, w: 40, alt: 'SQL databases' },
  { src: '/img/logo-parquet-mark.png', x: 202, y: 244, w: 58, alt: 'Parquet' },
  { src: '/img/logo-excel.png', x: 328, y: 252, w: 34, alt: 'Excel' },
  { src: '/img/icon-csv.png', x: 419, y: 248, w: 66, alt: 'CSV' },
  { src: '/img/logo-aws.png', x: 140, y: 296, w: 78, alt: 'AWS' },
  { src: '/img/logo-azure.png', x: 271, y: 302, w: 34, alt: 'Azure' },
  { src: '/img/logo-gcp.png', x: 376, y: 304, w: 58, alt: 'Google Cloud' },
]
// Arrow sits in the middle; everything wires through it.
const hub = { x: 227, y: 133, w: 150 }
const cx = hub.x + hub.w / 2
const cy = hub.y + 30
</script>

<template>
  <div class="hub">
    <svg class="hub-wires" viewBox="0 0 640 350">
      <g stroke="var(--dm-connecting)" stroke-width="2" opacity="0.4" fill="none">
        <line v-for="e in engines" :key="e.alt"
              :x1="cx" :y1="cy" :x2="e.x + e.w / 2" :y2="e.y + 34" />
        <line v-for="s in sources" :key="s.alt"
              :x1="cx" :y1="cy + 34" :x2="s.x + s.w / 2" :y2="s.y + 14" />
      </g>
    </svg>

    <img v-for="e in engines" :key="e.alt" class="hub-img"
         :src="e.src" :alt="e.alt" :style="{ left: `${e.x}px`, top: `${e.y}px`, width: `${e.w}px` }" />

    <img class="hub-img hub-arrow" src="/img/logo-arrow.png" alt="Apache Arrow"
         :style="{ left: `${hub.x}px`, top: `${hub.y}px`, width: `${hub.w}px` }" />

    <img v-for="s in sources" :key="s.alt" class="hub-img"
         :src="s.src" :alt="s.alt" :style="{ left: `${s.x}px`, top: `${s.y}px`, width: `${s.w}px` }" />
  </div>
</template>

<style scoped>
.hub { position: relative; width: 640px; height: 350px; margin: 8px auto 0; }
.hub-wires { position: absolute; inset: 0; width: 640px; height: 350px; }
.hub-img { position: absolute; height: auto; }
.hub-arrow { filter: drop-shadow(0 4px 14px rgba(84, 62, 220, 0.25)); }
</style>
