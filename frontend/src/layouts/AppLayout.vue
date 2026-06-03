<template>
    <div class="flex h-screen bg-gray-100 dark:bg-gray-900">

        <!-- Sidebar -->
        <aside class="sidebar w-64 bg-white dark:bg-gray-800 shadow-md flex flex-col flex-shrink-0">
            <div class="h-16 flex items-center px-6 border-b border-gray-200 dark:border-gray-700">
                <span class="text-xl font-bold text-gray-900 dark:text-white">CoreBase</span>
            </div>

            <nav class="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
                <router-link
                    to="/dashboard"
                    class="flex items-center px-4 py-2 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                    active-class="bg-indigo-50 text-indigo-700 dark:bg-indigo-900 dark:text-indigo-300"
                >
                    Dashboard
                </router-link>
                <router-link
                    to="/tenants"
                    class="flex items-center px-4 py-2 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                    active-class="bg-indigo-50 text-indigo-700 dark:bg-indigo-900 dark:text-indigo-300"
                >
                    Tenants
                </router-link>
                <router-link
                    to="/jobs"
                    class="flex items-center px-4 py-2 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                    active-class="bg-indigo-50 text-indigo-700 dark:bg-indigo-900 dark:text-indigo-300"
                >
                    Jobs
                </router-link>
                <router-link
                    v-if="user?.is_superuser"
                    to="/watchdog"
                    class="flex items-center px-4 py-2 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                    active-class="bg-indigo-50 text-indigo-700 dark:bg-indigo-900 dark:text-indigo-300"
                >
                    Watchdog
                </router-link>
            </nav>
        </aside>

        <!-- Panel derecho -->
        <div class="flex-1 flex flex-col overflow-hidden">

            <!-- Header -->
            <header class="h-16 bg-white dark:bg-gray-800 shadow-sm flex items-center justify-end px-6 space-x-4 flex-shrink-0">

                <!-- Toggle dark mode -->
                <button
                    @click="toggleDark"
                    class="p-2 rounded-md text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
                    :title="isDark ? 'Modo claro' : 'Modo oscuro'"
                >
                    <svg v-if="isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707M17.657 17.657l-.707-.707M6.343 6.343l-.707-.707M12 7a5 5 0 100 10A5 5 0 0012 7z"/>
                    </svg>
                    <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
                    </svg>
                </button>

                <!-- Campana de notificaciones -->
                <NotificationBell />

                <div class="h-6 w-px bg-gray-200 dark:bg-gray-600"></div>

                <!-- Usuario + logout -->
                <div class="flex items-center space-x-3">
                    <router-link
                        to="/profile"
                        class="flex items-center space-x-2 text-sm text-gray-700 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400"
                    >
                        <div class="w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center">
                            <span class="text-xs font-medium text-indigo-700 dark:text-indigo-300">
                                {{ userInitial }}
                            </span>
                        </div>
                        <span class="hidden md:block">{{ user?.email }}</span>
                    </router-link>

                    <button
                        @click="logout"
                        class="p-2 rounded-md text-gray-500 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-700"
                        title="Cerrar sesión"
                    >
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
                        </svg>
                    </button>
                </div>
            </header>

            <!-- Contenido -->
            <main class="main-content flex-1 overflow-y-auto p-6">
                <router-view />
            </main>
        </div>

        <ToastContainer />
    </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { useAuth } from "@/composables/useAuth";
import { useNotifications } from "@/composables/useNotifications";
import NotificationBell from "@/components/NotificationBell.vue";
import ToastContainer from "@/components/ToastContainer.vue";

const { user, logout } = useAuth();
const { connectWebSocket, disconnect, loadUnreadCount } = useNotifications();

const isDark = ref(false);

onMounted(() => {
    isDark.value = localStorage.getItem("theme") === "dark" ||
        (!localStorage.getItem("theme") && window.matchMedia("(prefers-color-scheme: dark)").matches);
    applyTheme();
});

watch(user, (u) => {
    if (u) {
        loadUnreadCount();
        connectWebSocket(u.id);
    } else {
        disconnect();
    }
}, { immediate: true });

onUnmounted(disconnect);

function toggleDark() {
    isDark.value = !isDark.value;
    localStorage.setItem("theme", isDark.value ? "dark" : "light");
    applyTheme();
}

function applyTheme() {
    document.documentElement.classList.toggle("dark", isDark.value);
}

const userInitial = computed(() => {
    const email = user.value?.email || "";
    return email.charAt(0).toUpperCase();
});
</script>
