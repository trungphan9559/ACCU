// ===================================================
// Validate input text
// ===================================================
// p_input: input muốn validate

// var _language = 'en';
var _language = 'jp';
var _msg = {
  'required': {
    'default': 'Please fill out this field!',
    'jp': '必須のフィールドに入力してください。'
  },
  'special_char': {
    'default': "Don't enter special character! ",
    'jp': '特殊文字を入力しないでください！'
  },
  'fill_out': {
    'default': "Please fill out this field line:  ",
    'jp': 'このフィールド行に入力してください：'
  },
  'remove_char': {
    'default': "Please remove special character in line: ",
    'jp': '行の特殊文字を削除してください。'
  }
}



function validate_input_text(p_input,error_div, regex_str = /[!~`@#$'%^&*-+=(),/|.?":{}|<>\\_]/){

  console.log('TEST VALID')
  
  var text_input = p_input.val()
  var is_validate = true;
  var error_html = '';
  if (text_input.trim() == ""){
    is_validate = false;
    var str = _msg['required'][_language];

    error_html = "<span class='text-danger error-required'>"+str+"</span>" 
  }   
  if(regex_str.test(text_input)){
    is_validate = false;
    var str = _msg['special_char'][_language];
    error_html = "<span class='text-danger error-required'>"+str+"</span>";      
  }    
  error_div.html(error_html)  
  return is_validate
}

function validate_input_text_area(p_input,error_div, regex_str = /[!~`@#$'%^&*-+=(),/|.?":{}|<>\\_]/){
  var keyword_name =  $("#"+p_input).val().split("\n");
  var list_keywords_line_fill = _msg['fill_out'][_language];
  var list_keywords_line_special =  _msg['remove_char'][_language];
  var is_validate = true;
  var error_html = '';
  is_need_fill = false;
  is_need_remove = false;
  for (var j = 0; j < keyword_name.length; j++) {
    var text_input = keyword_name[j]

    if (text_input.trim() == ""){
      is_validate = false;
      is_need_fill = true;
      list_keywords_line_fill += (String(j+1) + '  ')
    }   
    if(regex_str.test(text_input)){
      is_validate = false
      is_need_remove = true;
      list_keywords_line_special += (String(j+1) + '  ')
    } 

    }
    
  if(is_validate == false){
    if(is_need_fill == false){
      list_keywords_line_fill ='';
    }
    if(is_need_remove == false){
      list_keywords_line_special ='';
    }
    error_html  = list_keywords_line_fill +'<br>'+ list_keywords_line_special
  }

  error_html  = "<span class='text-danger error-required'>"+error_html +" </span>"
  error_div.html(error_html)  

  return is_validate
}



function validate_input_text_new(p_input,append_error_div, regex_str = /[!~`@#$'%^&*-+=(),/|.?":{}|<>\\_]/){
  
  var text_input = p_input.val()
  var is_validate = true;
  var error_html = '';
  if (text_input.trim() == ""){
    is_validate = false;
    var str = _msg['required'][_language];

    error_html = "<div class='col-12 error-require p-0'><span class='text-danger error-required'>"+str+"</span></div>" 
  }   
  if(regex_str.test(text_input)){
    is_validate = false;
    var str = _msg['special_char'][_language];
    error_html = "<div class='col-12 error-require p-0'><span class='text-danger error-required'>" +str+ "</span></div>"      
  }    
  append_error_div.append(error_html)  
  return is_validate
}

function remove_validate_error(){
  $(".error-require").remove();
}

function validate_select(select_label,p_select,error_div){
  var select_value = p_select.val()
  var is_validate = true;
  var error_html = '';

  if (select_value == null){
    is_validate = false
  } 
  else{
    is_validate = (select_value.length == 0) ? false : true
  }   

  if(is_validate == false){
    error_html = "<span class='text-danger error-required'>" + select_label + "を選択してください" + "。</span>"
  }
  
  error_div.html(error_html)

  return is_validate
}

function validate_email(email_id, error_div){
  var email_input = email_id.val();
  var regex_str = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  var error_html = '';
  var is_validate = true;
  if (email_input.trim() == ""){
    is_validate = false;
    var str = _msg['required'][_language];
    error_html = "<span class='text-danger error-required'>"+str+"</span>"; 
  } 
  if(!regex_str.test(email_input)){
    is_validate = false
    error_html = "<span class='text-danger error-required'>Please enter your email address in format: yourname@example.com</span>"      
  }  
  error_div.html(error_html)  
  return is_validate
}

function validate_password(password_id,div_box_li){

  //$(password_id).on("input", function(e) {
    is_validate = true;
    var input = $(password_id);
    var password_input = input.val();

    var is_length = true;
    var is_lower = true;
    var is_upper = true;
    var is_difficult = true;
    // check độ dài password
    var check_length = password_input.length

    if (check_length < 8){
      is_length = false;
      is_validate = false;
      $(div_box_li).eq(0).css('color','red');
    }
    else{
      is_length = true;
      $(div_box_li).eq(0).css('color','green');
    }

    //Kiểm tra ký tự thường
    var check_lower = /[a-z]/.test(password_input);

    if (check_lower == false){
      is_lower = false;
      is_validate = false;

      $(div_box_li).eq(1).css('color','red');
    }
    else{
      is_lower = true;
      $(div_box_li).eq(1).css('color','green');
    }

    // Kiểm tra ký tự viết hoa
    var check_upper =  /[A-Z]/.test(password_input);

    if (check_upper == false){
      is_upper = false;
      is_validate = false;

      $(div_box_li).eq(2).css('color','red');
    }
    else{
      is_upper = true;
      $(div_box_li).eq(2).css('color','green');
    }
    
    // Kiểm tra biến số, ký tự đặc biệt
    var is_number_exist = /[0-9]/.test(password_input)
    var is_special_char = /[!@#$%^_&*()\s,.?":{}|<>]/.test(password_input)

    var check_difficult =  is_number_exist ||  is_special_char;
    
    if (check_difficult == false){
      is_difficult = false;
      is_validate = false;

      $(div_box_li).eq(3).css('color','red');
    }
    else{
      is_difficult = true;
      $(div_box_li).eq(3).css('color','green');
    }

  return is_validate
}

function validate_checkbox(select_label,input_checked,error_div){
  var checkbox_value = []
  input_checked.each(function(){
    var value_checkbox = $(this).val();
    checkbox_value.push(value_checkbox);
  });

  var is_validate = true;
  var error_html = '';

  if (checkbox_value == null){
    is_validate = false
  } 
  else{
    is_validate = (checkbox_value.length == 0) ? false : true
  }   

  if(is_validate == false){

    error_html = "<span class='text-danger error-required'>Please choose " + select_label + "!</span>"
  }
  
  error_div.html(error_html)


  return is_validate
}

function validate_phone(e, insert_after_element){
  $(".error-phone-number").remove();
  html_error = "<div class='col-12 error-phone-number p-0'><span class='text-danger error-required'>Your phone is invalid. Please enter only numbers.</span></div>"
  var text = $(e).val();
  
  if (/^[0-9]*$/.test(text) == false){
    if (insert_after_element == undefined) {
      $(html_error).insertAfter($(e));
    }else{
      $(html_error).insertAfter($(insert_after_element));
    }
  }
  
  var number_in_text = text.match(/\d+/);
  $(e).val(number_in_text);   
}

// ==================================
// =========== Validate =============
// ==================================

// Message

const list_message_default = {
  'required' : "必須項目です。",
  'size_file' : "Dung lượng file vượt quá tối đa cho phép"
}

function message_error(message, type){
  let error_html = ''

  if ( message ){
    error_html = `<small class="text-danger d-block errors-validate">${message}</small>`
  } else {
    error_html = `<small class="text-danger d-block errors-validate">${list_message_default[type]}</small>`
  }

  return error_html
}

// 1. Required input text, select
function validate_required (list_element ,message){
  let error_html = message_error(message, 'required')
  
  for ( element of list_element ) {
    if( !$(element).val() || $(element).val() == '-1'){
      $(error_html).appendTo($(element).closest('.form-group'));
    }
  }
}

// 2. Required input file
function validate_required_file(list_element ,message){
  let error_html = message_error(message, 'required')
  
  for ( element of list_element ) {
    if( $(element)[0].files[0] === undefined ){
      $(error_html).appendTo($(element).closest('.form-group'));
    }
  }
}

// 3. Limit size file
function validate_size_file(list_element ,message, maximum_size){
  let error_html = message_error(message, 'size_file')
  for ( element of list_element ) {
    if( $(element)[0].files[0].size > maximum_size ){
      $(error_html).appendTo($(element).closest('.form-group'));
    }
  }
}

// Remove error when enter input 
function change_value(e){
  $(e).closest('.form-group').find('.errors-validate').remove();
}

// Remove old error
function remove_error_validate(){
  $('.errors-validate').remove();
}