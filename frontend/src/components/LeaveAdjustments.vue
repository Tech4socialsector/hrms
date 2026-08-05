<template>
	<div class="flex flex-col w-full mt-5" v-if="leaveAdjustments.data?.length">
		<div class="flex flex-row justify-between items-center px-4">
			<div class="text-lg text-gray-800 font-bold">{{ __("Leave Adjustments") }}</div>
			<div
				v-if="leaveAdjustments.data.length > INLINE_LIMIT"
				id="open-leave-adjustment-list"
				class="text-sm text-gray-800 font-semibold cursor-pointer underline underline-offset-2"
			>
				{{ __("View All") }}
			</div>
		</div>

		<div class="flex flex-col gap-2 mx-4 mt-3">
			<LeaveAdjustmentRow v-for="row in inlineRows" :key="row.name" :row="row" />
		</div>
	</div>

	<ion-modal
		ref="modal"
		v-if="leaveAdjustments.data?.length > INLINE_LIMIT"
		trigger="open-leave-adjustment-list"
		:initial-breakpoint="1"
		:breakpoints="[0, 1]"
	>
		<div class="bg-white w-full flex flex-col items-center pb-5">
			<div class="w-full pt-8 pb-5 border-b text-center">
				<span class="text-gray-900 font-bold text-lg">{{ __("Leave Adjustments") }}</span>
			</div>
			<div class="w-full flex flex-col gap-2 p-4 overflow-y-auto" style="max-height: 60vh">
				<LeaveAdjustmentRow v-for="row in allRows" :key="row.name" :row="row" />
			</div>
		</div>
	</ion-modal>
</template>

<script setup>
import { computed, inject } from "vue"
import { IonModal } from "@ionic/vue"

import LeaveAdjustmentRow from "@/components/LeaveAdjustmentRow.vue"
import { leaveAdjustments } from "@/data/leaves"

const __ = inject("$translate")

const INLINE_LIMIT = 5

const allRows = computed(() => {
	if (!leaveAdjustments.data) return []
	return leaveAdjustments.data.map((adjustment) => ({
		...adjustment,
		is_increase: adjustment.adjustment_type === "Allocate",
	}))
})

const inlineRows = computed(() => allRows.value.slice(0, INLINE_LIMIT))
</script>
