// Navbar scroll effect
document.addEventListener('DOMContentLoaded', () => {
    const nav = document.querySelector('nav');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    });

    // Mobile menu toggle (if needed)
    // Add HTMX event listeners for dynamic interactions
    document.body.addEventListener('htmx:beforeSwap', function(evt) {
        if(evt.detail.xhr.status === 404){
            alert("Error: Resource not found");
        } else if(evt.detail.xhr.status === 422){
            alert("Error: Validation failed");
        }
    });
});

// Utility to handle notifications (placeholder for a better toast system)
function notify(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
}
