$(document).ready(function() {
  $.ajaxSetup({ cache: true });
  $.getScript('//connect.facebook.net/en_US/sdk.js', function(){
    FB.init({
      appId: '1946794675549597',
      version: 'v2.8' // or v2.1, v2.2, v2.3, ...
    });
    $('.facebook-login').on('click', function(){
        $('.fb-loading-icon').fadeIn();
        FB.getLoginStatus(function(response){
            if (response.status === 'connected') {
                get_user_data();
                $('.fb-loading-icon').fadeOut(function(){
                    $('.fb-completed-icon').fadeIn();
                    $('#continuar2').prop('disabled', false);
                });
            }else {
                FB.login(function(){
                    get_user_data();
                    $('.fb-loading-icon').fadeOut(function(){
                        $('.fb-completed-icon').fadeIn();
                        $('#continuar2').prop('disabled', false);
                    });
                }, {scope: 'email, public_profile, user_friends, user_relationships, user_birthday, user_hometown'});
            }
        });
    });
  });
});
function get_user_data(){
    var query = "/me?fields=id,name,email,gender,birthday,locale,education,hometown,location,family,picture,relationship_status,religion,significant_other,verified,work,political,about,cover";
    FB.api(query, function (response) {
        if (response && !response.error) {
            console.log(response);
        }else{
            console.log(response.error);
        }
    });
}


function get_user_photo(){
    FB.api("/me/picture", function (response) {
        if (response && !response.error) {
            console.log(response.data.url);
        }else{
            console.log(response.error);
        }
    });
}
function get_user_friends(){
    FB.api("/me/friendlists", function (response) {
        if (response && !response.error) {
            console.log(response);
            for (var i = 0; i < response.data.length; i++) {
                var tmp_id = response.data[i].id
                FB.api("/"+tmp_id, function (response) {
                    if (response && !response.error) {
                        console.log('list: ');
                        console.log(response);
                    }else{
                        console.log(response.error);
                    }
                });
            }
        }else{
            console.log(response.error);
        }
    });
}
