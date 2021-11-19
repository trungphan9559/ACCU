//==================================================
// Management App Variables
//==================================================
var LOGIN_STATUS_SUCCESS = 1;
var LOGIN_STATUS_ERROR = 0;
var LOGIN_STATUS_INVALID = -1;

var AJAX_RESPONSE_STATUS_SUCCESS = 1;
var AJAX_RESPONSE_STATUS_ERROR = 0;

var _management_page_size = 20;
var _loading_bar_html = '<div class="progress"><div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div></div>';
var _progress_bar_html = '<div class="progress"><div class="progress-bar" role="progressbar" style="width: [PERCENT]%;" aria-valuenow="[PERCENT]" aria-valuemin="0" aria-valuemax="100">[PERCENT]%</div></div>';
var _progress_percent_text = '<div class="progress"><div class="progress-bar" role="progressbar" style="width: [PERCENT]%;" aria-valuenow="[PERCENT]" aria-valuemin="0" aria-valuemax="100">[PERCENT]% Complete ([TEXT])</div></div>';

//==================================================
// Lấy nội dung HTML cho loading bar
//==================================================
function get_loading_bar() {
  return _loading_bar_html;
}

//==================================================
// Set disabled cho toàn bộ Button trên Form
//==================================================
function set_disabled_buttons(isDisabled) {
  if(isDisabled) {
    $('.form-wrap button[type="button"]').attr('disabled','disabled');
    $('.form-wrap button[type="reset"]').attr('disabled','disabled');
    $('#modalEditForm button[type="button"]').attr('disabled','disabled');
    $('#pagination_box button[type="button"]').attr('disabled','disabled');
  } else {
    $('.form-wrap button[type="button"]').removeAttr('disabled');
    $('.form-wrap button[type="reset"]').removeAttr('disabled');
    $('#modalEditForm button[type="button"]').removeAttr('disabled');
    $('#pagination_box button[type="button"]').removeAttr('disabled');
  }
}

function show_progress_bar(progress_bar_id, percent) {
  //1. Show progress bar
  if($('#' + progress_bar_id + ' .progress-bar').length == 0) {
    var progress_bar_html = _progress_bar_html.replace('[PERCENT]', percent).replace('[PERCENT]', percent).replace('[PERCENT]', percent);
    $('#' + progress_bar_id).html(progress_bar_html);
    $('#' + progress_bar_id).removeClass("invisible");
  } else {
    $('#' + progress_bar_id + ' .progress-bar').width(percent + '%');
    $('#' + progress_bar_id + ' .progress-bar').html(percent + '%');
  }

  //2. Disable buttons
  set_disabled_buttons(true);
}

function hide_progress_bar(progress_bar_id) {
  $('#' + progress_bar_id).html('');
  $('#' + progress_bar_id).addClass('invisible');

  //2. Enable buttons
  set_disabled_buttons(false);
}

function show_loading_bar(loading_bar_id) { 
  //1. Show loading bar
  var html_loading_bar = _loading_bar_html;

  $('#' + loading_bar_id).html(html_loading_bar);
  $('#' + loading_bar_id).removeClass("invisible");

  //2. Disable buttons
  set_disabled_buttons(true);
}

function hide_loading_bar(loading_bar_id) {
  //1. Hide loading bar
  $('#' + loading_bar_id).html('');
  $('#' + loading_bar_id).addClass('invisible');

  //2. Enable buttons
  set_disabled_buttons(false);
}

function show_error_message(message_box_id, msg) {
  var msg_html = '<div class="alert alert-danger" role="alert">' + msg + '</div>';
  $('#' + message_box_id).removeClass("invisible");
  $('#' + message_box_id).html(msg_html);
}

function show_success_message(message_box_id, msg) {
  var msg_html = '<div class="alert alert-success" role="alert">' + msg + '</div>';
  $('#' + message_box_id).removeClass("invisible");
  $('#' + message_box_id).html(msg_html);
}

