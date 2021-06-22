$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
/*
    if (window.location.href.indexOf("/topup") > -1) {
        $("#navbar-support-item").removeClass("active");
        $("#navbar-topup-item").addClass("active");
    }
*/
});
/*
var header = document.getElementById("navbarSupportedContent");
var btns = header.getElementsByClassName("nav-item active");
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function() {
  var current = document.getElementsByClassName("active");
  current[0].className = current[0].className.replace(" active", "");
  this.className += " active";
  });
}

*/



