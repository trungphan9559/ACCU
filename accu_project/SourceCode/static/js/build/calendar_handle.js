var start_day = moment().format("YYYY-MM-D");
var end_day = moment().format("YYYY-MM-D");

function get_start_date_and_end_date(calendar_id){
  var date = $("#" + calendar_id + " span").text();
  list_date = date.split(" - ");
  return {
      'start_date' : list_date[0],
      'end_date' : list_date[1],
  }
}

function init_calendar_single(calendar_id, input, startDate=true, endDate= false) {
  if (input != "None" && input != '') {
    var format_date = moment(input).format('MM/DD/YYYY');
    var cb = function (input) {
      //Hiển thị cho khách hàng tháng/ngày/năm
      $("#"+ calendar_id +" span").html(input.format("YYYY/MM/DD"));
    };
    //Đặt dữ liệu mặc định cho Chart
    var option = {
      dateFormat: "YYYY-MM-DD",
      format: "YYYY/MM/DD",
      singleDatePicker: true,
      showDropdowns: true,
      minDate: "01/01/2012",
      maxDate: moment().endOf("day")
    };
    if (startDate == true) {
      option['startDate'] = format_date;
      option['minDate'] = format_date;
      // $("#" + calendar_id + " span").html('Start date');
    }
    if (endDate == true) {
      option['endDate'] = format_date;
      option['maxDate'] = format_date;
      // $("#" + calendar_id + " span").html('End date');
    } 
    
    $("#"+ calendar_id).daterangepicker(option, cb);
  } else {
    $("#" + calendar_id + " span").html(input);
  }
  
}

function init_calendar(calendar_id,date_range=6) {
  
  var cb = function (start, end, label) {
    //Hiển thị cho khách hàng tháng/ngày/năm
    $("#"+ calendar_id +" span").html(start.format("YYYY-MM-DD") + " - " + end.format("YYYY-MM-DD"));
  };
  var optionSet1 = {
    dateFormat: "YYYY-MM-DD",
    startDate: moment().subtract(date_range, "days"),
    endDate: moment(),
    minDate: "01/01/2012",
    maxDate: moment().endOf("day"),
    //Có cái này thì range mới chạy được
    dateLimit: {
      days: 365
    },
    //hiển thị để chọn năm,  tháng
    showDropdowns: true,
    //Hiển thị cái cột  tuần ở bên cạnh
    showWeekNumbers: true,
    // timePicker: false,
    // timePickerIncrement: 1,
    // timePicker12Hour: true,
    //Luôn hiện cái bảng dù có chọn là 7 ngày, 1 tháng
    alwaysShowCalendars: true,
    ranges: {
      Today: [moment(), moment()],
      Yesterday: [moment().subtract(1, "days"), moment().subtract(1, "days")],
      "Last 7 Days": [moment().subtract(6, "days"), moment()],
      "Last 30 Days": [moment().subtract(29, "days"), moment()],
      "This Month": [moment().startOf("month"), moment().endOf("month")],
      "Last Month": [moment().subtract(1, "month").startOf("month"),moment().subtract(1, "month").endOf("month")]
    },
    // opens: 'left',
    buttonClasses: ["btn btn-default"],
    applyClass: "btn-small btn-primary",
    cancelClass: "btn-small btn-warning",
    format: "YYYY-MM-DD",
    separator: " to ",
    locale: {
      applyLabel: "Submit",
      cancelLabel: "Clear",
      fromLabel: "From",
      toLabel: "To",
      customRangeLabel: "Custom",
      daysOfWeek: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
      monthNames: [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
      ]
    }
  };
  //Đặt dữ liệu mặc định cho Chart
  $("#"+ calendar_id).daterangepicker(optionSet1, cb);
  $("#" + calendar_id + " span").html(moment().subtract(date_range, "days").format("YYYY-MM-DD") + " - " + moment().format("YYYY-MM-DD"));
}

function init_calendar_min_max(calendar_id,min_date,max_date, date_range=6) {
  var cb = function (start, end, label) {
    //Hiển thị cho khách hàng tháng/ngày/năm
    $("#"+ calendar_id +" span").html(start.format("YYYY-MM-DD") + " - " + end.format("YYYY-MM-DD"));
  };

  var format_min_date = moment(min_date).format('MM/DD/YYYY');
  var format_max_date = moment(max_date).format('MM/DD/YYYY');


  var optionSet1 = {
    dateFormat: "YYYY-MM-DD",
    startDate: moment().subtract(date_range, "days"),
    endDate: moment(),
    minDate: format_min_date,
    maxDate: format_max_date,
    //Có cái này thì range mới chạy được
    dateLimit: {
      days: 365
    },
    //hiển thị để chọn năm,  tháng
    showDropdowns: true,
    //Hiển thị cái cột  tuần ở bên cạnh
    showWeekNumbers: true,
    // timePicker: false,
    // timePickerIncrement: 1,
    // timePicker12Hour: true,
    //Luôn hiện cái bảng dù có chọn là 7 ngày, 1 tháng
    alwaysShowCalendars: true,
    ranges: {
      Today: [moment(), moment()],
      Yesterday: [moment().subtract(1, "days"), moment().subtract(1, "days")],
      "Last 7 Days": [moment().subtract(6, "days"), moment()],
      "Last 30 Days": [moment().subtract(29, "days"), moment()],
      "This Month": [moment().startOf("month"), moment().endOf("month")],
      "Last Month": [moment().subtract(1, "month").startOf("month"),moment().subtract(1, "month").endOf("month")]
    },
    // opens: 'left',
    buttonClasses: ["btn btn-default"],
    applyClass: "btn-small btn-primary",
    cancelClass: "btn-small btn-warning",
    format: "YYYY-MM-DD",
    separator: " to ",
    locale: {
      applyLabel: "Submit",
      cancelLabel: "Clear",
      fromLabel: "From",
      toLabel: "To",
      customRangeLabel: "Custom",
      daysOfWeek: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
      monthNames: [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
      ]
    }
  };
  //Đặt dữ liệu mặc định cho Chart
  $("#"+ calendar_id).daterangepicker(optionSet1, cb);
  $("#" + calendar_id + " span").html(min_date + " - " + max_date);
}

// Date Picker
function show_date_format(id_selector, value , disable=false){
  if (disable == false){
    var _html_input_start_date = '<div id="div-'+id_selector+'" class="input-group date" data-date-format="yyyy-mm-dd">' +
    '<input id="'+id_selector+'" class="form-control custom-datepicker-style" type="text" readonly value="'+value+'" />' +
    '<span class="input-group-addon"><i class="fa fa-calendar"></i></span>' +
    '</div>'
  }else{
    var _html_input_start_date = '<div id="div-'+id_selector+'" class="input-group date pointer-disable" data-date-format="yyyy-mm-dd">' +
    '<input id="'+id_selector+'" class="form-control custom-datepicker-style" type="text" readonly value="'+value+'" />' +
    '<span class="input-group-addon"><i class="fa fa-calendar"></i></span>' +
    '</div>'
  }

  $("#"+id_selector).replaceWith(_html_input_start_date)

  $("#div-"+id_selector).datepicker({
    autoclose: true,
    todayHighlight: true
  });
}