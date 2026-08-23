<script setup lang="ts">
/**
 * The pick-two trade-off: three properties at the corners, and every tool sitting on the
 * edge between the two properties it satisfies. Tools below the bottom edge are cheap and
 * simple but do not scale out; the further below, the less they scale.
 * Geometry taken from slides 41 and 42 of the original deck (scaled by 0.82). The click adds
 * the single node wave. The original also put a MapReduce pill on the left edge here; it is
 * dropped, since it is neither emerging nor single node. It stays on the 2004 timeline.
 */
const corners = [
  { emoji: '📈', label: 'Scalable', cx: 284, cy: 51, lx: 284, ly: 12 },
  { emoji: '💰', label: 'Cost-efficient', cx: 126, cy: 251, lx: 54, ly: 292 },
  { emoji: '💆', label: 'Simple', cx: 448, cy: 249, lx: 520, ly: 288 },
]
// on an edge: satisfies the two corners that edge connects
const established = [
  { label: 'Snowflake', x: 403, y: 102 },
  { label: 'Spark on k8s', x: 152, y: 123 },
  { label: 'Databricks', x: 440, y: 141 },
  { label: 'pandas', x: 287, y: 337 },
]
const emerging = [
  { label: 'Polars', x: 287, y: 267 },
  { label: 'DuckDB', x: 287, y: 302 },
]
</script>

<template>
  <div class="tri">
    <svg class="tri-edges" viewBox="0 0 580 360">
      <g stroke="var(--dm-connecting)" stroke-width="3" opacity="0.55">
        <line x1="284" y1="51" x2="126" y2="251" />
        <line x1="284" y1="51" x2="448" y2="249" />
        <line x1="126" y1="251" x2="448" y2="249" />
      </g>
      <circle v-for="c in corners" :key="c.label"
              :cx="c.cx" :cy="c.cy" r="25" fill="var(--dm-authentic)"
              stroke="var(--dm-connecting)" stroke-width="2" />
    </svg>

    <div v-for="c in corners" :key="`e-${c.label}`" class="tri-emoji"
         :style="{ left: `${c.cx}px`, top: `${c.cy}px` }">{{ c.emoji }}</div>
    <div v-for="c in corners" :key="`l-${c.label}`" class="tri-corner"
         :style="{ left: `${c.lx}px`, top: `${c.ly}px` }">{{ c.label }}</div>

    <div v-for="t in established" :key="t.label" class="tri-pill"
         :style="{ left: `${t.x}px`, top: `${t.y}px` }">{{ t.label }}</div>

    <div v-click>
      <div v-for="t in emerging" :key="t.label" class="tri-pill"
           :style="{ left: `${t.x}px`, top: `${t.y}px` }">{{ t.label }}</div>
    </div>
  </div>
</template>

<style scoped>
.tri { position: relative; width: 580px; height: 360px; margin: 12px auto 0; }
.tri-edges { position: absolute; inset: 0; width: 580px; height: 360px; }
.tri-emoji {
  position: absolute; transform: translate(-50%, -50%);
  font-size: 22px; line-height: 1;
}
.tri-corner {
  position: absolute; transform: translate(-50%, -50%);
  font-weight: 700; font-size: 16px; white-space: nowrap;
}
.tri-pill {
  position: absolute; transform: translate(-50%, -50%);
  min-width: 110px; padding: 5px 10px;
  border-radius: 9999px; text-align: center; white-space: nowrap;
  font-size: 14px; font-weight: 600;
  background: #fff; color: var(--dm-premium);
  border: 2px solid var(--dm-premium);
}
</style>
