<template>
	<BaseLayout @refresh="handleRefresh">
		<template #body>
			<div class="flex flex-col items-center mt-2 mb-5 p-4 gap-6">
				<!-- <CheckInPanel /> -->
				<!-- <QuickLinks :items="quickLinks" :title="__('Quick Links')" /> -->
				<!-- <RequestPanel /> -->

				<div class="flex flex-col w-full">
					<h2 class="text-lg font-bold text-gray-900">
						{{ __("{0}, {1}", [greeting, employee?.data?.first_name]) }} 👋
					</h2>
				</div>

				<LeaveQuickActions />
				<LeaveSummaryCards />
				<LeaveBalanceList />

				<div class="flex flex-col gap-3 w-full">
					<div class="text-lg font-medium text-gray-900">
						{{ __("Recent Leave Applications") }}
					</div>
					<RequestList
						:component="markRaw(LeaveRequestItem)"
						:items="myLeaves.data"
						:addListButton="true"
						listButtonRoute="LeaveApplicationListView"
						:emptyStateMessage="__('You have no leave applications')"
					/>
				</div>
			</div>
		</template>
	</BaseLayout>
</template>

<script setup>
import { computed, inject, markRaw } from "vue"

import CheckInPanel from "@/components/CheckInPanel.vue"
import QuickLinks from "@/components/QuickLinks.vue"
import BaseLayout from "@/components/BaseLayout.vue"
import RequestPanel from "@/components/RequestPanel.vue"
import AttendanceIcon from "@/components/icons/AttendanceIcon.vue"
import ShiftIcon from "@/components/icons/ShiftIcon.vue"
import LeaveIcon from "@/components/icons/LeaveIcon.vue"
import ExpenseIcon from "@/components/icons/ExpenseIcon.vue"
import EmployeeAdvanceIcon from "@/components/icons/EmployeeAdvanceIcon.vue"
import SalaryIcon from "@/components/icons/SalaryIcon.vue"

import LeaveSummaryCards from "@/components/LeaveSummaryCards.vue"
import LeaveQuickActions from "@/components/LeaveQuickActions.vue"
import LeaveBalanceList from "@/components/LeaveBalanceList.vue"
import RequestList from "@/components/RequestList.vue"
import LeaveRequestItem from "@/components/LeaveRequestItem.vue"
import { myLeaves, leaveBalance } from "@/data/leaves"

const __ = inject("$translate")

const handleRefresh = async (done) => {
	await Promise.all([myLeaves.reload(), leaveBalance.reload()])
	done()
}
const employee = inject("$employee")
const dayjs = inject("$dayjs")

const greeting = computed(() => {
	const hour = dayjs().hour()
	if (hour < 12) return __("Good morning")
	if (hour < 17) return __("Good afternoon")
	return __("Good evening")
})

const quickLinks = [
	{
		icon: markRaw(AttendanceIcon),
		title: __("Request Attendance"),
		route: "AttendanceRequestFormView",
	},
	{
		icon: markRaw(ShiftIcon),
		title: __("Request a Shift"),
		route: "ShiftRequestFormView",
	},
	{
		icon: markRaw(LeaveIcon),
		title: __("Request Leave"),
		route: "LeaveApplicationFormView",
	},
	{
		icon: markRaw(ExpenseIcon),
		title: __("Claim an Expense"),
		route: "ExpenseClaimFormView",
	},
	{
		icon: markRaw(EmployeeAdvanceIcon),
		title: __("Request an Advance"),
		route: "EmployeeAdvanceFormView",
	},
	{
		icon: markRaw(SalaryIcon),
		title: __("View Salary Slips"),
		route: "SalarySlipsDashboard",
	},
]
</script>
