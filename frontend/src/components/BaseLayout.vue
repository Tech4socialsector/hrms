<template>
	<ion-page>
		<ion-header class="ion-no-border">
			<div class="w-full sm:w-96">
				<div class="flex flex-col bg-white shadow-sm p-4">
					<div class="flex flex-row justify-between items-center">
						<div class="flex flex-row items-center gap-2">
							<FrappeHRLogo class="h-7 w-7" />
							<h2 class="text-xl font-bold text-gray-900">
								{{ props.pageTitle || __("Pathways") }}
							</h2>
						</div>
						<div class="flex flex-row items-center gap-3 ml-auto">
							<router-link
								:to="{ name: 'Notifications' }"
								v-slot="{ navigate }"
								class="flex flex-col items-center"
							>
								<span class="relative inline-block" @click="navigate">
									<FeatherIcon name="bell" class="h-6 w-6" />
									<span
										v-if="unreadNotificationsCount.data"
										class="absolute top-0 right-0.5 inline-block w-2 h-2 bg-red-600 rounded-full border border-white"
									>
									</span>
								</span>
							</router-link>
							<router-link
								:to="{ name: 'Profile' }"
								class="flex flex-col items-center"
							>
								<Avatar
									:image="user.data.user_image"
									:label="user.data.first_name"
									size="xl"
								/>
							</router-link>
						</div>
					</div>
				</div>
			</div>
		</ion-header>

		<ion-content class="ion-no-padding">
			<ion-refresher slot="fixed" @ionRefresh="handleRefresh">
				<ion-refresher-content
					:pullingIcon="chevronDownCircleOutline"
					:pullingText="__('Pull to refresh')"
					:refreshingSpinner="'circles'"
					:refreshingText="__('Refreshing…')"
				></ion-refresher-content>
			</ion-refresher>

			<div class="flex flex-col h-screen w-screen sm:w-96">
				<slot name="body"></slot>
			</div>
		</ion-content>
	</ion-page>
</template>

<script setup>
import { IonHeader, IonContent, IonPage, IonRefresher, IonRefresherContent } from "@ionic/vue"
import { chevronDownCircleOutline } from "ionicons/icons"
import { FeatherIcon, Avatar } from "frappe-ui"

import FrappeHRLogo from "@/components/icons/FrappeHRLogo.vue"
import { unreadNotificationsCount } from "@/data/notifications"
import { employeeResource } from "@/data/employee"

import { inject } from "vue"

const user = inject("$user")

const props = defineProps({
	pageTitle: {
		type: String,
		required: false,
		default: "",
	},
})

const emit = defineEmits(["refresh"])

const handleRefresh = async (event) => {
	const refreshes = [
		user.reload(),
		employeeResource.reload(),
		unreadNotificationsCount.reload(),
	]

	// views that don't listen to "refresh" never call resolveDone, so cap
	// the wait to avoid the refresher spinner hanging indefinitely
	let resolveDone
	const done = new Promise((resolve) => (resolveDone = resolve))
	const timeout = new Promise((resolve) => setTimeout(resolve, 3000))
	emit("refresh", resolveDone)
	refreshes.push(Promise.race([done, timeout]))

	try {
		await Promise.all(refreshes)
	} finally {
		event.target.complete()
	}
}
</script>
