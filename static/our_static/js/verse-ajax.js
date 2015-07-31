$(document).ready(function() {

        // JQuery code to be added in here.

});

    $('#up').click(function(event){
    event.preventDefault();
    var verseid;
    verseid = $(this).attr("data-verse");
     $.get('/upvote/', {verse_id: verseid}, function(data){
               $('#vote_count').html(data)
               $('#up').hide();
           });
});

    $('#down').click(function(event){
    event.preventDefault();
    var verseid;
    verseid = $(this).attr("data-verse");
     $.get('/downvote/', {verse_id: verseid}, function(data){
               $('#vote_count').html(data)
               $('#down').hide();
           });
});
      $('#refresh').click(function(event){
    event.preventDefault();
    var verseid;
    verseid = $(this).attr("data-verse");
     $.get('/revote/', {verse_id: verseid}, function(data){
               $('#vote_count').html(data)
               $('#re').hide();
               $('#down').show();
               $('#up').show();

           });
});

