// Control Room DSR JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Auto-save functionality for forms
    const formInputs = document.querySelectorAll('input[type="text"], input[type="number"], textarea, select');
    let autoSaveTimer;

    formInputs.forEach(input => {
        input.addEventListener('input', function() {
            clearTimeout(autoSaveTimer);
            showAutoSaveIndicator('saving');
            
            autoSaveTimer = setTimeout(() => {
                // Auto-save logic here
                showAutoSaveIndicator('saved');
            }, 2000);
        });
    });

    // File upload drag and drop
    const uploadAreas = document.querySelectorAll('.upload-area');
    uploadAreas.forEach(area => {
        area.addEventListener('dragover', function(e) {
            e.preventDefault();
            area.classList.add('dragover');
        });

        area.addEventListener('dragleave', function(e) {
            e.preventDefault();
            area.classList.remove('dragover');
        });

        area.addEventListener('drop', function(e) {
            e.preventDefault();
            area.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                const fileInput = area.querySelector('input[type="file"]');
                if (fileInput) {
                    fileInput.files = files;
                    handleFileSelect(fileInput);
                }
            }
        });
    });

    // Handle file selection
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            handleFileSelect(this);
        });
    });

    // Search functionality
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(input => {
        input.addEventListener('input', debounce(function() {
            const searchTerm = this.value.toLowerCase();
            performSearch(searchTerm);
        }, 300));
    });
});

// Auto-save indicator
function showAutoSaveIndicator(status) {
    let indicator = document.getElementById('autoSaveIndicator');
    
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'autoSaveIndicator';
        indicator.className = 'position-fixed bottom-0 end-0 m-3 alert alert-info py-2 px-3';
        indicator.style.zIndex = '9999';
        document.body.appendChild(indicator);
    }

    if (status === 'saving') {
        indicator.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Auto-saving...';
        indicator.className = 'position-fixed bottom-0 end-0 m-3 alert alert-info py-2 px-3 show';
    } else if (status === 'saved') {
        indicator.innerHTML = '<i class="fas fa-check me-2"></i>Auto-saved';
        indicator.className = 'position-fixed bottom-0 end-0 m-3 alert alert-success py-2 px-3 show';
        
        setTimeout(() => {
            indicator.classList.remove('show');
            setTimeout(() => {
                if (indicator.parentNode) {
                    indicator.parentNode.removeChild(indicator);
                }
            }, 300);
        }, 2000);
    }
}

// File upload handler
function handleFileSelect(input) {
    const file = input.files[0];
    if (!file) return;

    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = [
        'application/pdf',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ];

    if (file.size > maxSize) {
        showAlert('File size must be less than 16MB', 'error');
        input.value = '';
        return;
    }

    if (!allowedTypes.includes(file.type)) {
        showAlert('Only PDF, Excel, and Word documents are allowed', 'error');
        input.value = '';
        return;
    }

    // Show file preview
    const preview = input.parentNode.querySelector('.file-preview');
    if (preview) {
        preview.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-file me-2"></i>
                <span>${file.name}</span>
                <span class="badge bg-secondary ms-auto">${formatFileSize(file.size)}</span>
            </div>
        `;
        preview.style.display = 'block';
    }
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Show alert
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.classList.remove('show');
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.parentNode.removeChild(alertDiv);
                }
            }, 300);
        }
    }, 5000);
}

// Debounce function
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Search functionality
function performSearch(searchTerm) {
    const searchableElements = document.querySelectorAll('[data-searchable]');
    
    searchableElements.forEach(element => {
        const text = element.textContent.toLowerCase();
        const parent = element.closest('.searchable-item') || element.parentNode;
        
        if (text.includes(searchTerm) || searchTerm === '') {
            parent.style.display = '';
        } else {
            parent.style.display = 'none';
        }
    });
}

// Form submission with loading state
function submitFormWithLoading(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    if (!submitBtn) return;

    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Please wait...';
    submitBtn.disabled = true;

    // Re-enable after 10 seconds as fallback
    setTimeout(() => {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }, 10000);
}

// Initialize form loading states
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function() {
        submitFormWithLoading(this);
    });
});

// Print functionality
function printReport(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
            <head>
                <title>DSR Report</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body { font-family: Arial, sans-serif; }
                    @media print { 
                        .no-print { display: none !important; }
                        .card { border: 1px solid #000; }
                    }
                </style>
            </head>
            <body>
                ${element.innerHTML}
                <script>
                    window.onload = function() { 
                        window.print(); 
                        window.close(); 
                    }
                </script>
            </body>
        </html>
    `);
    printWindow.document.close();
}

