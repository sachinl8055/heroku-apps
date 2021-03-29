
// Scrolling Effect

$(window).on("scroll", function () {
  if ($(window).scrollTop()) {
    $('nav').addClass('black');
  }

  else {
    $('nav').removeClass('black');
  }
})

$('#image').click(function(){
  $('#myfile').click()
})
/******* Map Functionality  */

window.onload = function () {

}

var readProductImg = function(event){
  var pro_img = document.getElementById('image');

  var file = event.files[0];  
  var reader = new FileReader();  
  reader.onloadend = function() {  
    pro_img.src = reader.result;  
  }  
  reader.readAsDataURL(file);
}