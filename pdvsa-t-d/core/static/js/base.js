$(document).ready(function() {
	$('.F-valid').bootstrapValidator({
		message: 'El Valor no es Valido',
	        feedbackIcons: {
	            valid: 'glyphicon glyphicon-ok',
	            invalid: 'glyphicon glyphicon-remove',
	            validating: 'glyphicon glyphicon-refresh'
	        }
	});
	
$('.datatable').dataTable({
    "language": {
        "lengthMenu": "Mostrando _MENU_ Registros",
        "zeroRecords": "No se encontraron registros",
        "info": "Pagina _PAGE_ de _PAGES_",
        "infoEmpty": "No hay registros",
        "infoFiltered": "(Se filtraron _MAX_ Registros en total)",
        "search":         "<div class='glyphicon glyphicon-filter'></div>",
        "paginate": {
            "first":      "Inicio",
            "last":       "Fin",
            "next":       "Siguiente <span aria-hidden='true'>&rarr;</span>",
            "previous":   "<span aria-hidden='true'>&larr;</span> Anterior"
        },
    }
} );

$('.datatablesimple').dataTable({
	bFilter: false,
	bInfo: false,
	paginate: false,
 
} );

$('.selects2').select2();
});


$('.date').datetimepicker({
	 locale: 'es',
	format: 'DD-MM-YYYY'
});

$('.date2').datetimepicker({
	 locale: 'es',
	format: 'YYYY-MM-DD H:m',
});


$(':checkbox').bootstrapToggle({
	 on: 'Si',
     off: 'No'
});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break; 
            }
        }
    }
    return cookieValue;
}

function fncSumar(v){
	var total = 0.0;
	var clase = $(v).attr('class').split(" ");
	$('.'+clase[0]).each(function(){
		if($(this).val()!= ""){			
		total = total +  parseFloat($(this).val());	
		/*
		console.log("Planificacion: " + clase[0]);
		console.log("mes: "+$(this).data('mes'));
		console.log("actividad: "+$(this).data('actividad'));
		console.log("proceso: "+$(this).data('proceso'));
		console.log("Valor: " + $(this).val());
		*/
		}
	});
	$('#'+clase[0]).val(total);
}


$(".int").keydown(function (e) {
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
        (e.keyCode == 65 && e.ctrlKey === true) || 
        (e.keyCode >= 35 && e.keyCode <= 39)) {
             return;
    }

    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
    	e.preventDefault();
    }
});


$("table input").keydown(function (e) {
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
        (e.keyCode == 65 && e.ctrlKey === true) || 
        (e.keyCode >= 35 && e.keyCode <= 39)) {
             return;
    }

    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
    	e.preventDefault();
    }
});

$('#btn_save_table').on('click', function(){
	send_table();
});

function send_table(){
	var list = [];
	var dic = {};
	var ant = 0;
	var init = 0;
	$('.datos').each(function(){
		if(init==0){
			ant = $(this).data('id');
			init = 1;
		}
		if(ant==$(this).data('id')){		
			dic["id"] = $(this).data('id');
			dic[$(this).data('tipo')] = $(this).val();
			if(dic.id && dic.plan_sap && dic.plan_meta && dic.real_mc && dic.plan_hh && dic.real_hh ){
				list.push(dic);
				dic = {};
			}
		}else{		
			dic["id"] = $(this).data('id');
			dic[$(this).data('tipo')] = $(this).val();
		}
		ant = $(this).data('id');
		
	});
    $.ajax({
        url: '/control/save_table/',
        type: 'POST',
        data: {'lista': list},
        beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));}
    }).done(function(json) {
    	
    });
}


(function($){
	$(document).ready(function(){
		$('ul.dropdown-menu [data-toggle=dropdown]').on('click', function(event) {
			event.preventDefault(); 
			event.stopPropagation(); 
			$(this).parent().siblings().removeClass('open');
			$(this).parent().toggleClass('open');
		});
	});
})(jQuery);
