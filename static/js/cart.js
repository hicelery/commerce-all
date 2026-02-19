document.addEventListener('DOMContentLoaded', function() {

    // Clear-cart modal elements
    const clearModalEl = document.getElementById("clearCartModal");
    const clearModal = clearModalEl ? new bootstrap.Modal(clearModalEl) : null;
    const clearButtons = document.querySelectorAll('.btn-clear');
    const clearConfirmBtn = document.getElementById('clearConfirm');
    const confirmClearForm = document.getElementById('confirmClearForm');


    // Clear-cart handlers
    clearButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const btn = e.currentTarget || button;
            const clearUrl = btn.getAttribute('data-clear-url');
            if (confirmClearForm && clearUrl) {
                confirmClearForm.setAttribute('action', clearUrl);
            }
            // prefer explicit data-remove-url, otherwise fall back to enclosing form's action
            let removeUrl = btn.getAttribute('data-remove-url');
            if (!removeUrl) {
                const form = btn.closest('form');
                if (form) removeUrl = form.getAttribute('action');
            }
            if (confirmForm && removeUrl) {
                confirmForm.setAttribute('action', removeUrl);
            }
    if (clearConfirmBtn) {
        clearConfirmBtn.addEventListener('click', () => {
            if (confirmClearForm && confirmClearForm.getAttribute('action')) {
                confirmClearForm.submit();
            }
        });
    }
});