/**
 * Tracksy Core JS
 * Auth helpers, API fetch wrapper, toast system
 */

const API_BASE = '/api';

const Tracksy = {
    // API Wrapper
    async fetch(endpoint, options = {}) {
        const token = localStorage.getItem('tracksy_token');
        const headers = {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` }),
            ...options.headers
        };

        const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
        
        if (response.status === 401) {
            localStorage.removeItem('tracksy_token');
            if (!window.location.pathname.includes('/login')) {
                window.location.href = '/login';
            }
        }
        
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'API Error');
        }
        
        return response.json();
    },

    // Toast System
    toast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;
        
        const colors = {
            success: 'bg-green-500',
            error: 'bg-red-500',
            warn: 'bg-yellow-500',
            info: 'bg-blue-500'
        };
        
        const toast = document.createElement('div');
        toast.className = `${colors[type]} text-white p-4 rounded-lg shadow-lg mb-4 flex items-center justify-between transition-all duration-300 transform translate-x-full`;
        toast.innerHTML = `
            <span>${message}</span>
            <button onclick="this.parentElement.remove()" class="ml-4 font-bold">&times;</button>
        `;
        
        container.appendChild(toast);
        setTimeout(() => toast.classList.remove('translate-x-full'), 100);
        setTimeout(() => {
            toast.classList.add('translate-x-full');
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    },

    // Auth Helpers
    logout() {
        localStorage.removeItem('tracksy_token');
        localStorage.removeItem('tracksy_role');
        window.location.href = '/login';
    },

    formatDate(dateStr) {
        if (!dateStr) return 'TBD';
        return new Date(dateStr).toLocaleString();
    },

    initCounter() {
        const counters = document.querySelectorAll('.counter');
        counters.forEach(counter => {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText;
            const inc = target / 100;
            if (count < target) {
                counter.innerText = Math.ceil(count + inc);
                setTimeout(() => this.initCounter(), 10);
            } else {
                counter.innerText = target;
            }
        });
    }
};

// Dark Mode Toggle
document.addEventListener('DOMContentLoaded', () => {
    const isDark = localStorage.getItem('tracksy_theme') !== 'light';
    if (isDark) document.documentElement.classList.add('dark');
    else document.documentElement.classList.remove('dark');
});
