// =====================================================================================
// Xử lý chuỗi (xóa ký tự đặc biệt và thay thế khoảng trắng bằng gạch dưới) - giống slug
// =====================================================================================
function remove_special_character_and_more (str){
  string_output = str.toLowerCase().replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '_') 
  return string_output;
}

// ===================================================
// Copy all text
// ===================================================
function copyText(div, icon_id) {
  var srcObj = document.getElementById (div);
  var range, selection, worked;

  if (document.body.createTextRange) {
      range = document.body.createTextRange();
      range.moveToElementText(srcObj);
      range.select();
  } else if (window.getSelection) {
      selection = window.getSelection();        
      range = document.createRange();
      range.selectNodeContents(srcObj);
      selection.removeAllRanges();
      selection.addRange(range);
  }
  
  try {
      document.execCommand('copy');
      $("#" + icon_id).addClass("text-success");        
  }
  catch (err) {
      alert('Error data can\'t copy');
  }
}