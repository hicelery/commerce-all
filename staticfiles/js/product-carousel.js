/**
 * Product Image Carousel
 * Handles main image display, thumbnail selection, and expanded image modal
 */

document.addEventListener('DOMContentLoaded', function() {
    // Get all image URLs
    const thumbnails = document.querySelectorAll('.product-thumbnail');
    const mainImage = document.getElementById('mainProductImage');
    const expandedImage = document.getElementById('expandedImage');
    const imageExpandModal = document.getElementById('imageExpandModal');
    const imageCounter = document.getElementById('imageCounter');
    const prevImageBtn = document.getElementById('prevImageBtn');
    const nextImageBtn = document.getElementById('nextImageBtn');
    
    let allImages = [];
    let currentImageIndex = 0;
    
    // Collect all image URLs
    function initializeImages() {
        allImages = [];
        thumbnails.forEach(thumbnail => {
            allImages.push({
                thumb: thumbnail.src,
                full: thumbnail.dataset.fullSrc
            });
        });
    }
    
    // Set main image and update thumbnail selection
    function setMainImage(imageSrc, index) {
        if (mainImage) {
            mainImage.src = imageSrc;
        }
        currentImageIndex = index;
        
        // Update thumbnail borders
        thumbnails.forEach((thumb, i) => {
            if (i === index) {
                thumb.style.borderColor = '#007bff';
                thumb.style.opacity = '1';
            } else {
                thumb.style.borderColor = '#e9ecef48';
                thumb.style.opacity = '0.7';
            }
        });
    }
    
    // Handle thumbnail clicks
    thumbnails.forEach((thumbnail, index) => {
        thumbnail.addEventListener('click', function() {
            setMainImage(this.dataset.fullSrc, index);
        });
    });
    
    // Handle main image click for expansion
    if (mainImage) {
        mainImage.addEventListener('click', function() {
            expandedImage.src = allImages[currentImageIndex].full;
            updateImageCounter();
            const modal = new bootstrap.Modal(imageExpandModal);
            modal.show();
        });
    }
    
    // Update image counter
    function updateImageCounter() {
        imageCounter.textContent = `${currentImageIndex + 1} / ${allImages.length}`;
    }
    
    // Show specific image in modal
    function showImageInModal(index) {
        if (index >= 0 && index < allImages.length) {
            currentImageIndex = index;
            expandedImage.src = allImages[index].full;
            updateImageCounter();
            
            // Update main image too
            if (mainImage) {
                mainImage.src = allImages[index].full;
            }
            setMainImage(allImages[index].full, index);
        }
    }
    
    // Previous image in modal
    if (prevImageBtn) {
        prevImageBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            let newIndex = currentImageIndex - 1;
            if (newIndex < 0) {
                newIndex = allImages.length - 1;
            }
            showImageInModal(newIndex);
        });
    }
    
    // Next image in modal
    if (nextImageBtn) {
        nextImageBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            let newIndex = currentImageIndex + 1;
            if (newIndex >= allImages.length) {
                newIndex = 0;
            }
            showImageInModal(newIndex);
        });
    }
    
    // Keyboard navigation in modal (optional - arrow keys)
    document.addEventListener('keydown', function(e) {
        if (imageExpandModal.classList.contains('show')) {
            if (e.key === 'ArrowLeft') {
                prevImageBtn.click();
            } else if (e.key === 'ArrowRight') {
                nextImageBtn.click();
            } else if (e.key === 'Escape') {
                const modal = bootstrap.Modal.getInstance(imageExpandModal);
                if (modal) {
                    modal.hide();
                }
            }
        }
    });
    
    // Initialize on load
    initializeImages();
    if (currentImageIndex < allImages.length) {
        setMainImage(allImages[0].full, 0);
    }
});
