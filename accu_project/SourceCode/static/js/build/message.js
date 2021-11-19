function show_error_message(message_box_id, msg) {
  var msg_html = '<div class="alert alert-danger mb-0" role="alert">' + msg + '</div>';
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

function show_error_required_message(message_box_id, msg='必須フィールドに入力してください。') {
  var msg_html = '<div class="alert alert-danger" role="alert">' + msg + '</div>';
  $('#' + message_box_id).removeClass("invisible");
  $('#' + message_box_id).html(msg_html);
}

function show_success_message_in_modal(modal_id, msg) {
  var msg_html = '<div class="alert alert-success" role="alert">' + msg + '</div>';
  var e_message = $('#' + modal_id + ' #message')
  e_message.removeClass("invisible");
  e_message.html(msg_html);
}

function show_error_message_in_modal(modal_id, msg) {
  var msg_html = '<div class="alert alert-danger" role="alert">' + msg + '</div>';
  var e_message = $('#' + modal_id + ' #message')
  e_message.removeClass("invisible");
  e_message.html(msg_html);
}

function hide_message_in_modal(modal_id) {
  var e_message = $('#' + modal_id + ' #message')
  e_message.html('');
  e_message.addClass("invisible");
}