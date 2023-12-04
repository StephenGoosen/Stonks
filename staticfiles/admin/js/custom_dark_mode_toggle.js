// custom_dark_mode_toggle.js

document.addEventListener('DOMContentLoaded', function() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const bodyElement = document.body;
    const h3Elements = document.querySelectorAll('h3');

    // Check if dark mode preference is set
    let isDarkMode = localStorage.getItem('darkMode') === 'enabled';

    // Set initial dark mode state
    updateDarkMode();

    // Toggle dark mode on button click
    darkModeToggle.addEventListener('click', function() {
        isDarkMode = !isDarkMode; // Toggle dark mode state
        updateDarkMode();
    });

    function updateDarkMode() {
        if (isDarkMode) {
            enableDarkMode();
        } else {
            disableDarkMode();
        }
    }

    function enableDarkMode() {
        bodyElement.classList.add('dark-mode');
        h3Elements.forEach(function(h3Element) {
            h3Element.classList.add('dark-mode');
        });
        localStorage.setItem('darkMode', 'enabled');
    }

    function disableDarkMode() {
        bodyElement.classList.remove('dark-mode');
        h3Elements.forEach(function(h3Element) {
            h3Element.classList.remove('dark-mode');
        });
        localStorage.setItem('darkMode', null);
    }
});