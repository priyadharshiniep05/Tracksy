// Counter animation: animate number from 0 to target
function animateCounter(el, target, duration=1500, prefix='', suffix='') {
    anime({
        targets: el,
        innerHTML: [0, target],
        easing: 'easeOutExpo',
        round: 1,
        duration: duration,
        update: function(a) {
            el.innerHTML = prefix + el.innerHTML + suffix;
        }
    });
}

// Stagger entrance animations for cards on page load
function staggerEntranceAnimation(selector, delay=100) {
    anime({
        targets: selector,
        translateY: [20, 0],
        opacity: [0, 1],
        easing: 'easeOutExpo',
        delay: anime.stagger(delay)
    });
}
