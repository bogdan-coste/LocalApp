<template>
    <div :class="['h-screen w-full font-sans transition-colors duration-1000 relative overflow-hidden antialiased', { 'dark': isDark }]"
         :style="{ background: bgGradient }"
         @dragenter.prevent="isDragOver = true">
        
        <div v-if="isDragOver"
             @dragover.prevent
             @dragleave.prevent="isDragOver = false"
             @drop.prevent="handleDrop"
             class="fixed inset-4 z-[100] rounded-[3rem] border-4 border-dashed border-blue-500 bg-white/70 dark:bg-slate-900/80 backdrop-blur-xl flex flex-col items-center justify-center animate-in fade-in zoom-in-95 duration-300">
            
            <div class="pointer-events-none flex flex-col items-center text-center">
                <div class="p-8 rounded-full bg-gradient-to-br from-blue-600 to-sky-500 text-white shadow-[0_0_50px_rgba(59,130,246,0.6)] mb-6 animate-bounce">
                    <Upload :size="64" :stroke-width="2.5" />
                </div>
                <h2 class="text-4xl md:text-5xl font-black text-blue-700 dark:text-blue-400 tracking-tighter drop-shadow-sm">Eliberează fișierul oriunde</h2>
                <p class="mt-4 text-lg font-bold text-blue-600/60 dark:text-blue-400/60">Procesăm instant documentul tău.</p>
            </div>
        </div>

        <div class="fixed inset-0 pointer-events-none" :style="{ background: 'radial-gradient(circle at 50% 50%, transparent 40%, rgba(0,0,0,0.3) 100%)' }"></div>

        <div ref="particlesRef" class="fixed inset-0 -z-5 overflow-hidden pointer-events-none">
            <div v-for="i in 40" :key="i"
                 class="absolute rounded-full mix-blend-soft-light animate-float"
                 :style="{
                     width: `${Math.random() * 500 + 100}px`,
                     height: `${Math.random() * 500 + 100}px`,
                     left: `${Math.random() * 100}%`,
                     top: `${Math.random() * 100}%`,
                     background: `radial-gradient(circle, ${isDark ? `hsla(${200 + Math.random() * 40}, 80%, 60%, 0.1)` : `hsla(${200 + Math.random() * 40}, 80%, 80%, 0.1)`} 0%, transparent 70%)`,
                     transform: `translate(${mousePosition.x * 0.01}px, ${mousePosition.y * 0.01}px)`,
                     filter: 'blur(80px)',
                     transition: 'transform 0.2s ease-out',
                     animationDelay: `${i * 0.2}s`,
                     animationDuration: `${20 + Math.random() * 20}s`,
                 }"
            ></div>
        </div>

        <canvas v-if="showConfetti" ref="canvasRef" class="fixed inset-0 pointer-events-none z-50"></canvas>

        <header :class="['fixed top-0 left-0 right-0 z-40 px-6 lg:px-8 py-3 border-b transition-all duration-500', glassBg]"
                style="box-shadow: 0 20px 40px -15px rgba(0,0,0,0.1)">
            <div class="w-full flex justify-between items-center">
                
                <div class="flex items-center gap-3 group transition-all duration-300 select-none">
                    <div class="p-2.5 rounded-2xl bg-gradient-to-br from-blue-600 to-sky-500 text-white shadow-xl transition-all duration-300 group-hover:scale-110 group-hover:shadow-[0_0_40px_rgba(56,189,248,0.8)]">
                        <Fingerprint :size="24" />
                    </div>
                    <h1 :class="['text-2xl font-black tracking-tight bg-clip-text text-transparent bg-gradient-to-r transition-all duration-300', 
                                isDark ? 'from-white to-sky-200' : 'from-gray-900 to-blue-800']">
                        DocPlus
                    </h1>
                </div>

                <div class="flex items-center gap-4">
                    <div :class="['hidden lg:flex items-center gap-2 px-4 py-2 rounded-2xl border transition-colors', cardBg]">
                        <Globe :size="16" :class="textSecondary" />
                        <span :class="['text-sm font-bold', textPrimary]">{{ formattedTime }}</span>
                    </div>

                    <div class="relative">
                        <button @click="userDropdownOpen = !userDropdownOpen"
                                :class="['flex items-center gap-3 px-4 py-2 rounded-2xl border transition-all duration-300 hover:scale-105', cardBg]">
                            <div class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-600 to-sky-500 flex items-center justify-center text-white shadow-md">
                                <User :size="16" />
                            </div>
                            <div class="hidden md:block text-left">
                                <p :class="['text-sm font-bold leading-none', textPrimary]">{{ userEmail }}</p>
                                <p class="text-[10px] text-blue-600 dark:text-blue-400 font-black uppercase tracking-widest mt-1">Admin</p>
                            </div>
                            <ChevronDown :size="16" :class="['transition-transform', textPrimary, { 'rotate-180': userDropdownOpen }]" />
                        </button>

                        <div v-if="userDropdownOpen" 
                            :class="['absolute right-0 mt-3 w-64 rounded-2xl border overflow-hidden animate-in slide-in-from-top-2 duration-200 z-50', 
                                    isDark ? 'bg-[#0f172a] border-white/10 shadow-[0_10px_40px_rgba(0,0,0,0.8)]' : 'bg-white border-gray-100 shadow-[0_10px_40px_rgba(59,130,246,0.15)]']">
                            <div :class="['p-4 border-b', isDark ? 'border-white/10' : 'border-gray-100']">
                                <p :class="['text-sm font-bold', textPrimary]">{{ userEmail }}</p>
                                <p :class="['text-xs mt-0.5', textSecondary]">admin@docplus.com</p>
                            </div>
                            <div class="p-2 flex flex-col gap-1">
                                <button :class="['w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-left transition-colors font-medium text-sm', isDark ? 'hover:bg-white/5 text-gray-200' : 'hover:bg-gray-50 text-gray-700']">
                                    <Settings :size="16" /> Setări
                                </button>
                                <button :class="['w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-left transition-colors font-medium text-sm', isDark ? 'hover:bg-white/5 text-gray-200' : 'hover:bg-gray-50 text-gray-700']">
                                    <Bell :size="16" /> Notificări
                                </button>
                                <div :class="['h-px w-full my-1', isDark ? 'bg-white/5' : 'bg-gray-100']"></div>
                                <button @click="handleLogout" :class="['w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-left transition-colors font-medium text-sm', isDark ? 'hover:bg-red-500/10 text-red-400' : 'hover:bg-red-50 text-red-600']">
                                    <LogOut :size="16" /> Ieșire
                                </button>
                            </div>
                        </div>
                    </div>

                    <button @click="toggleTheme"
                            :class="['p-2.5 rounded-2xl transition-all duration-500 hover:rotate-180 hover:scale-110 active:scale-95 border', cardBg]">
                        <Sun v-if="isDark" :size="18" class="text-amber-500" />
                        <Moon v-else :size="18" class="text-blue-600" />
                    </button>
                </div>
            </div>
        </header>

        <main class="h-full w-full pt-28 pb-10 px-6 max-w-5xl mx-auto relative z-20 flex flex-col">
            
            <div v-if="errorMsg" :class="['fixed top-28 right-6 z-50 flex items-center gap-4 px-6 py-4 rounded-2xl shadow-2xl border transition-all duration-500 bg-red-50 border-red-200 text-red-800', showError ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-10 pointer-events-none']">
                <AlertCircle :size="24" class="animate-bounce" />
                <p class="font-bold">{{ errorMsg }}</p>
                <button @click="showError = false" class="ml-4 hover:opacity-70">
                    <X :size="18" />
                </button>
            </div>

            <div class="flex flex-col items-center text-center gap-8 mb-8 animate-in fade-in slide-in-from-bottom-4 duration-1000 shrink-0 mt-auto">
                
                <div>
                    <h2 :class="['text-6xl lg:text-7xl font-black tracking-tighter', textPrimary]">
                        Workspace
                    </h2>
                    <p :class="['text-lg md:text-xl font-medium mt-3', textSecondary]">Procesează documente instant cu rețele neurale avansate.</p>
                </div>
                
                <div class="flex flex-col md:flex-row items-center justify-center gap-4 w-full mt-2">
                    <div class="relative w-full md:w-96 group">
                        <Search :class="['absolute left-4 top-1/2 -translate-y-1/2 transition-colors group-focus-within:text-blue-600', textSecondary]" :size="20" />
                        <input type="text" placeholder="Caută fișiere..." v-model="searchTerm"
                            :class="['w-full pl-12 pr-16 py-4 rounded-2xl border focus:outline-none focus:ring-4 focus:ring-blue-500/20 transition-all font-medium shadow-sm', cardBg, textPrimary]" />
                        
                        <div class="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-1 opacity-60">
                            <kbd :class="['px-2 py-1 text-[10px] font-bold rounded-lg border bg-black/5 border-black/10', textPrimary]">⌘</kbd>
                            <kbd :class="['px-2 py-1 text-[10px] font-bold rounded-lg border bg-black/5 border-black/10', textPrimary]">K</kbd>
                        </div>
                    </div>

                    <div class="relative group w-full md:w-auto">
                        <div class="absolute -inset-0.5 bg-gradient-to-r from-blue-800 via-blue-600 to-sky-500 rounded-2xl blur-lg opacity-40 group-hover:opacity-70 transition duration-500 animate-pulse-slow"></div>
                        <input type="file" id="file-upload" class="hidden" @change="handleFileUpload" :disabled="isUploading" accept=".pdf,.png,.jpg,.jpeg" />
                        <label for="file-upload" 
                            class="relative flex items-center justify-center gap-2 px-8 py-4 rounded-2xl text-sm font-extrabold tracking-wide cursor-pointer transition-all active:scale-95 overflow-hidden text-white bg-gradient-to-r from-blue-800 to-blue-500 border-none shadow-md hover:scale-105 hover:shadow-lg hover:shadow-blue-500/30 w-full"
                            style="text-shadow: 0px 1px 2px rgba(0,0,0,0.4);">
                            <span class="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-500"></span>
                            <template v-if="isUploading">
                                <Loader2 :size="18" class="animate-spin" />
                                <span>{{ uploadProgress }}%</span>
                            </template>
                            <template v-else>
                                <Upload :size="18" class="animate-bounce-x" :stroke-width="2.5" />
                                Încarcă PDF
                            </template>
                        </label>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 shrink-0">
                <div v-for="(stat, idx) in statsWidgets" :key="idx"
                    :class="['rounded-2xl p-5 border transition-all duration-700 hover:shadow-lg animate-in fade-in slide-in-from-bottom-4 flex items-center gap-4', cardBg]"
                    :style="{ animationDelay: `${(idx as number) * 100}ms` }">
                    <div :class="['p-3.5 rounded-xl bg-gradient-to-br text-white shadow-md', stat.color]">
                        <component :is="stat.icon" :size="24" />
                    </div>
                    <div class="flex-1">
                        <p :class="['text-xs font-bold uppercase tracking-wider', textSecondary]">{{ stat.label }}</p>
                        <div class="flex items-baseline justify-between">
                            <p :class="['text-2xl font-black tabular-nums leading-none mt-1', textPrimary]">{{ stat.value }}</p>
                            <div v-if="stat.label === 'Procesate' && statsCount.total > 0" class="w-16 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                                <div class="h-full bg-emerald-500 rounded-full transition-all duration-1000"
                                    :style="{ width: `${(statsCount.completed / statsCount.total) * 100}%` }"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="filteredDocs.length > 0" 
                :class="['rounded-3xl border shadow-sm overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-700 flex flex-col flex-1 min-h-0 mb-auto', cardBg]">
                
                <div :class="['hidden md:grid grid-cols-12 gap-4 px-6 py-3 border-b text-xs font-bold uppercase tracking-widest shrink-0', isDark ? 'border-white/10 text-gray-400 bg-white/5' : 'border-gray-200 text-gray-500 bg-gray-50/50']">
                    <div class="col-span-5">Nume Fișier</div>
                    <div class="col-span-3">Status</div>
                    <div class="col-span-4 text-right">Acțiuni</div>
                </div>

                <div class="flex flex-col overflow-y-auto custom-scrollbar flex-1">
                    <div v-for="(doc, index) in filteredDocs" :key="doc.id"
                        :class="['relative group grid grid-cols-1 md:grid-cols-12 gap-4 px-6 py-4 items-center border-b last:border-b-0 transition-colors duration-300 shrink-0', 
                                isDark ? 'border-white/10 hover:bg-white/5' : 'border-gray-100 hover:bg-blue-50/30']">
                        
                        <div class="col-span-1 md:col-span-5 flex items-center gap-4">
                            <div class="p-2.5 rounded-xl bg-gradient-to-br from-blue-600 to-sky-500 text-white shadow-sm shrink-0 group-hover:scale-105 transition-transform">
                                <FileText :size="20" />
                            </div>
                            <div class="min-w-0">
                                <h3 :class="['font-bold text-sm md:text-base truncate', textPrimary]">{{ doc.name }}</h3>
                                <p :class="['text-xs font-medium mt-0.5', textSecondary]">{{ doc.uploadTime || 'azi' }} • {{ doc.size || '—' }}</p>
                            </div>
                        </div>

                        <div class="col-span-1 md:col-span-3 flex items-center">
                            <span :class="['inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider border', 
                                        (doc.status === 'Ready' || doc.status === 'Completed') ? 'bg-emerald-50 text-emerald-600 border-emerald-200 dark:bg-emerald-500/10 dark:text-emerald-400 dark:border-emerald-500/20' : 'bg-amber-50 text-amber-600 border-amber-200 dark:bg-amber-500/10 dark:text-amber-400 dark:border-amber-500/20 animate-pulse']">
                                <CheckCircle v-if="doc.status === 'Ready' || doc.status === 'Completed'" :size="14" />
                                <Clock v-else :size="14" />
                                {{ doc.status }}
                            </span>
                        </div>

                        <div class="col-span-1 md:col-span-4 flex justify-start md:justify-end items-center gap-2">
                            <button @click="handleAnalyze(doc)"
                                    :disabled="analyzingId === doc.fileId || doc.status !== 'Ready'"
                                    :class="['flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-extrabold tracking-wide transition-all disabled:opacity-50', 
                                            analyzingId === doc.fileId 
                                                ? (isDark ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30' : 'bg-blue-50 text-blue-600 border border-blue-200') 
                                                : 'bg-gradient-to-r from-blue-800 to-blue-500 text-white border-none shadow-sm hover:scale-105 hover:shadow-md hover:shadow-blue-500/30']"
                                    :style="analyzingId !== doc.fileId ? 'text-shadow: 0px 1px 2px rgba(0,0,0,0.4);' : ''">
                                <Loader2 v-if="analyzingId === doc.fileId" :size="14" class="animate-spin" />
                                <Sparkles v-else :size="14" :stroke-width="2.5" />
                                {{ analyzingId === doc.fileId ? 'Analizare...' : (doc.status === 'Completed' ? 'Recitește' : 'Procesare OCR') }}
                            </button>
                            
                            <div class="flex items-center gap-1 ml-2 border-l pl-3" :class="isDark ? 'border-white/10' : 'border-gray-200'">
                                <button :class="['p-2 rounded-lg transition-colors', isDark ? 'text-gray-400 hover:bg-white/10 hover:text-white' : 'text-gray-500 hover:bg-gray-100 hover:text-gray-900']" title="Descarcă">
                                    <Download :size="16" />
                                </button>
                                <button :class="['p-2 rounded-lg transition-colors', isDark ? 'text-gray-400 hover:bg-white/10 hover:text-white' : 'text-gray-500 hover:bg-gray-100 hover:text-gray-900']" title="Previzualizează">
                                    <Eye :size="16" />
                                </button>
                            </div>
                        </div>

                        <div v-if="analyzingId === doc.fileId" class="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-500/20 overflow-hidden">
                            <div class="h-full bg-blue-500 rounded-full animate-progress shadow-[0_0_10px_rgba(59,130,246,0.8)]"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div v-else 
                :class="['group relative rounded-3xl border transition-all duration-500 animate-in fade-in zoom-in-95 flex flex-col items-center justify-center flex-1 min-h-[250px] mb-auto', 
                        isDark 
                        ? 'border-blue-500/30 bg-blue-500/5 shadow-[0_0_40px_rgba(59,130,246,0.15)]' 
                        : 'border-blue-200 bg-white shadow-[0_0_30px_rgba(59,130,246,0.1)]', cardBg]">
    
                <div class="pointer-events-none flex flex-col items-center relative z-10">
                    <div :class="['p-6 rounded-2xl inline-block mb-4 transition-all duration-500 shadow-lg', 
                                isDark ? 'bg-gradient-to-br from-blue-600 to-blue-400 text-white' : 'bg-blue-50 text-blue-600']">
                        <Upload :size="40" :stroke-width="2.5" class="animate-bounce" />
                    </div>
                    
                    <h3 :class="['text-xl font-black mb-2 tracking-tight', textPrimary]">Trage fișierul PDF aici</h3>
                    <p :class="['text-sm font-semibold mb-2 max-w-sm mx-auto', textSecondary]">
                        Procesare instantanee cu AI PaddleOCR
                    </p>
                </div>
            </div>
            
            <div class="mt-auto pt-16"></div>
        </main>

        <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center px-4 py-8 animate-in fade-in duration-300">
            <div class="absolute inset-0 bg-black/70 backdrop-blur-2xl" @click="isModalOpen = false"></div>
            <div :class="['relative w-full max-w-4xl max-h-[85vh] flex flex-col rounded-3xl shadow-2xl border overflow-hidden', glassBg]"
                 style="transform: rotateX(2deg) rotateY(2deg); animation: spring-in 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);">
                <div :class="['flex justify-between items-center px-8 py-6 border-b', isDark ? 'border-white/10' : 'border-black/5']">
                    <div class="flex items-center gap-4">
                        <div :class="['p-3 rounded-xl text-white shadow-lg bg-gradient-to-r from-blue-800 to-blue-500']">
                            <AlignLeft :size="24" />
                        </div>
                        <div>
                            <h3 :class="['text-2xl font-black', textPrimary]">Text Extras</h3>
                            <p class="text-xs font-bold uppercase tracking-widest mt-1 text-blue-400">AI PaddleOCR</p>
                        </div>
                    </div>
                        <div class="flex items-center gap-3">
                            <button @click="handleCopyText"
                                    :class="['flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-extrabold tracking-wide transition-all', 
                                            isCopied 
                                                ? (isDark ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-emerald-100 text-emerald-700 border border-emerald-200') 
                                                : 'bg-gradient-to-r from-blue-800 to-blue-500 text-white border-none shadow-md hover:scale-105 hover:shadow-lg hover:shadow-blue-500/30']"
                                    :style="!isCopied ? 'text-shadow: 0px 1px 2px rgba(0,0,0,0.4);' : ''">
                                <Check v-if="isCopied" :size="16" :stroke-width="2.5" />
                                <Copy v-else :size="16" :stroke-width="2.5" />
                                {{ isCopied ? 'Copiat!' : 'Copiază text' }}
                            </button>
                            <button @click="isModalOpen = false" :class="['p-2.5 rounded-xl transition hover:scale-110', isDark ? 'text-gray-400 hover:bg-white/20 hover:text-white' : 'text-gray-500 hover:bg-black/10 hover:text-gray-900']">
                                <X :size="24" />
                            </button>
                        </div>
                </div>

                <div class="p-8 overflow-y-auto custom-scrollbar">
                    <div :class="['p-6 rounded-2xl text-sm md:text-base leading-relaxed whitespace-pre-wrap border font-mono shadow-inner', textPrimary, isDark ? 'bg-black/30 border-white/10' : 'bg-white/30 border-black/5']">
                        {{ extractedText || "Nu a fost detectat niciun text. Asigură-te că PDF-ul conține caractere vizibile." }}
                    </div>
                </div>

                <div :class="['px-8 py-5 border-t flex justify-between items-center', isDark ? 'border-white/10' : 'border-black/5']">
                    <p :class="['text-xs font-semibold', textSecondary]">Rezultatele pot necesita ajustări manuale minore.</p>
                    
                    <button @click="isModalOpen = false" 
                            class="px-8 py-2.5 rounded-xl text-sm font-extrabold tracking-wide transition-all text-white bg-gradient-to-r from-blue-800 to-blue-500 border-none shadow-md hover:scale-105 hover:shadow-lg hover:shadow-blue-500/30"
                            style="text-shadow: 0px 1px 2px rgba(0,0,0,0.4);">
                        Închide
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted, onUnmounted, nextTick } from 'vue';
import { useRouter } from 'vue-router'; 
import {
    LogOut, Upload, Search, FileText, CheckCircle, Clock,
    Sun, Moon, User, Loader2, X, AlignLeft, AlertCircle,
    Copy, Check, Sparkles, Download, Eye,
    Bell, Settings, ChevronDown,
    Fingerprint, Zap, Globe
} from 'lucide-vue-next';

