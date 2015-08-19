$(document).ready(function() {

    $('#up').click(function(event){
    event.preventDefault();
    var verseid = $(this).attr("data-verse");
    
     $.get('/upvote/', {verse_id: verseid}, function(data){
               $('#bla').html(data);
               $('#refresh').show();
               $('#up').hide();
               $('#down').hide();
               
           });
});

    $('#down').click(function(event){
    event.preventDefault();
    var verseid;
    verseid = $(this).attr("data-verse");
     $.get('/downvote/', {verse_id: verseid}, function(data){
               $('#bla').html(data);
               $('#refresh').show();
               $('#up').hide();
               $('#down').hide();
           });
});
      $('#refresh').click(function(event){
    event.preventDefault();
    var verseid;
    verseid = $(this).attr("data-verse");
     $.get('/revote/', {verse_id: verseid}, function(data){
               $('#bla').html(data)
               $('#refresh').hide();
               $('#down').show();
               $('#up').show();

           });
});

});