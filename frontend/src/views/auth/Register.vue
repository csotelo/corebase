<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-100">
        <div class="max-w-md w-full bg-white rounded-lg shadow-md p-8">
            <h1 class="text-2xl font-bold text-center mb-6">Create Account</h1>

            <NotificationBanner v-if="error" type="error" :message="errorMessage" @close="clearError" />
            <NotificationBanner v-if="success" type="success" message="Registration successful! Please check your email to verify your account." />

            <form v-if="!success" @submit.prevent="handleRegister" class="space-y-4">
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700">
                        Email
                    </label>
                    <input
                        id="email"
                        v-model="form.email"
                        type="email"
                        required
                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                        placeholder="you@example.com"
                    />
                    <p v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email[0] }}</p>
                </div>

                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700">
                        Password
                    </label>
                    <input
                        id="password"
                        v-model="form.password"
                        type="password"
                        required
                        minlength="8"
                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                    />
                    <p v-if="errors.password" class="mt-1 text-sm text-red-600">{{ errors.password[0] }}</p>
                </div>

                <div>
                    <label for="password_confirm" class="block text-sm font-medium text-gray-700">
                        Confirm Password
                    </label>
                    <input
                        id="password_confirm"
                        v-model="form.password_confirm"
                        type="password"
                        required
                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                    />
                </div>

                <button
                    type="submit"
                    :disabled="loading"
                    class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                >
                    {{ loading ? "Creating account..." : "Create Account" }}
                </button>
            </form>

            <div class="mt-6 text-center text-sm">
                <router-link
                    to="/login"
                    class="font-medium text-indigo-600 hover:text-indigo-500"
                >
                    Already have an account? Sign in
                </router-link>
            </div>
        </div>
    </div>
</template>

<script setup>
import { reactive, computed } from "vue";
import { useAuth } from "@/composables/useAuth";
import NotificationBanner from "@/components/NotificationBanner.vue";

const { register, loading, error, clearError } = useAuth();

const form = reactive({
    email: "",
    password: "",
    password_confirm: "",
});

const errors = reactive({});
const success = ref(false);

const errorMessage = computed(() => {
    if (typeof error.value === "object") {
        return JSON.stringify(error.value);
    }
    return error.value;
});

function validate() {
    Object.keys(errors).forEach((key) => delete errors[key]);
    let valid = true;

    if (form.password !== form.password_confirm) {
        errors.password_confirm = ["Passwords do not match"];
        valid = false;
    }

    if (form.password.length < 8) {
        errors.password = ["Password must be at least 8 characters"];
        valid = false;
    }

    return valid;
}

async function handleRegister() {
    clearError();
    if (!validate()) return;

    const result = await register(form);
    if (result) {
        success.value = true;
    }
}
</script>

<script>
import { ref } from "vue";
export default { name: "RegisterView" };
</script>