const emit = defineEmits(['logout']);
const router = useRouter(); 

interface Document {
    id: number;
    name: string;
    fileId?: string;
    status: 'Pending' | 'Ready' | 'Completed' | 'Processing';
    uploadTime?: string;
    size?: string;
}

const documents = ref<Document[]>([]);
const searchTerm = ref('');
const theme = ref<'dark' | 'light'>('dark');
const userEmail = ref('Se încarcă...');
const analyzingId = ref<string | null>(null);
const errorMsg = ref<string | null>(null);
const showError = ref(false);
const uploadProgress = ref(0);
const isUploading = ref(false);
const isModalOpen = ref(false);
const extractedText = ref('');
const isCopied = ref(false);
const showConfetti = ref(false);
const userDropdownOpen = ref(false);
const currentTime = ref(new Date());
const mousePosition = ref({ x: 0, y: 0 });
const isDragOver = ref(false);

const canvasRef = ref<HTMLCanvasElement | null>(null);
const particlesRef = ref<HTMLDivElement | null>(null);

const isDark = computed(() => theme.value === 'dark');
const formattedTime = computed(() => currentTime.value.toLocaleTimeString());
const filteredDocs = computed(() => documents.value.filter((doc : Document) => doc.name.toLowerCase().includes(searchTerm.value.toLowerCase())));

