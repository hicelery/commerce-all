    document.addEventListener('DOMContentLoaded', function() {
        const standardShipping = parseFloat('{{ standard_shipping }}');
        const expressShipping = parseFloat('{{ express_shipping }}');
        const subtotal = parseFloat('{{ subtotal }}');
        
        const shippingRadios = document.querySelectorAll('input[name="shipping_method"]');
        const shippingCostSpan = document.getElementById('shippingCost');
        const totalSpan = document.querySelector('.text-primary.fw-bold');
        
        function updateShippingCost() {
            const selectedMethod = document.querySelector('input[name="shipping_method"]:checked').value;
            let shippingCost;
            console.log(expressShipping)
            
            if (selectedMethod === 'express') {
                shippingCost = expressShipping;
            } else {
                shippingCost = standardShipping;
            }
            
            // Update shipping display
            if (shippingCost === 0) {
                shippingCostSpan.textContent = 'Free';
            } else {
                shippingCostSpan.textContent = '£' + shippingCost.toFixed(2);
            }
            
            // Update total
            const total = subtotal + shippingCost;
            totalSpan.textContent = '£' + total.toFixed(2);
        }
        
        // Add change listener to shipping method radios
        shippingRadios.forEach(radio => {
            radio.addEventListener('change', updateShippingCost);
        });
    });