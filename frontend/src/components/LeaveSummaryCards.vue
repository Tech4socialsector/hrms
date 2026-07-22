<template>
	<div class="flex flex-col gap-3 w-full">
		<div class="text-lg font-medium text-gray-900">{{ __("My Leave Summary") }}</div>
		<div class="grid grid-cols-2 gap-3">
			<div
				v-for="card in cards"
				:key="card.title"
				class="flex flex-col bg-white rounded-lg p-4 gap-2"
			>
				<div
					class="flex items-center justify-center h-8 w-8 rounded"
					:class="card.iconBg"
				>
					<FeatherIcon :name="card.icon" class="h-4 w-4" :class="card.iconColor" />
				</div>
				<div class="text-xs text-gray-600">{{ card.title }}</div>
				<div class="text-xl font-bold text-gray-900">{{ card.value }}</div>
				<div class="text-xs text-gray-500">{{ card.subtitle }}</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed, inject } from "vue"
import { FeatherIcon } from "frappe-ui"

import { leaveBalance, myLeaves } from "@/data/leaves"

const __ = inject("$translate")

const availableBalance = computed(() => {
	if (!leaveBalance.data) return 0
	return Object.values(leaveBalance.data).reduce(
		(total, allocation) => total + (allocation.balance_leaves || 0),
		0
	)
})

const leavesTaken = computed(() => {
	if (!leaveBalance.data) return 0
	return Object.values(leaveBalance.data).reduce(
		(total, allocation) =>
			total + ((allocation.allocated_leaves || 0) - (allocation.balance_leaves || 0)),
		0
	)
})

const pendingApplications = computed(() => {
	if (!myLeaves.data) return 0
	return myLeaves.data.filter((leave) => leave.status === "Open").length
})

const approvedLeaves = computed(() => {
	if (!myLeaves.data) return 0
	return myLeaves.data.filter((leave) => leave.status === "Approved").length
})

const cards = computed(() => [
	{
		title: __("Available Leave Balance"),
		value: __("{0} Days", [availableBalance.value]),
		subtitle: __("Across all leave types"),
		icon: "calendar",
		iconBg: "bg-green-100",
		iconColor: "text-green-600",
	},
	{
		title: __("Leaves Taken This Year"),
		value: __("{0} Days", [leavesTaken.value]),
		subtitle: __("Till date"),
		icon: "bar-chart-2",
		iconBg: "bg-blue-100",
		iconColor: "text-blue-600",
	},
	{
		title: __("Pending Applications"),
		value: pendingApplications.value,
		subtitle: __("Awaiting Approval"),
		icon: "clock",
		iconBg: "bg-orange-100",
		iconColor: "text-orange-600",
	},
	{
		title: __("Approved Leaves"),
		value: approvedLeaves.value,
		subtitle: __("This Year"),
		icon: "check-circle",
		iconBg: "bg-purple-100",
		iconColor: "text-purple-600",
	},
])
</script>
