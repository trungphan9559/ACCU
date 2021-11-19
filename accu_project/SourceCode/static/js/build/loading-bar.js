//=========================================================
// Show loading bar Core UI
//=========================================================
function show_loading_bar_CoreUI(element_id){
  $('#' + element_id).removeClass("invisible");
  progress_coreui = '<div class="progress-bar mb-2 rounded">'+
                      '<div class="progress">'+
                        '<div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div>'+
                      '</div>'+ 
                    '</div> '   
  $('#' + element_id).html(progress_coreui);
}

function hide_loading_bar_CoreUI(element_id){
  $("#"+element_id).children().remove();
}

function show_loading_bar_CoreUI_with_elem($this){
  $this.removeClass("invisible");
  progress_coreui = '<div class="progress-bar mb-2 rounded">'+
                      '<div class="progress">'+
                        '<div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div>'+
                      '</div>'+ 
                    '</div> '   
  $this.html(progress_coreui);
}

// =====================================================
// Progress bar
// =====================================================
function show_progress_bar(progress_bar_id, percent) {
  var _progress_bar_html = '<div class="progress"><div class="progress-bar" role="progressbar" style="width: [PERCENT]%;" aria-valuenow="[PERCENT]" aria-valuemin="0" aria-valuemax="100">[PERCENT]%</div></div>';
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
  //set_disabled_buttons(true);
}

function hide_progress_bar(progress_bar_id) {
  $('#' + progress_bar_id).html('');
  $('#' + progress_bar_id).addClass('invisible');

  //2. Enable buttons
  //set_disabled_buttons(false);
}

// ================================================
// Loading Spinner small
// ================================================
function spinner_small(div_id){
  spinner = '<div class="sk-three-bounce">' + 
              '<div class="sk-child sk-bounce1"></div>' + 
              '<div class="sk-child sk-bounce2"></div>'+
              '<div class="sk-child sk-bounce3"></div>'+
            '</div>';
  $("#" + div_id).html(spinner);
  $(".sk-three-bounce div").css('background-color','#b2bec3'); 
  $(".sk-three-bounce").css('margin','0'); 
  $(".sk-three-bounce .sk-child").css({'width':'10px','height':'10px'});  
}

function loading_small(div_id){
  spinner = '<div class="sk-three-bounce">' + 
              '<div class="sk-child sk-bounce1"></div>' + 
              '<div class="sk-child sk-bounce2"></div>'+
              '<div class="sk-child sk-bounce3"></div>'+
            '</div>';
  $("#" + div_id).html(spinner);
  $("#"+div_id+" .sk-three-bounce div").css('background-color','#b2bec3'); 
  $("#"+div_id+" .sk-three-bounce").css('margin','0'); 
  $("#"+div_id+" .sk-three-bounce .sk-child").css({'width':'10px','height':'10px'});  
}

function loading_default(div_id){
  spinner = '<div class="sk-three-bounce">' + 
              '<div class="sk-child sk-bounce1"></div>' + 
              '<div class="sk-child sk-bounce2"></div>'+
              '<div class="sk-child sk-bounce3"></div>'+
            '</div>';
  $(div_id).html(spinner);
  $(".sk-three-bounce div").css('background-color','#b2bec3'); 
  $(".sk-three-bounce").css({'margin':'auto', 'paddingTop': 30});  
}

// ================================================
// Chart loading
// ================================================ 
function chart_loading(div_id, height = "", pt = "100"){
  spinner = '<div style="height:' + height + 'px;">' +
              '<div class="sk-three-bounce mb-0" style="padding-top:' + pt + 'px;">' +
                '<div class="sk-child sk-bounce1"></div>' +
                '<div class="sk-child sk-bounce2"></div>' +
                '<div class="sk-child sk-bounce3"></div>' +
              '</div>' +
              '<p class="text-center" style="color: #b2bec3">Chart loading...</p>' +
            '</div>';
  $("#" + div_id).html(spinner);
  $(".sk-three-bounce div").css('background-color','#b2bec3'); 
}

// ================================================
// Disable, Enable item
// ================================================ 
function disable_element(e) {
  //1)Disable đi không cho bấm vào
  e.css({ 'pointer-events': 'none', 'position': 'relative'});
  spinner = 
              '<div class="sk-three-bounce d-flex align-items-center">' +
                '<div class="sk-child sk-bounce1" style="margin-left: calc(50% - 30px); background: #73818f "></div>' +
                '<div class="sk-child sk-bounce2" style="background: #73818f"></div>' +
                '<div class="sk-child sk-bounce3" style="background: #73818f"></div>' +
              '</div>'
            ;

  e_width = e.width()
  e_height = e.height()

  //2)Thêm spinner
  e.append(spinner)
  $spinner = e.find('.sk-three-bounce').first()

  // spinner_width = $spinner.width()
  // spinner_height = $spinner.height()

  $spinner.css({
    'width' : '100%',
    'height' : '100%',
    'background' : '#fff',
    'opacity' : '0.6',
    'position' : 'absolute',
    'margin' : '0',
    'top' : '50%',
    'left' : '50%',
    'transform' : 'translate(-50%, -50%)',
    'z-index' : '200'
  })

  // $spinner.children().css({
  //   'margin-left' : 'calc(50% - 80px)'
  // })

  // $spinner.css('width', '100%');
  // $spinner.css('position', 'absolute');
  // $spinner.css('margin', '0');
  // $spinner.css('top', '50%');
  // $spinner.css('left', '50%');
  // $spinner.css('transform', 'translate(-50%, -50%)');

  // 3) Khóa hết tất cả các nav-link tab không cho nhấn vào khi load
  $(".nav-item").each(function () {
    $(this).css({ 'pointer-events': 'none', 'opacity': '0.5' })
  });

  // 4) Khóa hết các nút
  $(".btn, .btn-sm").each(function () {
    $(this).css({ 'pointer-events': 'none', 'opacity': '0.5' })
  });

}

function enable_element(e) {
  //1)Xóa spinner đi
  $spinner = e.find('.sk-three-bounce').first()
  $spinner.remove()

  //2)Mở ra lại bình thường
  e.css({ 'pointer-events': 'auto', 'opacity': '1' });

  // 3) Mở hết tất cả các nav-link đã khóa
  $(".nav-item").each(function () {
    $(this).css({ 'pointer-events': 'auto', 'opacity': '1' })
  });

  // 4) Khóa hết các nút
  $(".btn, .btn-sm").each(function () {
    $(this).css({ 'pointer-events': 'auto', 'opacity': '1' })
  });
}

function click_tab_show_loading (selector_click, variable, selector_show_loading) {
  selector_click.click(function(){
    if (variable == false){
      variable = true
      disable_element(selector_show_loading);
    }
  });
}