const statsCount = computed(() => ({
    total: documents.value.length,
    completed: documents.value.filter((d : Document) => d.status === 'Ready' || d.status === 'Completed').length,
    pending: documents.value.filter((d : Document) => d.status === 'Pending' || d.status === 'Processing').length,
}));

const statsWidgets = computed(() => [
    { label: 'Total documente', value: statsCount.value.total, icon: FileText, color: 'from-blue-600 to-blue-400' },
    { label: 'Procesate', value: statsCount.value.completed, icon: CheckCircle, color: 'from-blue-500 to-cyan-400' },
    { label: 'În așteptare', value: statsCount.value.pending, icon: Clock, color: 'from-slate-500 to-slate-400' },
]);

const bgGradient = computed(() => isDark.value ? 'radial-gradient(circle at 30% 20%, #0A192F, #020617 80%)' : 'radial-gradient(circle at 70% 30%, #E0F2FE, #F1F5F9 80%)');
const glassBg = computed(() => isDark.value ? 'bg-[rgba(10,25,47,0.5)] backdrop-blur-2xl border border-white/10 shadow-2xl' : 'bg-[rgba(240,248,255,0.6)] backdrop-blur-2xl border border-blue-200/30 shadow-2xl');
const cardBg = computed(() => isDark.value ? 'bg-[rgba(15,35,65,0.5)] backdrop-blur-xl border border-blue-500/20 hover:border-blue-500/40' : 'bg-[rgba(240,248,255,0.7)] backdrop-blur-xl border border-blue-200/40 hover:border-blue-300/60');
const textPrimary = computed(() => isDark.value ? 'text-white' : 'text-gray-900');
const textSecondary = computed(() => isDark.value ? 'text-blue-200/70' : 'text-blue-800/60');

