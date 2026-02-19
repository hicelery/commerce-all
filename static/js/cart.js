document.addEventListener('DOMContentLoaded', function() {
    const deleteModalEl = document.getElementById("deleteModal");
    const deleteModal = deleteModalEl ? new bootstrap.Modal(deleteModalEl) : null;
    const deleteButtons = document.querySelectorAll(".btn-delete");
    const deleteConfirmBtn = document.getElementById("deleteConfirm");
    const confirmForm = document.getElementById("confirmDeleteForm");

    // Clear-cart modal elements
    const clearModalEl = document.getElementById("clearCartModal");
    const clearModal = clearModalEl ? new bootstrap.Modal(clearModalEl) : null;
    const clearButtons = document.querySelectorAll('.btn-clear');
    const clearConfirmBtn = document.getElementById('clearConfirm');
    const confirmClearForm = document.getElementById('confirmClearForm');

    deleteButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const btn = e.currentTarget || button;
            const removeUrl = btn.getAttribute('data-remove-url');
            if (confirmForm && removeUrl) {
                confirmForm.setAttribute('action', removeUrl);
            }
            if (deleteModal) deleteModal.show();
        });
    });

    if (deleteConfirmBtn) {
        deleteConfirmBtn.addEventListener('click', () => {
            if (confirmForm && confirmForm.getAttribute('action')) {
                confirmForm.submit();
            }
        });
    }

    // Clear-cart handlers
    clearButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const btn = e.currentTarget || button;
            const clearUrl = btn.getAttribute('data-clear-url');
            if (confirmClearForm && clearUrl) {
                confirmClearForm.setAttribute('action', clearUrl);
            }
            if (clearModal) clearModal.show();
        });
    });

    if (clearConfirmBtn) {
        clearConfirmBtn.addEventListener('click', () => {
            if (confirmClearForm && confirmClearForm.getAttribute('action')) {
                confirmClearForm.submit();
            }
        });
    }
});