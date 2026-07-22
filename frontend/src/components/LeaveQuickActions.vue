<template>
	<div class="flex flex-col gap-3 w-full">
		<div class="text-lg font-medium text-gray-900">{{ __("Quick Actions") }}</div>
		<div class="flex flex-col bg-white rounded-lg">
			<router-link
				class="flex flex-row items-center justify-between p-4"
				:class="action !== actions[actions.length - 1] && 'border-b'"
				v-for="action in actions"
				:key="action.title"
				:to="{ name: action.route }"
			>
				<div class="flex flex-row items-center gap-3 grow">
					<div class="flex items-center justify-center h-9 w-9 rounded-full bg-green-100">
						<FeatherIcon :name="action.icon" class="h-4 w-4 text-green-600" />
					</div>
					<div class="flex flex-col">
						<div class="text-base font-normal text-gray-800">{{ action.title }}</div>
						<div class="text-xs text-gray-500">{{ action.subtitle }}</div>
					</div>
				</div>
				<FeatherIcon name="chevron-right" class="h-5 w-5 text-gray-500" />
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
