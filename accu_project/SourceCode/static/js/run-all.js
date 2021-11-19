// Run All Page
$('form').submit(function () {
  disable_element($(".card"))
});

$('[data-toggle="tooltip"]').tooltip();

$('[data-toggle="popover"]').popover({
  trigger: 'hover',
})

// ===============================================================
// Ẩn sidebar trong các trường hợp đặc biệt như ở trang chọn site
// ===============================================================

function show_sidebar(){
  // 1. Khởi tạo các giá trị
  var is_superuser = $("#permission").val();
  var is_ms_group = $("#permission_ms").val();

  // 1.1 Kiểm tra có phải admin
  if (is_superuser == 'False' && is_ms_group == 'False'){
    var get_site_id_in_session = parseInt($("#site_id_in_session").val());
    var href = window.location.pathname
    var list_url = ['authentication']

    // 2. Xử lý đường dẫn
    var is_show_sidebar = true
    var check_href = (href.split('/').filter(item => item)).pop();
    list_url.forEach(function (url) {
      if ( check_href == url ){
        is_show_sidebar = false;
      }
    })

    // 3. Check có tồn tại và url có hợp lệ
    if ( !get_site_id_in_session || is_show_sidebar == false){
      $('.sidebar-toggler').hide();
    }
  }
}

$(document).ready(function(){
  show_sidebar();
})