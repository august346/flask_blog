$(document).ready(function () {

    var pattern = '\\/([A-Za-z]+)\\/\\d';
    var url = window.location.href;
    var postId = false;

    var isEdit = url.search(pattern) > 0;

    var pattern2 = 'edit\\/([0-9]+)';
    if (isEdit) {
        postId = url.match(pattern2)[1];
    }


    $('#preview').on("click", function (e) {

        e.preventDefault();

        var art = {};
        art.title = $('#title').val();
        art.picture = $('#picture').val();
        art.text = $('#text').val();
        art.date = new Date().toLocaleString().split(',')[0];

        $('#prev h1').text(art.title);
        $('#prev #date').text('Posted on ' + art.date);
        $('#prev img').attr('src', art.picture);
        $('#prev #content').text(art.text);

    });

   $('#send').on("click", function (e) {

       e.preventDefault();
       if (isEdit) {
           $('#postForm').attr('action', "/edit/" + postId).submit();
       } else {
           $('#postForm').attr('action', "/new_post").submit();
       }
   });

});