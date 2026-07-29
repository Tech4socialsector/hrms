<template>
	<div class="flex flex-col gap-3 w-full" v-if="leaveBalance.data">
		<div class="text-lg font-medium text-gray-900">{{ __("My Leave Balance") }}</div>
		<div class="flex flex-row items-center gap-5 bg-white rounded-lg p-4">
			<div class="relative flex items-center justify-center h-28 w-28 shrink-0">
				<DonutChart :data="chartData" />
				<div class="absolute flex flex-col items-center">
					<div class="text-xl font-bold text-gray-900">{{ totalBalance }}</div>
					<div class="text-[11px] text-gray-500">{{ __("Days") }}</div>
				</div>
			</div>
			<div class="flex flex-col gap-2 grow min-w-0">
				<div
					v-for="(allocation, leave_type, index) in leaveBalance.data"
					:key="leave_type"
					class="flex flex-row items-center gap-2"
				>
					<span
						class="h-2.5 w-2.5 rounded-full shrink-0"
						:style="{ backgroundColor: getChartColor(index) }"
					></span>
					<div class="text-xs text-gray-600 truncate grow">
						{{ __(leave_type, null, "Leave Type") }}
					</div>
					<div class="text-xs font-medium text-gray-900 shrink-0">
						{{ allocation.balance_leaves }}
					</div>
				</div>
			</div>
		</div>
	</div>
	<EmptyState :message="__('You have no leaves allocated')" v-else />
</template>

<script setup>
import { computed, inject } from "vue"

import DonutChart from "@/components/DonutChart.vue"
import { leaveBalance } from "@/data/leaves"

const __ = inject("$translate")

// note: tw colors - rose-400, pink-400, purple-500, amber-400, teal-400, sky-400
const chartColors = [
	"#fb7185",
	"#f472b6",
	"#918ef5",
	"#fbbf24",
	"#2dd4bf",
	"#38bdf8",
]

const getChartColor = (index) => chartColors[index % chartColors.length]

const chartData = computed(() => {
	if (!leaveBalance.data) return []
	return Object.entries(leaveBalance.data).map(([leave_type, allocation], index) => ({
		key: leave_type,
		value: allocation.balance_leaves || 0,
		color: getChartColor(index),
	}))
})

const totalBalance = computed(() => {
	if (!leaveBalance.data) return 0
	return Object.values(leaveBalance.data).reduce(
		(total, allocation) => total + (allocation.balance_leaves || 0),
		0
	)
})
</script>
