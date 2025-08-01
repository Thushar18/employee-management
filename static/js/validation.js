// Common validation functions for Employee Management System

// Email validation
function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

// Phone validation
function validatePhone(phone) {
    const phonePattern = /^[\d\s\-\+\(\)]{10,15}$/;
    return phonePattern.test(phone);
}

// Password strength validation
function validatePassword(password) {
    return password.length >= 6;
}

// Name validation
function validateName(name) {
    return name.trim().length >= 2 && /^[a-zA-Z\s]+$/.test(name);
}

// URL validation
function validateURL(url) {
    if (!url) return true; // Optional field
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
}

// Add visual feedback to form fields
function setFieldValid(fieldId) {
    const field = document.getElementById(fieldId);
    const errorSpan = document.getElementById(fieldId + '-error');
    if (field && errorSpan) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        errorSpan.textContent = '';
    }
}

function setFieldInvalid(fieldId, message) {
    const field = document.getElementById(fieldId);
    const errorSpan = document.getElementById(fieldId + '-error');
    if (field && errorSpan) {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
        errorSpan.textContent = message;
    }
}

// Real-time validation for common fields
document.addEventListener('DOMContentLoaded', function() {
    // Email field real-time validation
    const emailFields = document.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        field.addEventListener('blur', function() {
            if (this.value && !validateEmail(this.value)) {
                setFieldInvalid(this.id, 'Please enter a valid email address');
            } else if (this.value) {
                setFieldValid(this.id);
            }
        });
    });

    // Phone field real-time validation
    const phoneFields = document.querySelectorAll('input[id*="phone"]');
    phoneFields.forEach(field => {
        field.addEventListener('blur', function() {
            if (this.value && !validatePhone(this.value)) {
                setFieldInvalid(this.id, 'Please enter a valid phone number');
            } else if (this.value) {
                setFieldValid(this.id);
            }
        });
    });

    // Password field real-time validation
    const passwordFields = document.querySelectorAll('input[type="password"]');
    passwordFields.forEach(field => {
        field.addEventListener('input', function() {
            if (this.value && !validatePassword(this.value)) {
                setFieldInvalid(this.id, 'Password must be at least 6 characters');
            } else if (this.value) {
                setFieldValid(this.id);
            }
        });
    });

    // Name field real-time validation
    const nameFields = document.querySelectorAll('input[id*="name"]');
    nameFields.forEach(field => {
        field.addEventListener('blur', function() {
            if (this.value && !validateName(this.value)) {
                setFieldInvalid(this.id, 'Name must be at least 2 characters and contain only letters');
            } else if (this.value) {
                setFieldValid(this.id);
            }
        });
    });
});

// Utility function to show loading state
function showLoading(buttonId) {
    const button = document.getElementById(buttonId);
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    }
}

// Utility function to hide loading state
function hideLoading(buttonId, originalText) {
    const button = document.getElementById(buttonId);
    if (button) {
        button.disabled = false;
        button.innerHTML = originalText;
    }
}