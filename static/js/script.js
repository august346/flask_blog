$(document).ready(function () {



    $('.btn-danger').on('click', function (e) {
        var result = confirm("You wont to delete this post?");

        if (!result) {
            e.preventDefault();
        }
    });
});