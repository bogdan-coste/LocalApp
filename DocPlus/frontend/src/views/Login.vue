<template>

    <div class="min-h-screen font-sans relative overflow-hidden antialiased"
         :style="{ background: 'radial-gradient(circle at 30% 20%, #0A192F, #020617 80%)' }">
        
        <div class="fixed inset-0 pointer-events-none" 
             :style="{ background: 'radial-gradient(circle at 50% 50%, transparent 40%, rgba(0,0,0,0.4) 100%)' }">
        </div>

        <div class="fixed inset-0 -z-5 overflow-hidden pointer-events-none">
            <div v-for="i in 30" :key="i"
                 class="absolute rounded-full mix-blend-soft-light animate-float"
                 :style="{
                     width: `${Math.random() * 400 + 100}px`,
                     height: `${Math.random() * 400 + 100}px`,
                     left: `${Math.random() * 100}%`,
                     top: `${Math.random() * 100}%`,
                     background: `radial-gradient(circle, hsla(${200 + Math.random() * 40}, 80%, 60%, 0.15) 0%, transparent 70%)`,
                     transform: `translate(${mousePosition.x * 0.01}px, ${mousePosition.y * 0.01}px)`,
                     filter: 'blur(80px)',
                     transition: 'transform 0.2s ease-out',
                     animationDelay: `${i * 0.2}s`,
                     animationDuration: `${20 + Math.random() * 20}s`,
                 }"
            ></div>
        </div>

        <div class="relative z-10 flex min-h-screen items-center justify-center px-4 py-12 sm:px-6 lg:px-8">
            <div class="w-full max-w-md">
                <div class="group relative bg-[rgba(10,25,47,0.5)] backdrop-blur-2xl border border-white/10 shadow-2xl rounded-3xl p-8 sm:p-10 transition-all duration-500 hover:shadow-blue-500/20">
                    
                    <div class="absolute inset-0 -z-10 rounded-3xl bg-gradient-to-r from-blue-700/0 via-blue-500/0 to-sky-500/0 group-hover:from-blue-700/20 group-hover:via-blue-500/20 group-hover:to-sky-500/20 blur-xl transition-all duration-700"></div>

                    <div class="text-center mb-8">
                        <div :class="['inline-flex items-center justify-center w-16 h-16 rounded-2xl text-white shadow-xl shadow-green-500/30 mb-4', logoGradient]">
                            <span class="text-2xl font-black">D+</span>
                        </div>
                        <h2 class="text-3xl font-black tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-blue-200">
                            DocPlus
                        </h2>
                        <p :class="['mt-2 text-sm font-medium', textSecondary]">
                            Your AI Document Workspace
                        </p>
                    </div>

                    <form @submit.prevent="handleLogin" class="space-y-6">
                        <div class="space-y-1">
                            <label for="email" :class="['block text-sm font-medium', textSecondary]">Email</label>
                            <input id="email" type="email" required v-model="email"
                                   class="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-blue-300/30 focus:outline-none focus:ring-4 focus:ring-blue-500/20 transition-all"
                                   placeholder="admin@docplus.com" />
                        </div>

                        <div class="space-y-1">
                            <div class="flex items-center justify-between">
                                <label for="password" :class="['block text-sm font-medium', textSecondary]">Password</label>
                                <a href="#" class="text-sm font-medium text-sky-400 hover:text-sky-300 transition-colors">Forgot password?</a>
                            </div>
                            <div class="relative">
                                <input id="password" :type="showPassword ? 'text' : 'password'" required v-model="password"
                                       class="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-blue-300/30 focus:outline-none focus:ring-4 focus:ring-blue-500/20 transition-all pr-12"
                                       placeholder="••••••••" />
                                <button type="button" @click="showPassword = !showPassword"
                                        class="absolute inset-y-0 right-0 pr-4 flex items-center text-blue-300/50 hover:text-white transition-colors">
                                    <EyeOff v-if="showPassword" class="w-5 h-5" />
                                    <Eye v-else class="w-5 h-5" />
                                </button>
                            </div>
                        </div>

                        <button type="submit" :disabled="isLoading"
                                :class="['relative w-full py-3.5 rounded-xl font-bold text-white transition-all duration-300 overflow-hidden group/btn', 
                                isLoading ? 'bg-blue-500/50 cursor-not-allowed' : `${accentGradient} hover:scale-[1.02] hover:shadow-2xl hover:shadow-sky-500/30`]">
                            <span class="absolute inset-0 bg-white/20 translate-y-full group-hover/btn:translate-y-0 transition-transform duration-500"></span>
                            <span v-if="isLoading" class="flex items-center justify-center gap-2">
                                <svg class="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                </svg>
                                Se conectează...
                            </span>
                            <span v-else>Log In</span>
                        </button>

                        <div v-if="error" class="flex items-center gap-3 p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 animate-in fade-in">
                            <AlertCircle :size="20" />
                            <p class="text-sm font-medium">{{ error }}</p>
                        </div>
                    </form>

                    <div class="mt-8 text-center">
                        <p :class="['text-sm', textSecondary]">
                            No account? <a href="#" class="font-medium text-sky-400 hover:text-sky-300 transition-colors">Sign up</a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router'; 
import { Eye, EyeOff, AlertCircle } from 'lucide-vue-next';

const router = useRouter();

const emit = defineEmits(['loginSuccess']);

const email = ref('admin@docplus.com');
const password = ref('changethis'); 
const showPassword = ref(false);
const error = ref('');
const isLoading = ref(false);
const mousePosition = reactive({ x: 0, y: 0 });

const textSecondary = 'text-blue-200/70';
const accentGradient = 'bg-gradient-to-r from-blue-800 via-blue-600 to-sky-500';
const logoGradient = 'bg-gradient-to-br from-green-500 to-emerald-600';

const handleMouseMove = (e: MouseEvent) => {
    mousePosition.x = e.clientX;
    mousePosition.y = e.clientY;
};

onMounted(() => {
    window.addEventListener('mousemove', handleMouseMove);
});

onUnmounted(() => {
    window.removeEventListener('mousemove', handleMouseMove);
});

const handleLogin = async () => {
    error.value = "";
    isLoading.value = true;
    const formData = new FormData();
    formData.append('username', email.value);
    formData.append('password', password.value);

    try {
        const response = await fetch("http://localhost:8000/api/v1/login/access-token", {
            method: "POST",
            body: formData,
        });
        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem("token", data.access_token);
            
            emit('loginSuccess');
            

            router.push('/dashboard'); 
        } else {
            error.value = data.detail || "Email sau parolă incorectă.";
        }
    } catch (err) {
        console.error("Eroare request:", err);
        error.value = "Nu m-am putut conecta la serverul backend. Verifică dacă Docker rulează.";
    } finally {
        isLoading.value = false;
    }
};
</script>

<style scoped>
@keyframes float {
    0%, 100% { transform: translateY(0) translateX(0); }
    50% { transform: translateY(-30px) translateX(10px); }
}
.animate-float {
    animation: float 20s infinite alternate;
}
</style>