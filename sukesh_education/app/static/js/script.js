// Sukesh Education - Custom scripts

// Set up light mode (no theme switching)
function ensureLightMode() {
    // Clear any saved theme
    localStorage.removeItem('theme');
    // Ensure body has no theme class
    document.body.className = '';
}

document.addEventListener('DOMContentLoaded', function() {
    // Ensure light mode is set
    ensureLightMode();
    
    // Check if we're running in desktop mode (using pywebview)
    const isDesktop = window.navigator.userAgent.includes('pywebview');
    
    if (isDesktop) {
        // Add desktop mode class
        document.body.classList.add('desktop-mode');
        console.log('Running in desktop mode');
        
        // Show desktop controls
        const desktopControls = document.querySelector('.desktop-controls');
        if (desktopControls) {
            desktopControls.classList.remove('d-none');
        }
        
        // Setup window control handlers
        const minimizeBtn = document.getElementById('minimizeWindow');
        if (minimizeBtn) {
            minimizeBtn.addEventListener('click', function(e) {
                e.preventDefault();
                // This will be intercepted by pywebview
                if (window.pywebview && window.pywebview.api) {
                    // Try to use pywebview API if available
                    window.pywebview.api.minimize_window().then(function(result) {
                        console.log('Window minimized: ', result);
                    }).catch(function(error) {
                        console.error('Error minimizing window:', error);
                    });
                } else {
                    // Fallback - send a message to the window
                    window.dispatchEvent(new CustomEvent('pywebview-minimize'));
                }
            });
        }
        
        // Get system info if available
        if (window.pywebview && window.pywebview.api) {
            window.pywebview.api.get_system_info().then(function(info) {
                console.log('System info:', info);
                
                // Create a system info tooltip or badge if needed
                const sysInfoElement = document.createElement('div');
                sysInfoElement.className = 'system-info position-fixed bottom-0 end-0 p-2 m-2 bg-light rounded small text-muted';
                sysInfoElement.style.opacity = '0.7';
                sysInfoElement.textContent = `${info.platform} · PyWebView ${info.pywebview_version}`;
                sysInfoElement.style.zIndex = '1000';
                document.body.appendChild(sysInfoElement);
                
                // Make it fade out after hover
                sysInfoElement.addEventListener('mouseenter', function() {
                    this.style.opacity = '1';
                });
                sysInfoElement.addEventListener('mouseleave', function() {
                    this.style.opacity = '0.7';
                });
            }).catch(function(error) {
                console.error('Error getting system info:', error);
            });
        }
    }
    
    // Add animation class to auth cards on load
    const authCards = document.querySelectorAll('.auth-card');
    authCards.forEach(card => {
        card.classList.add('animate');
    });
    
    // Password visibility toggle functionality
    const togglePasswordBtns = document.querySelectorAll('.toggle-password');
    togglePasswordBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const passwordInput = document.querySelector(this.getAttribute('data-target'));
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                this.innerHTML = '<i class="bi bi-eye-slash"></i>';
            } else {
                passwordInput.type = 'password';
                this.innerHTML = '<i class="bi bi-eye"></i>';
            }
        });
    });
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-persistent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});
