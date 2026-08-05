<template>
	<div class="flex flex-row items-center justify-between bg-white rounded-lg p-3">
		<div class="flex flex-col min-w-0">
			<div class="text-sm font-medium text-gray-900 truncate">
				{{ __(row.leave_type, null, "Leave Type") }}
			</div>
			<div class="text-xs text-gray-500">
				{{ formatDate(row.posting_date) }}
			</div>
		</div>
		<div
			class="text-sm font-semibold shrink-0"
			:class="row.is_increase ? 'text-teal-600' : 'text-rose-500'"
		>
			{{ row.is_increase ? "+" : "-" }}{{ row.leaves_to_adjust }}
			{{ __("days") }}
		</div>
	</div>
</template>

<script setup>
import { inject } from "vue"

import dayjs from "@/utils/dayjs"

const __ = inject("$translate")

defineProps({
	row: {
		type: Object,
		required: true,
	},
})

const formatDate = (date) => dayjs(date).format("D MMM YYYY")
</script>