// Session timeout warning functionality
function initSessionTimeout() {
    const SESSION_TIMEOUT = 60 * 60 * 1000; // 1 hour in milliseconds
    const WARNING_TIME = 10 * 60 * 1000; // Show warning 10 minutes before timeout
    
    let sessionTimer;
    let warningTimer;
    let warningShown = false;

    function resetTimers() {
        clearTimeout(sessionTimer);
        clearTimeout(warningTimer);
        warningShown = false;
        
        // Set warning timer (50 minutes)
        warningTimer = setTimeout(showSessionWarning, SESSION_TIMEOUT - WARNING_TIME);
        
        // Set session timeout (60 minutes)
        sessionTimer = setTimeout(handleSessionTimeout, SESSION_TIMEOUT);
    }

    function showSessionWarning() {
        if (warningShown) return;
        warningShown = true;
        
        const warningDiv = document.createElement('div');
        warningDiv.id = 'sessionWarning';
        warningDiv.className = 'modal fade';
        warningDiv.setAttribute('data-bs-backdrop', 'static');
        warningDiv.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-warning">
                        <h5 class="modal-title">
                            <i class="fas fa-exclamation-triangle me-2"></i>
                            Session Timeout Warning
                        </h5>
                    </div>
                    <div class="modal-body">
                        <p>Your session will expire in <strong><span id="countdownTimer">10:00</span></strong> minutes due to inactivity.</p>
                        <p>Click "Stay Logged In" to extend your session, or "Logout Now" to logout immediately.</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-success" onclick="extendSession()">
                            <i class="fas fa-clock me-2"></i>Stay Logged In
                        </button>
                        <button type="button" class="btn btn-secondary" onclick="logoutNow()">
                            <i class="fas fa-sign-out-alt me-2"></i>Logout Now
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(warningDiv);
        
        const modal = new bootstrap.Modal(warningDiv);
        modal.show();
        
        // Start countdown
        startCountdown();
    }

    function startCountdown() {
        let timeLeft = 10 * 60; // 10 minutes in seconds
        const countdownElement = document.getElementById('countdownTimer');
        
        const countdown = setInterval(() => {
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            countdownElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            
            timeLeft--;
            
            if (timeLeft < 0) {
                clearInterval(countdown);
                handleSessionTimeout();
            }
        }, 1000);
    }

    function handleSessionTimeout() {
        // Redirect to logout
        window.location.href = '/auth/logout';
    }

    window.extendSession = function() {
        // Make a request to extend session
        fetch('/auth/extend-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        }).then(response => {
            if (response.ok) {
                // Reset timers
                resetTimers();
                
                // Close warning modal
                const warningModal = document.getElementById('sessionWarning');
                if (warningModal) {
                    const modal = bootstrap.Modal.getInstance(warningModal);
                    modal.hide();
                    warningModal.remove();
                }
                
                showAlert('Session extended successfully!', 'success');
            }
        }).catch(error => {
            console.error('Error extending session:', error);
        });
    };

    window.logoutNow = function() {
        window.location.href = '/auth/logout';
    };

    // Reset timers on user activity
    ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'].forEach(event => {
        document.addEventListener(event, resetTimers, true);
    });

    // Initialize timers
    resetTimers();
}

// Update session time display
function updateSessionTimeDisplay() {
    const sessionTimeElement = document.getElementById('sessionTime');
    const sessionStatusElement = document.getElementById('sessionStatus');
    
    if (!sessionTimeElement || !sessionStatusElement) return;
    
    // This will be updated by the session timeout timer
    let sessionStartTime = new Date();
    
    setInterval(() => {
        const now = new Date();
        const elapsed = now - sessionStartTime;
        const hours = Math.floor(elapsed / (1000 * 60 * 60));
        const minutes = Math.floor((elapsed % (1000 * 60 * 60)) / (1000 * 60));
        
        const timeLeft = 60 - minutes; // Assuming 1-hour session
        
        if (timeLeft > 10) {
            sessionTimeElement.textContent = `${timeLeft}min left`;
            sessionStatusElement.className = 'badge bg-success ms-1';
            sessionStatusElement.title = 'Session Active';
        } else if (timeLeft > 0) {
            sessionTimeElement.textContent = `${timeLeft}min left`;
            sessionStatusElement.className = 'badge bg-warning ms-1';
            sessionStatusElement.title = 'Session expires soon';
        } else {
            sessionTimeElement.textContent = 'Expired';
            sessionStatusElement.className = 'badge bg-danger ms-1';
            sessionStatusElement.title = 'Session expired';
        }
    }, 60000); // Update every minute
}

// Initialize session timeout for authenticated users
if (document.querySelector('.navbar-nav .dropdown')) {
    initSessionTimeout();
    updateSessionTimeDisplay();
}

// Export functions for global use
window.showAlert = showAlert;
window.submitFormWithLoading = submitFormWithLoading;
window.printReport = printReport;
