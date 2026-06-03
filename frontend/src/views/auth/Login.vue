<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-100">
        <div class="max-w-md w-full bg-white rounded-lg shadow-md p-8">
            <h1 class="text-2xl font-bold text-center mb-6">Sign In</h1>

            <NotificationBanner v-if="error" type="error" :message="error" @close="clearError" />

            <form @submit.prevent="handleLogin" class="space-y-4">
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
                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                    />
                </div>

                <button
                    type="submit"
                    :disabled="loading"
                    class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                >
                    {{ loading ? "Iniciando sesión..." : "Iniciar sesión" }}
                </button>
            </form>

            <div class="mt-6 text-center text-sm">
                <router-link
                    to="/register"
                    class="font-medium text-indigo-600 hover:text-indigo-500"
                >
                    Don't have an account? Sign up
                </router-link>
            </div>

            <div class="mt-4 text-center text-sm">
                <router-link
                    to="/forgot-password"
                    class="font-medium text-gray-600 hover:text-gray-500"
                >
                    Forgot your password?
                </router-link>
            </div>
        </div>
    </div>
</template>

<script setup>
import { reactive } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "@/composables/useAuth";
import NotificationBanner from "@/components/NotificationBanner.vue";

const router = useRouter();
const { login, loading, error, clearError } = useAuth();

const form = reactive({
    email: "",
    password: "",
});

async function handleLogin() {
    const success = await login(form.email, form.password);
    if (success) {
        router.push("/dashboard");
    }
}
</script>
