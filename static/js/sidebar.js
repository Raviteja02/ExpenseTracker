$(document).ready(function () {
    $(".fa-bars").click(function () {
        $(".side-wrapper").toggleClass('not');
        $(".alternate").toggleClass('no');
    });
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    }); 
});

$("#menu-toggle").click(function(e){
    		e.preventDefault();
    		$("#wrapper").toggleClass("toggled");

    	});