const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.clear(); 
    sessionStorage.clear();
    router.push('/').catch((err : Error) => {
        window.location.href = "/";
    });
};

const toggleTheme = () => {
    theme.value = theme.value === 'dark' ? 'light' : 'dark';
    document.documentElement.classList.toggle('light', theme.value === 'dark');
};

const fetchUser = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;
    try {
        const response = await fetch("http://localhost:8000/api/v1/users/me", {
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (response.ok) {
            const data = await response.json();
            userEmail.value = data.email;
        } else {
            userEmail.value = "Utilizator Necunoscut";
        }
    } catch (error) {
        console.error("Eroare conexiune user:", error);
    }
};

const handleCopyText = async () => {
    try {
        await navigator.clipboard.writeText(extractedText.value);
        isCopied.value = true;
        setTimeout(() => isCopied.value = false, 2000);
    } catch (err) {
        console.error('Failed to copy text: ', err);
    }
};

const handleAnalyze = async (doc: Document) => {
    if (!doc.fileId) {
        errorMsg.value = "Fișier invalid.";
        return;
    }
    errorMsg.value = null;
    analyzingId.value = doc.fileId;
    
    try {
        const token = localStorage.getItem("token");
        const response = await fetch(`http://localhost:8000/api/v1/documents/analyze/${doc.fileId}`, {
            method: "POST",
            headers: { "Authorization": `Bearer ${token}` }
        });
        
        if (response.ok) {
            const data = await response.json();
            extractedText.value = data.text;
            isModalOpen.value = true;
            showConfetti.value = true;
            
            const docIndex = documents.value.findIndex((d : Document) => d.fileId === doc.fileId);
            if (docIndex !== -1) {
                documents.value[docIndex].status = 'Completed';
            }
        } else {
            const errData = await response.json();
            errorMsg.value = errData.detail || "Backend-ul nu a putut procesa documentul.";
        }
    } catch (error) {
        errorMsg.value = "Eroare de conexiune cu serverul AI.";
    } finally {
        analyzingId.value = null;
    }
};

const processUpload = async (file: File) => {
    errorMsg.value = null;
    isUploading.value = true;
    uploadProgress.value = 0;

    const newDocId = documents.value.length ? Math.max(...documents.value.map((d : Document) => d.id)) + 1 : 1;
    const newDoc: Document = {
        id: newDocId,
        name: file.name,
        status: 'Pending',
        uploadTime: new Date().toLocaleTimeString(),
        size: (file.size / 1024).toFixed(2) + ' KB',
    };
    documents.value.push(newDoc);

    const formData = new FormData();
    formData.append("file", file);
    const token = localStorage.getItem("token");

    const interval = setInterval(() => {
        uploadProgress.value = Math.min(uploadProgress.value + 15, 90);
    }, 150);

    try {
        const response = await fetch("http://localhost:8000/api/v1/documents/upload", {
            method: "POST",
            headers: { "Authorization": `Bearer ${token}` },
            body: formData,
        });
        clearInterval(interval);
        
        if (response.ok) {
            uploadProgress.value = 100;
            const data = await response.json();
            const docIndex = documents.value.findIndex((d : Document) => d.id === newDocId);
            if (docIndex !== -1) {
                documents.value[docIndex].status = 'Ready';
                documents.value[docIndex].fileId = data.id;
            }
            setTimeout(() => uploadProgress.value = 0, 500);
        } else {
            throw new Error("Eroare la încărcare.");
        }
    } catch (error) {
        clearInterval(interval);
        errorMsg.value = "Eroare la procesarea fișierului.";
        documents.value = documents.value.filter((doc : Document) => doc.id !== newDocId);
    } finally {
        isUploading.value = false;
    }
};

const handleFileUpload = (e: Event) => {
    const target = e.target as HTMLInputElement;
    if (target.files?.length) {
        processUpload(target.files[0]);
    }
    target.value = ''; 
};

const handleDrop = (e: DragEvent) => {
    isDragOver.value = false; 
    const files = e.dataTransfer?.files;
    if (files && files.length > 0) {
        processUpload(files[0]);
    }
};

const handleMouseMove = (e: MouseEvent) => {
    mousePosition.value = { x: e.clientX, y: e.clientY };
};

const handleCardMouseMove = (e: MouseEvent) => {
    const target = e.currentTarget as HTMLElement;
    const rect = target.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const rotateX = (y / rect.height - 0.5) * 8;
    const rotateY = (x / rect.width - 0.5) * -8;
    target.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
};

const handleCardMouseLeave = (e: MouseEvent) => {
    const target = e.currentTarget as HTMLElement;
    target.style.transform = 'rotateX(0deg) rotateY(0deg) scale(1)';
};

let clockTimer: number;

onMounted(() => {
    window.addEventListener('mousemove', handleMouseMove);
    clockTimer = window.setInterval(() => currentTime.value = new Date(), 1000);
    fetchUser();
});

onUnmounted(() => {
    window.removeEventListener('mousemove', handleMouseMove);
    clearInterval(clockTimer);
});

watch(errorMsg, (newVal : string | null) => {
    if (newVal) {
        showError.value = true;
        setTimeout(() => showError.value = false, 5000);
    }
});

watch(showConfetti, async (newVal : boolean) => {
    if (newVal) {
        await nextTick();
    }
});
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
    width: 8px;
}
.custom-scrollbar::-webkit-scrollbar-track {
    background: v-bind("isDark ? '#020617' : '#e2e8f0'");
    border-radius: 20px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
    background: v-bind("isDark ? '#1e3a8a' : '#94a3b8'");
    border-radius: 20px;
}
@keyframes spring-in {
    0% { transform: scale(0.9) rotateX(0deg) rotateY(0deg); opacity: 0; }
    100% { transform: scale(1) rotateX(2deg) rotateY(2deg); opacity: 1; }
}
@keyframes bounce-x {
    0%, 100% { transform: translateX(0); }
    50% { transform: translateX(4px); }
}
.animate-bounce-x {
    animation: bounce-x 1s infinite;
}
@keyframes pulse-slow {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 0.8; }
}
.animate-pulse-slow {
    animation: pulse-slow 3s ease-in-out infinite;
}
@keyframes progress-fill {
    0% { width: 0%; }
    15% { width: 35%; }
    50% { width: 75%; }
    100% { width: 95%; } 
}

.animate-progress {
    animation: progress-fill 12s cubic-bezier(0.1, 0.8, 0.2, 1) forwards;
}
@keyframes float {
    0%, 100% { transform: translateY(0) translateX(0); }
    50% { transform: translateY(-30px) translateX(10px); }
}
.animate-float {
    animation: float 20s infinite alternate;
}

.drop-zone-glow {
  border: 2px dashed #00e676 !important; 
  border-radius: 8px; 
  box-shadow: 0 0 15px rgba(0, 230, 118, 0.7), 
              0 0 5px rgba(0, 230, 118, 0.5);  
  transition: box-shadow 0.3s ease; 
}
</style>