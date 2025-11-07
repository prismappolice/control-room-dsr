// Control Room DSR JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Mobile header optimization
    optimizeMobileHeader();
    
    // Handle window resize for header adjustments
    window.addEventListener('resize', debounce(optimizeMobileHeader, 250));
    
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

// Mobile header optimization
function optimizeMobileHeader() {
    const navbar = document.querySelector('.navbar');
    const navbarLeft = document.querySelector('.navbar-left');
    const navbarRight = document.querySelector('.navbar-right');
    const navbarCenter = document.querySelector('.navbar-center');
    const headerLogos = document.querySelectorAll('.header-logo');
    
    if (!navbar || !navbarLeft || !navbarRight || !navbarCenter) return;
    
    const screenWidth = window.innerWidth;
    
    // Adjust based on screen size
    if (screenWidth <= 576) {
        // Very small screens - minimize everything
        headerLogos.forEach(logo => {
            logo.style.maxHeight = '35px';
            logo.style.maxWidth = '60px';
        });
        
        // Adjust spacing
        navbarLeft.style.paddingRight = '0.25rem';
        navbarRight.style.paddingLeft = '0.25rem';
        
    } else if (screenWidth <= 768) {
        // Small screens
        headerLogos.forEach(logo => {
            logo.style.maxHeight = '40px';
            logo.style.maxWidth = '80px';
        });
        
        navbarLeft.style.paddingRight = '0.5rem';
        navbarRight.style.paddingLeft = '0.5rem';
        
    } else if (screenWidth <= 992) {
        // Medium screens
        headerLogos.forEach(logo => {
            logo.style.maxHeight = '50px';
            logo.style.maxWidth = '120px';
        });
        
        navbarLeft.style.paddingRight = '0.75rem';
        navbarRight.style.paddingLeft = '0.75rem';
        
    } else {
        // Large screens - reset to default
        headerLogos.forEach(logo => {
            logo.style.maxHeight = '75px';
            logo.style.maxWidth = '250px';
        });
        
        navbarLeft.style.paddingRight = '1rem';
        navbarRight.style.paddingLeft = '1rem';
    }
    
    // Handle logo loading errors
    headerLogos.forEach(logo => {
        logo.addEventListener('error', function() {
            this.style.display = 'none';
        });
        
        logo.addEventListener('load', function() {
            this.style.display = 'block';
        });
    });
}

// Check if images exist and handle gracefully
function handleLogoFallbacks() {
    const logos = document.querySelectorAll('.header-logo');
    
    logos.forEach(logo => {
        const img = new Image();
        img.onload = function() {
            logo.style.opacity = '1';
        };
        img.onerror = function() {
            logo.style.display = 'none';
            // Adjust layout when logo is missing
            const parent = logo.closest('.navbar-left, .navbar-right');
            if (parent) {
                parent.style.minWidth = '40px';
            }
        };
        img.src = logo.src;
    });
}

// Call on page load
document.addEventListener('DOMContentLoaded', handleLogoFallbacks);

// Export functions for global use
window.showAlert = showAlert;
window.submitFormWithLoading = submitFormWithLoading;
window.printReport = printReport;
window.optimizeMobileHeader = optimizeMobileHeader;
