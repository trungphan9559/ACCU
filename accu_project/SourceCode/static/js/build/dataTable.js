// ================================================
// Data Table

//const { FALSE } = require("node-sass");

// ================================================
function init_data_table(table_id,option = {}){
  //1)Phần thêm setting cho data Table
  setting = {
    "aLengthMenu"   :   [[10, 25, 50,100,500,1000, -1], [10, 25, 50,100,500,1000, "All"]],
    "bPaginate"     :   option.bPaginate != undefined ?  option.bPaginate : true,  //1)Thanh phân trang ở  góc phải bên dưới
    "bLengthChange" :   option.bPaginate != undefined ?  option.bPaginate : true,  //2)Số cột muốn hiển thị, cái này phải đi đôi với bPaginate
    "searching"     :   option.searching != undefined ?  option.searching : true,  //3)Cái ô search ở góc phía trên
    "info"          :   option.info != undefined ?  option.info : true,            //4)Hiển thị "1 to n of n entries" ở phía dưới
    "scrollX"       :   option.scrollX != undefined ?  option.scrollX : true,      //5)Cho phép hiển thị scoll bar theo chiều ngang
    "bSort"         :   option.bSort != undefined ?  option.bSort : true,          //6)Có cho phép sort hay là không trên toàn bộ table
    "select"        :   option.select != undefined ?  option.select : false,        //7)Bấm vào 1 hàng thì nó sáng lên
    "bStateSave"    :   true,                                                      //8)Khi load lại trang thì người dùng vẫn load lại trang đã dùng trước đó
    "autoWidth"     :   false,
    "fixedHeader"   :   option.fixedHeader != undefined ? option.fixedHeader : {header: true, headerOffset: $('header').height()},
    "columnDefs"    :   [{
                          "targets": "no-sort",
                          "orderable": false
                        }],
    "language"      :   {
                          "lengthMenu"  : "_MENU_",
                        }
  };
      //Vị trí của các element trong Datatable
    setting['dom'] = '<"row" <"col-12"f> >t<"row" <"col-4" i> <"col-8" l p>>'
  

  //2)Cài đặt Data Table
  var table = $('#' + table_id).DataTable(setting);

  //3)Style cho data table
  $('button.dt-button').addClass('btn btn-info text-white');

  $('button.buttons-html5').prepend('<i class="fa fa-download"></i> ');
  // Style cho khung search
  $(".dataTables_filter input").css({"height":"35px","width":"220px"});
  $(".dataTables_length select").css("height","35px");

  table.columns().iterator( 'column', function (ctx, idx) {
    $( table.column(idx).header() ).append('<span class="sort-icon"/>');
  });

  //3) Xóa cache sau khi search
  //$('#' + table_id  + "_filter").find('input').val('');
  //$('#' + table_id).DataTable().search('').draw();

}

// ===================================================
// Js cho phần hover vào mỗi hàng thì show lên các nút 
// ===================================================
function hover_table_show_button(){
  $('table tbody tr td div.button-action').hide();
  $('table tbody tr td').mouseover(function(){
      $(this).closest('table tbody tr').find('div.button-action').show();
  });  
  $('table tbody tr').mouseout(function(){
      $(this).closest('table tbody tr').find('div.button-action').hide();
  });  
}


function catch_event_in_table(table_id,funct){
  //Truyền vào argument là funtion không có () , Ex : test() --> test

  //1) bắt sự kiện filter số lượng cột
  $('#' + table_id + '_length').find('label select').on('change',function() {

    funct();

  });
  
  //2)bắt sự kiện next trang
  $('#' + table_id+ '_paginate').on('click',function() {

    funct();

  });
  
  //3) bắt sự kiện sorting_asc
  $('#' + table_id).find('th.sorting_asc').on('click',function() {
  
    funct();

  });
  
  //4) bắt sự kiện sorting_desc
  $('#' + table_id).find('th.sorting_desc').on('click',function() {
   
    funct();
   
  });
  
  //5) bắt sự kiện sorting
  $('#' + table_id).find('th.sorting').on('click',function() {

    funct();
   
  });
  
  //5) Bắt sự kiện Search
  $('#' + table_id+ '_filter').on("input", function(e){

    funct();  

  });

}

// =================================================
// ======== FUNTIONS SETTING FOR DATATABLE =========
// =================================================

function get_option_datatable_disable_search(option_addition){
  
  var option_default = {
    "pageLength": 50,
    "order": [],
    "language": {
      "lengthMenu": "_MENU_",
      "emptyTable": "現在表示できるデータがありません",
      "infoEmpty": "",
      "paginate": {
        "previous": "前へ",
        "next": "次へ"
      }
    },
    stateSave: true, // Lưu các giá trị trang, cột vào session
    "LengthMenu": [[-1, 10, 50, 100, 500], ["All", 10, 50, 100, 500]],
    "columnDefs": [{
      "targets": 'no-sort',
      "orderable": false,
    }],
    'dom': '<"row" <"col-12"f> >t<"row" <"col-4" i> <"col-8" l p>>',
  }

  if (option_addition){
    return {...option_default, ...option_addition}
  }else{
    return option_default
  }
}

function get_option_datatable(option_addition){
  
  var option_default = {
    "pageLength": 50,
    "order": [],
    "language": {
      "lengthMenu": "_MENU_",
      "emptyTable": "No data",
      "infoEmpty": "",
      "search":"",
      "paginate": {
        "previous": "previous",
        "next": "next"
      }
    },
    stateSave: true, // Lưu các giá trị trang, cột vào session
    "LengthMenu": [[-1, 10, 50, 100], ["All", 10, 50, 100]],
    "columnDefs": [{
      "targets": 'no-sort',
      "orderable": false,
    }],
    'dom': '<"row" <"col-12"f> >t<"row" <"col-4" i> <"col-8" l p>>',
  }

  if (option_addition){
    return {...option_default, ...option_addition}
  }else{
    return option_default
  }
}

function show_sort_datatable(table){
  table.columns().iterator('column', function (ctx, idx) {
    $(table.column(idx).header()).append('<span class="sort-icon"/>');
  });

  $(".dataTables_filter input").css({ "height": "28px", "width": "200px" });
  $(".dataTables_filter input[type='search']").attr('placeholder', 'Search...');
  $(".dataTables_length select").css("height", "35px");
}

function get_scroll_table(max_width){
  var window_width = window.innerWidth;
  scrollX = false;
  if (window_width < max_width) {
    scrollX = true;
    $("table").addClass("nowrap")
  }

  return scrollX
 
}