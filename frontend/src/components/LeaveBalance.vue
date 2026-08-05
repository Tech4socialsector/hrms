<template>
	<div class="flex flex-col w-full">
		<div class="flex flex-row justify-between items-center px-4">
			<div class="text-lg text-gray-800 font-bold">{{ __("Leave Balance") }} </div>
			<router-link
				:to="{ name: 'LeaveApplicationListView' }"
				v-slot="{ navigate }"
				v-if="leaveBalance.data"
			>
				<div
					@click="navigate"
					class="text-sm text-gray-800 font-semibold cursor-pointer underline underline-offset-2"
				>
					{{ __("View Leave History") }}
				</div>
			</router-link>
		</div>

		<!-- Leave Balance Dashboard -->
		<div class="flex flex-col gap-3 mx-4 mt-3" v-if="leaveBalance.data">
			<div class="grid grid-cols-2 gap-3">
				<div
					v-for="row in leaveRows"
					:key="row.leave_type"
					class="flex flex-row items-center gap-2.5 bg-white rounded-lg p-3"
				>
					<div
						class="flex items-center justify-center h-8 w-8 rounded-lg shrink-0"
						:style="{ backgroundColor: row.color + '1a' }"
					>
						<FeatherIcon name="calendar" class="h-4 w-4" :color="row.color" />
					</div>
					<div class="flex flex-col min-w-0">
						<div class="text-sm font-medium text-gray-900 truncate">
							{{ __(row.leave_type, null, "Leave Type") }}
						</div>
						<div class="text-xs text-gray-500">
							{{ __("{0}/{1} available", [row.balance_leaves, row.allocated_leaves]) }}
						</div>
					</div>
				</div>
			</div>

			<div class="flex flex-row items-center justify-between bg-white rounded-lg px-4 py-3">
				<div class="flex flex-col">
					<div class="text-base font-bold text-gray-900">{{ totals.allocated }}</div>
					<div class="text-xs text-gray-500">{{ __("Total Leave Days") }}</div>
				</div>
				<div class="flex flex-col items-center">
					<div class="text-base font-bold text-gray-900">{{ totals.used }}</div>
					<div class="text-xs text-gray-500">{{ __("Used") }}</div>
				</div>
				<div class="flex flex-col items-center">
					<div class="text-base font-bold text-gray-900">{{ totals.available }}</div>
					<div class="text-xs text-gray-500">{{ __("Available") }}</div>
				</div>
				<div class="flex flex-col items-end">
					<div class="text-base font-bold text-gray-900">{{ totals.pending }}</div>
					<div class="text-xs text-gray-500">{{ __("Pending") }}</div>
				</div>
			</div>
		</div>

		<EmptyState :message="__('You have no leaves allocated')" v-else />

		<LeaveAdjustments />
	</div>
</template>

<script setup>
import { computed, inject } from "vue"
import { FeatherIcon } from "frappe-ui"

import LeaveAdjustments from "@/components/LeaveAdjustments.vue"
import { leaveBalance, myLeaves } from "@/data/leaves"

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

const leaveRows = computed(() => {
	if (!leaveBalance.data) return []
	return Object.entries(leaveBalance.data).map(([leave_type, allocation], index) => {
		const allocated = allocation.allocated_leaves || 0
		const balance = allocation.balance_leaves || 0
		const used = Math.max(allocated - balance, 0)
		return {
			leave_type,
			allocated_leaves: allocated,
			balance_leaves: balance,
			used_leaves: used,
			color: getChartColor(index),
		}
	})
})

const totals = computed(() => {
	const allocated = leaveRows.value.reduce((sum, row) => sum + row.allocated_leaves, 0)
	const available = leaveRows.value.reduce((sum, row) => sum + row.balance_leaves, 0)
	const used = leaveRows.value.reduce((sum, row) => sum + row.used_leaves, 0)
	const pending = myLeaves.data
		? myLeaves.data.filter((leave) => leave.status === "Open").length
		: 0

	return { allocated, available, used, pending }
})
</script>
