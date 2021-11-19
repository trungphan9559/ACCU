//==================================================
// Management App Variables
//==================================================
var LOGIN_STATUS_SUCCESS = 1;
var LOGIN_STATUS_ERROR = 0;
var LOGIN_STATUS_INVALID = -1;

var AJAX_RESPONSE_STATUS_SUCCESS = 1;
var AJAX_RESPONSE_STATUS_ERROR = 0;

var _management_page_size = 5;
var _loading_bar_html = '<div class="progress"><div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div></div>';
var _progress_bar_html = '<div class="progress"><div class="progress-bar" role="progressbar" style="width: [PERCENT]%;" aria-valuenow="[PERCENT]" aria-valuemin="0" aria-valuemax="100">[PERCENT]%</div></div>';

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

function show_progress_bar_text(progress_bar_id, text) {
  //1. Show progress bar
  if($('#' + progress_bar_id + ' .progress-bar').length == 0) {
    var progress_bar_html = _progress_bar_html.replace('[PERCENT]', percent).replace('[PERCENT]', percent).replace('[PERCENT]', percent);
    $('#' + progress_bar_id).html(progress_bar_html);
    $('#' + progress_bar_id).removeClass("invisible");
  } else {
    $('#' + progress_bar_id + ' .progress-bar').width('100%');
    $('#' + progress_bar_id + ' .progress-bar').html(text);
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
  console.log('check_uncheck_all');
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