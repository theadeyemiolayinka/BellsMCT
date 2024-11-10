// Dark mode toggle and theme storage
const themeCheckbox = document.getElementById('theme-toggle-btn');
const body = document.body;
const storedTheme = localStorage.getItem('theme');

if (storedTheme === 'dark') {
    body.classList.add('dark-mode');
}

if (storedTheme === 'dark') {
    themeCheckbox.checked = true;
} else {
    themeCheckbox.checked = false;
}

themeCheckbox.addEventListener('change', () => {
    body.classList.toggle('dark-mode');
    const theme = body.classList.contains('dark-mode') ? 'dark' : 'light';
    if (theme === 'dark') {
        themeCheckbox.checked = true;
    } else {
        themeCheckbox.checked = false;
    }
    localStorage.setItem('theme', theme);
});

// Toggle mobile menu display
const hamburger = document.getElementById('hamburger');
const hamburger_btn = document.querySelector('#hamburger .menu-btn');
const mobileMenu = document.getElementById('mobileMenu');

hamburger.addEventListener('click', () => {
    mobileMenu.classList.toggle('show');
    if (hamburger_btn.classList.contains('open')) {
        hamburger_btn.classList.remove('open');
        hamburger_btn.classList.add('close');
    } else {
        hamburger_btn.classList.remove('close');
        hamburger_btn.classList.add('open');
    }
});

// Add background color to header on scroll
window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Check if the page loads pre-scrolled and apply the scrolled class
document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('header');
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});