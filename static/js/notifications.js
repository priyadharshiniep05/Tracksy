const toastContainer = document.getElementById('toast-container');

function showToast(title, message, type = 'info') {
    if (!toastContainer) return;
    
    const colors = {
        'info': 'bg-blue-500',
        'warning': 'bg-amber-500',
        'danger': 'bg-red-500',
        'success': 'bg-emerald-500'
    };
    const bgColor = colors[type] || colors['info'];

    const toast = document.createElement('div');
    toast.className = `max-w-xs text-white rounded shadow-lg p-4 mb-2 toast glassmorphism ${bgColor}`;
    toast.innerHTML = `
        <div class="font-bold flex items-center justify-between">
            <span>${title}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="text-white hover:text-gray-200">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
        </div>
        <div class="text-sm mt-1">${message}</div>
    `;
    
    toastContainer.appendChild(toast);
    
    // trigger animation
    setTimeout(() => toast.classList.add('show'), 100);
    
    // auto dismiss
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

let badgeCount = 0;
function updateNotificationBadge(increment) {
    const badge = document.getElementById('notif-badge');
    if(badge) {
        badgeCount += increment;
        if(badgeCount > 0) {
            badge.textContent = badgeCount;
            badge.classList.remove('hidden');
        } else {
            badge.classList.add('hidden');
        }
    }
}
