  // =============================================
  // Disable các option đã selected đi
  // =============================================

  // 2. Lấy hết tất các giá trị element đã select 
  function get_all_selected_element(select_element){
    // 2.1. Trước khi setup disable tất cả các element thì bỏ hết tất cả các element cũ đi
    $(select_element + " option").each(function(){
      $(this).prop("disabled",false);
    }); 
    // 2.2. Lấy ra mảng giá trị đã selected
    $(select_element).each(function(){
      var contact_list_id_selected = $("option:selected",this).val();
      _list_contact_list_id_selected.push(contact_list_id_selected);
    });
  }

  // 3. Disabled các select đã chọn
  function disabled_option(select_element){
    $(select_element + " option").each(function(){
      var check_selected =  $.inArray($(this).val(), _list_contact_list_id_selected)
      // check_selected != -1 có nghĩa la có tồn tại trong mảng
      if (check_selected != -1) {
        $(this).prop("disabled",true);
      }
    });    
  }

  // 4. Dùng hàm này để gọi lại các function trên cho gọn
  function disable_selected(select_element){  
    _list_contact_list_id_selected = []
    // Trường hợp mới load trang
    get_all_selected_element(select_element);
    console.log(_list_contact_list_id_selected);
    disabled_option(select_element);
  }