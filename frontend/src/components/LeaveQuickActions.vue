<template>
	<div class="flex flex-col gap-3 w-full">
		<div class="text-lg font-medium text-gray-900">{{ __("Quick Actions") }}</div>
		<div class="flex flex-col gap-3">
			<router-link
				v-for="(action, index) in actions"
				:key="action.title"
				:to="{ name: action.route }"
				class="flex flex-row items-center gap-3 rounded-lg py-4 px-4"
				:class="
					index === 0
						? 'bg-gray-900 text-white'
						: 'bg-white text-gray-900 border border-gray-200'
				"
			>
				<div
					class="flex items-center justify-center h-9 w-9 rounded-full shrink-0"
					:class="index === 0 ? 'bg-white/15' : 'bg-gray-100'"
				>
					<FeatherIcon
						:name="action.icon"
						class="h-4 w-4"
						:class="index === 0 ? 'text-white' : 'text-gray-800'"
					/>
				</div>
				<div class="flex flex-col grow">
					<div class="text-base font-medium">{{ action.title }}</div>
					<div class="text-xs" :class="index === 0 ? 'text-white/70' : 'text-gray-500'">
						{{ action.subtitle }}
					</div>
				</div>
				<FeatherIcon
					name="chevron-right"
					class="h-5 w-5 shrink-0"
					:class="index === 0 ? 'text-white/70' : 'text-gray-500'"
				/>
			</router-link>
		</div>
	</div>
</template>

<script setup>
import { inject } from "vue"
import { FeatherIcon } from "frappe-ui"

const __ = inject("$translate")

const actions = [
	{
		icon: "plus-circle",
		title: __("Apply for Leave"),
		subtitle: __("Submit a new leave application"),
		route: "LeaveApplicationFormView",
	},
	{
		icon: "file-text",
		title: __("My Leave Applications"),
		subtitle: __("View status of your applications"),
		route: "LeaveApplicationListView",
	},
]
</script>
