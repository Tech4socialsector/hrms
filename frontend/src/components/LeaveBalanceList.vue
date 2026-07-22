<template>
	<div class="flex flex-col gap-3 w-full" v-if="leaveBalance.data">
		<div class="text-lg font-medium text-gray-900">{{ __("My Leave Balance") }}</div>
		<div class="flex flex-col bg-white rounded-lg">
			<div
				class="flex flex-row items-center justify-between p-4"
				:class="index !== leaveTypes.length - 1 && 'border-b'"
				v-for="(allocation, leave_type, index) in leaveBalance.data"
				:key="leave_type"
			>
				<div class="text-base font-normal text-gray-800">
					{{ __(leave_type, null, "Leave Type") }}
				</div>
				<div class="text-base font-medium text-gray-900">
					{{ __("{0} Days", [allocation.balance_leaves]) }}
				</div>
			</div>
		</div>
	</div>
	<EmptyState :message="__('You have no leaves allocated')" v-else />
</template>

<script setup>
import { computed, inject } from "vue"

import { leaveBalance } from "@/data/leaves"

const __ = inject("$translate")

const leaveTypes = computed(() =>
	leaveBalance.data ? Object.keys(leaveBalance.data) : []
)
</script>
