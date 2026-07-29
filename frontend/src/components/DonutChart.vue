<template>
	<svg viewBox="0 0 48 48" class="h-full w-full -rotate-90">
		<circle
			class="stroke-current text-gray-100"
			cx="24"
			cy="24"
			r="20"
			fill="transparent"
			stroke-width="7"
		></circle>
		<circle
			v-for="segment in segments"
			:key="segment.key"
			:stroke="segment.color"
			cx="24"
			cy="24"
			r="20"
			fill="transparent"
			stroke-width="7"
			stroke-linecap="round"
			:stroke-dasharray="`${segment.arcLength} ${circumference - segment.arcLength}`"
			:stroke-dashoffset="segment.dashOffset"
		></circle>
	</svg>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
	// [{ key, value, color }]
	data: {
		type: Array,
		default: () => [],
	},
})

const circumference = 2 * Math.PI * 20
// small visual gap between adjacent segments, in circumference units
const GAP = 2

const total = computed(() =>
	props.data.reduce((sum, item) => sum + (item.value || 0), 0)
)

const segments = computed(() => {
	if (!total.value) return []

	let cumulative = 0
	return props.data
		.filter((item) => item.value > 0)
		.map((item) => {
			const fraction = item.value / total.value
			const arcLength = Math.max(fraction * circumference - GAP, 0)
			// dashoffset shifts the arc's start point backwards around the circle
			const dashOffset = -cumulative * circumference
			cumulative += fraction

			return {
				key: item.key,
				color: item.color,
				arcLength,
				dashOffset,
			}
		})
})
</script>
