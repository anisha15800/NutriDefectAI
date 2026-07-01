/**
 * main.js
 * Handles global interactions and dynamic component loading.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Dynamically load the navbar if the placeholder exists
    const navbarPlaceholder = document.getElementById('navbar-placeholder');
    if (navbarPlaceholder) {
        fetch('../components/navbar.html')
            .then(response => {
                if (!response.ok) throw new Error('Failed to load navbar');
                return response.text();
            })
            .then(html => {
                navbarPlaceholder.innerHTML = html;
                updateActiveNav();
            })
            .catch(error => console.error('Error loading navbar:', error));
    }
});

// Function to handle navbar state and highlight
function updateActiveNav() {
    const isLoggedIn = !!localStorage.getItem('token');
    const navLinksContainer = document.querySelector('.nav-links');
    
    if (navLinksContainer && isLoggedIn) {
        navLinksContainer.innerHTML = `
            <a href="index.html">Home</a>
            <a href="services.html">Services</a>
            <a href="nutrition_check.html">Nutrition Check</a>
            <a href="doctors.html">Doctors</a>
            <a href="about.html">About</a>
            <div class="nav-actions">
                <button id="logout-btn" class="btn btn-primary" style="display:flex; align-items:center; gap:0.5rem; padding: 0.5rem 1rem;">
                    <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
                    Logout
                </button>
                <button id="theme-toggle" class="theme-toggle">
                    <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" height="1.2em" width="1.2em" xmlns="http://www.w3.org/2000/svg"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
                </button>
            </div>
        `;
        
        document.getElementById('logout-btn').addEventListener('click', () => {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = 'index.html';
        });

        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                document.body.classList.toggle('light-mode');
            });
        }
        
        // Setup light mode as default for logged in state to match screenshot
        document.body.classList.add('light-mode');

        // Swap hero section if on index page
        const loggedOutHero = document.getElementById('logged-out-hero');
        const loggedInHero = document.getElementById('logged-in-hero');
        if (loggedOutHero && loggedInHero) {
            loggedOutHero.style.display = 'none';
            loggedInHero.style.display = 'flex';
        }
    }

    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        // Simple check to see if the link's href is included in the current path
        const href = link.getAttribute('href');
        if (href && href !== '#' && currentPath.includes(href.replace('../', ''))) {
            // Check for index page specifically to avoid empty strings matching
            if (href === 'index.html' && (currentPath.endsWith('/') || currentPath.endsWith('index.html'))) {
                link.style.color = 'var(--primary)';
                link.style.fontWeight = '700';
            } else if (href !== 'index.html') {
                link.style.color = 'var(--primary)';
                link.style.fontWeight = '700';
            }
        }
    });
}

// Form Handlers
document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = 'http://localhost:5000/api';

    // Sign Up Form Handler
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch(`${API_BASE_URL}/auth/signup`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ full_name: name, email, password })
                });
                const data = await response.json();
                
                if (response.ok) {
                    alert('Sign up successful!');
                    localStorage.setItem('token', data.token);
                    localStorage.setItem('user', JSON.stringify(data.user));
                    window.location.href = 'index.html';
                } else {
                    alert(data.error || 'Sign up failed.');
                }
            } catch (err) {
                console.error(err);
                alert('An error occurred while communicating with the server.');
            }
        });
    }

    // Sign In Form Handler
    const signinForm = document.getElementById('signin-form');
    if (signinForm) {
        signinForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch(`${API_BASE_URL}/auth/signin`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                const data = await response.json();
                
                if (response.ok) {
                    alert('Sign in successful!');
                    localStorage.setItem('token', data.token);
                    localStorage.setItem('user', JSON.stringify(data.user));
                    window.location.href = 'index.html';
                } else {
                    alert(data.error || 'Sign in failed.');
                }
            } catch (err) {
                console.error(err);
                alert('An error occurred while communicating with the server.');
            }
        });
    }
});
