$(document).ready(function() {
    var reviewsPerPage = 5;  // Set the number of reviews per page
    var $reviewList = $('.review-list');
    var $reviews = $reviewList.find('.review');
    var $pagination = $('.pagination');
    var $writeReviewButton = $('.write-review-button a');

    // Hide all reviews
    $reviews.hide();

    // Show the first N reviews (N = reviewsPerPage)
    $reviews.slice(0, reviewsPerPage).show();

    // Calculate the number of pages based on the number of reviews
    var numPages = Math.ceil($reviews.length / reviewsPerPage);

    // Create pagination buttons
    for (var i = 1; i <= numPages; i++) {
        var $button = $('<button class="pagination-button">' + i + '</button>');
        $button.data('page', i);
        $pagination.append($button);
    }

    // Handle pagination button click
    $pagination.on('click', '.pagination-button', function() {
        var page = $(this).data('page');
        var startIndex = (page - 1) * reviewsPerPage;
        var endIndex = startIndex + reviewsPerPage;

        // Hide all reviews and show reviews for the selected page
        $reviews.hide().slice(startIndex, endIndex).show();

        // Mark the clicked button as active
        $pagination.find('.pagination-button').removeClass('active');
        $(this).addClass('active');
    });

    // Initially set the first pagination button as active
    $pagination.find('.pagination-button:first').addClass('active');

    // Handle "Write a Review" button click
    $writeReviewButton.click(function(e) {
        e.preventDefault();
        // Handle the action when the "Write a Review" button is clicked
    });
});
