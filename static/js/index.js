$(function(){
    var actual_status = setInterval(function(){ request_status() }, 10000);
});
var score_result = 'pending';

function manage_score_response(data){
    console.log(data);
    $('#confirm-sms-p').hide();
    if (data.status) {
        if (data.response === 'denied') {
            // Muestro denegado
            show_verification_error('Transacción finalizada: solicitud de credito denegada.');
        }else if (data.response === 'pending') {
            // Muestro pendiente
            show_verification_error('Transacción finalizada: tu solicitud está en revisión, pronto nos pondremos en contacto contigo.');
        }else if(data.response === 'approved'){
            // Muestro aprobado
            show_verification_success('Transacción finalizada: solicitud de credito aprobada.');
        }else{
            console.log('index.js:manage_score_response:plop')
        }
        // Se notifica al E-Commerce
    }else{
        show_verification_error('No se pudo generar un puntaje con los datos suministrados.');
    }
}
function show_verification_success(msg){
    $('#verification_error_msg').hide();
    var html = '<p>'+msg+'</p><a href="'+global_confirmation_url+'" class="btn btn-default">Volver al E-Commerce</a>';
    $('#verification_success_msg').html(html);
    $('#verification_success_msg').fadeIn();
}
function show_verification_error(msg){
    $('#verification_success_msg').hide();
    var html = '<p>'+msg+'</p><a href="'+global_confirmation_url+'" class="btn btn-default">Volver al E-Commerce</a>';
    $('#verification_error_msg').html(html);
    $('#verification_error_msg').fadeIn();
}
function show_form_error(msg){
    $('#form_error_msg').text(msg);
    $('#form_error_msg').fadeIn();
}
sinchClient = new SinchClient({
	applicationKey: 'e55639fd-6e4a-40a1-ac22-4301e8ec619b',
});
var ongoingVerification;
function send_email(){

}
function send_sms(){
    clearMsg();
	var selectedPhoneNumber = $('input#phone').val();
    selectedPhoneNumber = '+57'+selectedPhoneNumber;
    if(selectedPhoneNumber){
        console.log('Se enviará un SMS de verificación a:', selectedPhoneNumber);
        ongoingVerification = sinchClient.createSmsVerification(selectedPhoneNumber);
    	ongoingVerification.initiate().then(function() {
    		//If successful
            $('#phone-p').hide();
            $('#confirm-sms-p').fadeIn();
    	}).fail(handleError);
    }else{
        console.log('Debe insertar un número');
    }
}
$('#finish-btn').on('click', function(){
    event.preventDefault();
	clearMsg();
	var verificationCode = $('input#confirmation_code').val();
	ongoingVerification.verify(verificationCode).then(function() {
        check_email_code(verificationCode);
	}).fail(handleError);
});
$(function(){
    $('#dia').on('change', function(){
        var dia_cuota = 'día ' + $('#dia').val();
        $('#dia_cuotas').text();
    });
    $('#sms-btn').on('click', function(){
        $('#phone-p').hide();
        $('#confirm-sms-p').fadeIn();
        $('#dia_cuotas').text(dia_cuota);
    });
    $('.datepicker').datepicker({
        format: "yyyy-mm-dd",
        language: "es",
        keyboardNavigation: false,
        autoclose: true,
        todayHighlight: true
    });
});
function calcular_cuota(subtotal, tasa, meses) {
    var cuota = (tasa*subtotal)/(1-(Math.pow((1+tasa),-meses)));
    $('#valor_cuotas').text('$' + parseInt(cuota).toLocaleString() + '/mes');
    $('#num_cuotas').text(meses + ' cuotas');
    $('#dia_cuotas').text('día ' + $('#dia').val());
    var inte = calcular_interes(subtotal, tasa, meses, cuota);
    return inte;
}
function calcular_interes(subtotal, tasa, meses, cuota) {
    var interes = 0;
    if(meses == 1){
        interes = subtotal*tasa;
        $('#interes').text('$' + parseInt(interes).toLocaleString());
        return interes;
    }else{
        interes = subtotal*tasa;
        interes_total = interes
        for (var i = 1; i < meses; i++) {
            interes_mes = (subtotal - cuota + interes) * tasa;
            subtotal = subtotal - cuota + interes
            interes_total += interes_mes;
            interes = interes_mes;
        }
        $('#interes').text('$ ' + parseInt(interes_total).toLocaleString());
        return interes_total;
    }
}
$('#continuar').on('click', function(){
    $('#financiacion').slideUp(function(){
        $('.finan-btn').removeClass('btn-primary');
        $('.finan-btn').addClass('btn-default');
        $('.ident-btn').removeClass('btn-default');
        $('.ident-btn').addClass('btn-primary');
        $('#identificacion').slideDown();
    });
});

$('#continuar2').on('click', function(){
    jQuery.extend(jQuery.validator.messages, {
        required: "Campo requerido",
        email: "Correo electrónico inválido",
        number: "Debe contener unicamente números",
    });
    $('#request_form').validate({
        errorPlacement: function(error, element) {
            if (element.attr("name") == "policy"){
                error.insertAfter($('#custom_error_policy'));
            }else{
                error.insertAfter(element);
            }
        },
    });
    if($('#request_form').valid()){
        $('#identificacion').slideUp(function(){
            $('#final_phone').text($('#phone').val());
            $('#final_email').text($('#email').val());
            $('#aprobacion').slideDown(function(){
                create_new_user();
            });
        });
    }else{
        show_form_error('Se encontraron errores en los campos del formulario.');
        document.getElementById('form_error_msg').scrollIntoView();
    }
});
$('#phone_number').on('input', function(){
    if(this.value.length == 10 ){
        $('#sms-btn').prop('disabled', false);
    }else{
        $('#sms-btn').prop('disabled', true);
    }
});
$('#confirmation_code').on('input', function(){
    if(this.value.length == 4 ){
        $('#finish-btn').prop('disabled', false);
    }else{
        $('#finish-btn').prop('disabled', true);
    }
});
$('#finish-btn').on('click', function(){
    $('#confirm-sms-p').hide();
    $('#final-p').fadeIn();
});
var handleError = function(error) {
	console.log('Verification error', error);
    show_verification_error('Error al verificar el codigo enviado al celular, porfavor intente de nuevo.');
}

/** Always clear errors and successes **/
var clearMsg = function() {
	$('#verification_error_msg').hide();
    $('#verification_success_msg').hide();
}
