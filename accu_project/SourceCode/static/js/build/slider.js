// ====================================================================
// ============================ SLIDER ================================
// ====================================================================
// slider(max_number, grid_value, slider_value, slider_id, is_grid);
// max_number: giới hạn thanh hiển thị là bao nhiêu
// grid_value: số liệu hiển thị trên grid cách nhau khoảng bao nhiêu
// slider_value: truyền giá trị hiện tại
// slider_id: id trong code html của slider
// is_grid: có bật grid lên không (true: có, false: không)
// function_name: hàm sẽ thực hiện
function slider(max_number, grid_value, slider_value, slider_id, is_grid){
  var max = max_number;
  var custom_values = [];
  for (var i = 0; i <= max; i+=grid_value){
    custom_values.push(i)
  }   

  var my_from = custom_values.indexOf(parseInt(slider_value));
  
  $("#" + slider_id).ionRangeSlider({
      grid: is_grid,
      from: my_from,
      step: grid_value,
      values: custom_values,
      from_min: slider_value,
  });

  $(".irs-min, .irs-max").css({'color':'#5c6873', 'font-weight':'bold'});
  $(".irs-single").css({'background':'#20a8d8', 'font-weight':'bold'});
}