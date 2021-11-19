// =================================================
// Hiển thị menu left
// =================================================
function show_left_sidebar(){
  $("body.app").addClass("sidebar-lg-show");
}

// =================================================
// Hiện active sidebar cho phần setting
// =================================================

function active_sidebar_setting(element_id){
  // Xóa active cũ của menu sidebar
  $("#menu-nav-setting a").each(function(){
    $(this).removeClass("active");
  });

  // Thêm active mới
  $("#menu-nav-setting").find("#" + element_id).addClass("active");  
}