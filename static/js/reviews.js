const editButtons = document.getElementsByClassName('btn-edit');
const reviewText = document.getElementById('review_comment');
const reviewTitle = document.getElementById('review_title');
const reviewRatingButton = document.querySelectorAll('input[name="rating"]'); // rating element not available in this static file
const reviewForm = document.getElementById('reviewForm');
const submitButton = document.getElementById('submit-review');
const resetButton = document.getElementById('reset-review');
const reviewFormHeader = document.getElementById('reviewFormHeader');
/**
 * Initializes the review edit functionality by adding event listeners to edit buttons.
 * When an edit button is clicked, it populates the review form with the existing review data
 * and changes the form action to the review edit URL.
 * Scrols the form into view for better user experience.
 * When the reset button is clicked, it clears the form fields and resets the form action to the default add review URL.
 * 
 */
for (let button of editButtons) {
    button.addEventListener('click', (e) => {
        /** get review id and review content */
        // ensure we reference the button the listener is attached to (handles clicks on inner elements)
        const btn = e.currentTarget || button;
        const reviewId = btn.getAttribute('review_id');
        const rating = document.getElementById(`ratingdisplay${reviewId}`).getAttribute('value'); // get the rating value from the span's value attribute

         // set the rating based on the review data (assuming rating is stored in a hidden input or similar)
        let reviewCommentText = document.getElementById(`review_comment${reviewId}`).innerText;
        let reviewTitleText = document.getElementById(`review_title${reviewId}`).innerText;
        
        console.log(`${rating}`);
       
        //scrolls form into view 
        reviewFormHeader.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        //Populate the review form with the existing review data and change the form action to the review edit URL.         
        if (reviewTitle) reviewTitle.value = reviewTitleText;
        if (reviewText) reviewText.value = reviewCommentText;
        reviewRatingButton[rating-1].setAttribute('checked', true); // set the correct rating button as checked
        submitButton.innerText = 'Update Review';
        resetButton.innerText = 'Cancel'; // show the reset button when editing
        reviewFormHeader.innerText = 'Edit Your Review';
        reviewForm.setAttribute('action', `review_edit/${reviewId}/`);

        
    });
    
}
/**Try to create HTML variable to reduce need to update script if any HTML changes  */

if (resetButton) {
            resetButton.addEventListener('click', () => {
                // Clear the form fields and reset the form action to the default add review URL
                reviewRatingButton.forEach(button => button.removeAttribute('checked')); // uncheck all rating buttons
                submitButton.innerHTML = '<i class="fas fa-paper-plane me-2"></i>Submit Review';
                reviewFormHeader.innerText = 'Write a Review';
                reviewForm.setAttribute('action', `add_review/`);
                resetButton.innerHTML = '<i class="fas fa-x me-2"></i>Clear'; // reset button text back to Reset
            });
        }