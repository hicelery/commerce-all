/*
 * static/js/sizeselect.js
 * Handles size selection and quantity controls for product detail page.
 * Shows one quantity input group by default, then toggles display when the size select changes.
 * Exposes global functions `increaseQuantity(size)` and `decreaseQuantity(size)` for existing onclick handlers.
 */

(function(){
    function getQuantityInputs(){
        return Array.from(document.querySelectorAll('input[id^="quantity_"]'));
    }

    function hideAllQuantityGroups(){
        getQuantityInputs().forEach(input => {
            if(input.parentElement) input.parentElement.style.display = 'none';
            // disable the input so only the selected quantity is submitted
            input.disabled = true;
        });
    }

    function showQuantityGroupForSize(size){
        const input = document.getElementById('quantity_' + size);
        if(input && input.parentElement) {
            // allow default CSS (Bootstrap flex) by clearing display
            input.parentElement.style.display = '';
            input.disabled = false;
        }
    }

    function increaseQuantity(size){
        const input = document.getElementById('quantity_' + size);
        if(!input) return;
        const max = Number.parseInt(input.max, 10);
        const current = Number.parseInt(input.value, 10) || 1;
        if(Number.isFinite(max) ? current < max : true) input.value = current + 1;
    }

    function decreaseQuantity(size){
        const input = document.getElementById('quantity_' + size);
        if(!input) return;
        const current = Number.parseInt(input.value, 10) || 1;
        if(current > 1) input.value = current - 1;
    }

    function initSizeSelect(){
        const sizeSelect = document.getElementById('size');
        const inputs = getQuantityInputs();

        if(inputs.length === 0) return;

        // Hide all groups first
        hideAllQuantityGroups();

        // Show a default group: if a size is already selected, show its group, otherwise show the first group
        let shown = null;
        if(sizeSelect && sizeSelect.value){
            shown = document.getElementById('quantity_' + sizeSelect.value);
        }
        if(!shown) shown = inputs[0];
        if(shown && shown.parentElement) {
            shown.parentElement.style.display = '';
            shown.disabled = false;
        }

        // Toggle groups when the size select changes
        if(sizeSelect){
            sizeSelect.addEventListener('change', function(){
                hideAllQuantityGroups();
                const sel = sizeSelect.value;
                const input = document.getElementById('quantity_' + sel);
                if(input && input.parentElement) {
                    input.parentElement.style.display = '';
                    input.disabled = false;
                }
            });
        }
    }

    // Expose functions globally for existing inline onclick handlers
    window.increaseQuantity = increaseQuantity;
    window.decreaseQuantity = decreaseQuantity;
    window.sizeSelect = initSizeSelect;

    document.addEventListener('DOMContentLoaded', initSizeSelect);
})();

