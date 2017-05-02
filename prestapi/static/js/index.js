$(function(){
    $('#dia').on('change', function(){
        var dia_cuota = 'día ' + $('#dia').val();
        $('#dia_cuotas').text();
    });
    $('#sms-btn').on('click', function(){
        $('#phone-p').hide();
        $('#confirm-sms-p').fadeIn();
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
    $('#identificacion').slideUp(function(){
        $('.ident-btn').removeClass('btn-primary');
        $('.ident-btn').addClass('btn-default');
        $('.auten-btn').removeClass('btn-default');
        $('.auten-btn').addClass('btn-primary');
        $('#autenticacion').slideDown();
    });
});
$('#phone_number').on('input', function(){
    if(this.value.length == 10 ){
        $('#sms-btn').prop('disabled', false);
    }else{
        $('#sms-btn').prop('disabled', true);
    }
});