function hide_message(message_box_id) {
  $('#' + message_box_id).html('');
  $('#' + message_box_id).addClass("invisible");
}

function check_uncheck_all(element) {
  var is_checked = $(element).is(':checked');
  $('#table_data tbody input[name="check_all_item"]').prop('checked', is_checked);
}

//==================================================
// Get parammeter từ URL
//==================================================
function getQueryString(query) {
  query = query.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var expr = "[\\?&]"+query+"=([^&#]*)";
  var regex = new RegExp( expr );
  var results = regex.exec( window.location.href );
  if ( results !== null ) {
      return results[1];
  } else {
      return false;
  }
}

// ===================================================
// Checkall and uncheckall
// ===================================================
function checked_show_button(checkbox_class, div_class){
  $('.' + checkbox_class).change(function(){
    var arr_check = [];
    $('.' + checkbox_class).each(function(){
        if(this.checked == true){
          arr_check.push("1");
        }else{
          arr_check.push("0");
          $('#checkAll').prop('checked',false);
        }
    });
    if(arr_check.indexOf("1") >= 0){
      $('.' + div_class).fadeIn();
    }else{
      $('.' + div_class).fadeOut();
    }

  });
}

function checkAll(element, div_show,checkbox_item_class){
  var is_checked = $(element).is(':checked');
  $('.' + checkbox_item_class).prop('checked', is_checked);
  if(is_checked == true){
    $('.' + div_show).fadeIn();
  }else{
    $('.' + div_show).fadeOut();
  }
}

