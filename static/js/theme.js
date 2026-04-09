function toggleDarkMode() {
    const html = document.documentElement;
    html.classList.toggle('dark');
    const isDark = html.classList.contains('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    updateThemeIcon(isDark);
}

function updateThemeIcon(isDark) {
    const icon = document.getElementById('theme-icon');
    if(icon) {
        if(isDark) {
            icon.innerHTML = '<polyline points="12 3 12 5"></polyline><polyline points="12 19 12 21"></polyline><polyline points="4.22 4.22 5.64 5.64"></polyline><polyline points="18.36 18.36 19.78 19.78"></polyline><polyline points="1 12 3 12"></polyline><polyline points="21 12 23 12"></polyline><polyline points="4.22 19.78 5.64 18.36"></polyline><polyline points="18.36 4.22 19.78 5.64"></polyline><circle cx="12" cy="12" r="5"></circle>';
        } else {
            icon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>';
        }
    }
}

// init
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
    updateThemeIcon(true);
} else {
    document.documentElement.classList.remove('dark');
    updateThemeIcon(false);
}

// Clock logic
setInterval(() => {
    const clock = document.getElementById('live-clock');
    if(clock) {
        clock.textContent = new Date().toLocaleTimeString();
    }
}, 1000);
