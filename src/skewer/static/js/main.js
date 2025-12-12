document.addEventListener('DOMContentLoaded', function () {
    var loader = document.getElementById('loading-overlay');

    // Show loader when clicking links that are not #, not new tab, and not download
    document.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function (e) {
            var href = link.getAttribute('href');
            if (href && href !== '#' && !href.startsWith('javascript') && link.target !== '_blank') {
                loader.classList.remove('d-none');
            }
        });
    });

    // Show loader on form submit
    document.querySelectorAll('form').forEach(function (form) {
        form.addEventListener('submit', function () {
            loader.classList.remove('d-none');
        });
    });

    // Hide loader when page is shown (fixes back button issue in some browsers)
    window.addEventListener('pageshow', function () {
        loader.classList.add('d-none');
    });
});