// ==========================================================
// =================== NOTIFICATION =========================
// ==========================================================
function show_notification(title, body, url){
  if (!("Notification" in window)) {
    alert("This browser does not support desktop notification");
  }

  // Let's check if the user is okay to get some notification
  else if (Notification.permission === "granted") {
      // If it's okay let's create a notification
    var options = {
            body: body,
            icon: "/static/img/brand/favicon.ico",
            dir : "ltr"
        };
    var notification = new Notification(title,options);
  }

  // Otherwise, we need to ask the user for permission
  // Note, Chrome does not implement the permission static property
  // So we have to check for NOT 'denied' instead of 'default'
  else if (Notification.permission !== 'denied') {
    Notification.requestPermission(function (permission) {
    // Whatever the user answers, we make sure we store the information
    if (!('permission' in Notification)) {
        Notification.permission = permission;
    }

    // If the user is okay, let's create a notification
    if (permission === "granted") {
        var options = {
            body: body,
            icon: "/static/img/brand/favicon.ico",
            dir : "ltr"
        };
        var notification = new Notification("ACCU Notification",options);
    }
    });
  }  

  notification.onclick = function(event) {
      event.preventDefault(); // prevent the browser from focusing the Notification's tab
      window.open(url, '_blank');
      
  }
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


// ===================================================
// Validate email
// ===================================================
function validation_email(email_input_id, email_div_id){
  $("#" + email_input_id).focusout(function(){
    var internal_email = $("#" + email_input_id).val();
    if (internal_email != ""){
      var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
      if(!filter.test(internal_email)){
        $("#" + email_div_id).append("<span class='text-danger'>Please enter your email address in format: yourname@example.com </span>")
      }else{
        $("#" + email_div_id + " span").remove();
      }
    }
  });  
}

// ================================================
// Change color when enter
// ================================================
function change_color_text_when_typed(){
  $("input").focusout(function(){
    var input = $(this).val();
    if (input != ""){
      $(this).addClass('text-primary');
    }
  });
  $("select").focusout(function(){
    var select = $(this).val();
    if (select != "0"){
      $(this).addClass('text-primary');
    }
  });
}

// ================================================
// Spinner small
// ================================================
function spinner_small(div_id){
  spinner = '<div class="sk-three-bounce"><div class="sk-child sk-bounce1"></div><div class="sk-child sk-bounce2"></div><div class="sk-child sk-bounce3"></div></div>';
  $("#" + div_id).html(spinner);
  $(".sk-three-bounce div").css('background-color','#b2bec3'); 
  $(".sk-three-bounce").css('margin','0'); 
  $(".sk-three-bounce .sk-child").css({'width':'10px','height':'10px'});  
}

// ================================================
// Init td checkbox event
// ================================================
function init_tdcheck_event() {
  $('.td-check').click(function(e) {
    var chk = $(this).closest("tr").find("input:checkbox").get(0);
    if(e.target != chk)
    {
        chk.checked = !chk.checked;
    }
  });

  $('.th-check').click(function(e) {
    var chk = $(this).closest("tr").find("input:checkbox").get(0);
    if(e.target != chk)
    {
      chk.checked = !chk.checked;

      check_uncheck_all(chk);
    }
  });
}

// ==================================================
// Show more data
// ==================================================
function init_show_all(e){
  //1)Lấy body
  var body = e.html()

  //2)Xử lý thêm vào body
  if(e.height() > 25){
      body = `<div class='div-show-all' style="max-height: 20px; overflow: hidden; width:80%; float: left">
                  ${body}
              </div> 
              <a class="show-all-button" onclick="show_all_data(this);">
                  Show All<i class="fa fa-plus-square-o ml-1"></i>
              </a>`
  }
  e.html(body)         
}

function show_all_data(e){
  var selector_div = $(e).parent().find(".div-show-all");
  $(selector_div).css('max-height', 'unset');
  $(e).html("Hide Less <i class='fa fa-minus-square-o'></i>").attr("onclick", "hide_data(this);")
}

function hide_data(e){
  var selector_div = $(e).parent().find(".div-show-all");
  $(selector_div).css('max-height', '20px');
  $(e).html("Show All<i class='fa fa-plus-square-o ml-1'></i>").attr("onclick", "show_all_data(this);")
}

// ===============================================
// ============== Show Tooltip focus =============
// ===============================================

function init_show_tooltip_focus(){
  $('[data-toggle="tooltip"]').tooltip();

  $('[data-toggle="tooltip"]').on('shown.bs.tooltip', function(){
    $(".tooltip").mouseenter(function(){
      $(this).tooltip("show")
    });
    $(".tooltip").mouseleave(function(){
      $(this).tooltip("hide")
    });
  })
}

function init_hide_tooltip(){
  $('[data-toggle="tooltip"]').tooltip("hide")
}


// ===============================================
// ============== Format Number =============
// ===============================================

function getThousandsGroupRegex(thousandsGroupStyle) {
  switch (thousandsGroupStyle) {
      case 'lakh':
          return /(\d+?)(?=(\d\d)+(\d)(?!\d))(\.\d+)?/g;

      case 'wan':
          return /(\d)(?=(\d{4})+(?!\d))/g;

      case 'thousand':
      default:
          return /(\d)(?=(\d{3})+(?!\d))/g;
  }
}

function formatNumber(str, thousandSeparator = ',', thousandsGroupStyle = 'thousand') {
  
  if(str != undefined) {
    str = str.toString();
  
    var thousandsGroupRegex = getThousandsGroupRegex(thousandsGroupStyle);
    var index = str.search(/[1-9]/);
    index = index === -1 ? str.length : index;
    return str.substring(0, index) + str.substring(index, str.length).replace(thousandsGroupRegex, '$1' + thousandSeparator);
  }
}

function convert_string_to_array(string){
  var new_list_folder = string.replaceAll("&#39;","'")
  var convert_oject = eval("[" + new_list_folder + "];")  // Convert string thành mảng nhiều chiều
  return convert_oject[0]
}

function push_param_to_url(param, current){
  if (window.location.search){
    if (window.location.href.includes(`?${current}`)){
      window.history.pushState('','', window.location.href.replace(current, '') + param)
    }else{
      window.history.pushState('','', window.location.href.replace(`&${current}`, '') + '&' + param)
    }
  }else{
    window.history.pushState('','', window.location + '?' + param)
  }    
}