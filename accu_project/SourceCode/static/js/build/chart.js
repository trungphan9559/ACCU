// ========================================================================
// Draw chart line or bar
// ========================================================================
function draw_chart_v2(chart_box_id, label_chart, list_label, list_data, type_chart, m_option = {},functio_){
  var div_html_chart = '<canvas id="chart_id" height = 50% ></canvas>';
  var m_backgroundColor = "#000000"; 

  // Tim gia tri cao nhat
  var max_val = 0;
  for(i = 0; i<list_data.length; i++) {
    if(list_data[i] > max_val) {
      max_val = list_data[i];
    }
  }

  var step_size = 0;
  if(max_val < 5) {
    step_size = 5;
  } else {
    step_size = max_val / 5;
  }

  step_size = step_size - (step_size % 5);
  
  if(Object.keys(m_option).length ==0 ){
    m_option = {   
      tooltips: {
        mode: 'index',
        intersect: false
      },
      responsive: true,
      scales: {
        xAxes: [{
          
          stacked: false,
        }],
        yAxes: [{
          stacked: false,
          scaleLabel: {
            display: true,
          },
          ticks: {
            display: true,
            beginAtZero: true,
            min: 0,
            stepSize: step_size,
        },
        }]
      }
    }
  }

  m_option['onClick'] = function(e) {
                                      var xLabel = this.scales['x-axis-0'].getValueForPixel(e.x);
                                      var label__ = this.scales['x-axis-0'].ticks[xLabel]
                                      if(functio_ != undefined){
                                        functio_(xLabel);
                                      }
                                      //alert("clicked x-axis area: " + xLabel);
                                    }
  if (type_chart == "bar"){
    m_backgroundColor =  "#3e95cd"
  }
  else{
    m_backgroundColor = "#f9fcfd"
  }  

  $('#' + chart_box_id).html(div_html_chart);
  var ctx = document.getElementById('chart_id').getContext('2d');
  var chart_id = new Chart(ctx, {
    type: type_chart, // line,bar...
    data: {
        labels: list_label ,
        datasets: [{
            label: label_chart,
            data: list_data,
            borderColor: "#3e95cd",  
            backgroundColor : m_backgroundColor
            
        }]
      },
      options: m_option
    });   
}

function draw_chart(chart_box_id, label_chart, list_label, list_data, type_chart, m_option = {},functio_){
  var div_html_chart = '<canvas id="chart_id" height = 50% ></canvas>';
  var m_backgroundColor = "#000000"; 
  
  if(Object.keys(m_option).length ==0 ){
    m_option = {   
      tooltips: {
        mode: 'index',
        intersect: false
      },
      responsive: true,
      scales: {
        xAxes: [{
          
          stacked: false,
        }],
        yAxes: [{
          stacked: false,
          scaleLabel: {
            display: true,
          },
          ticks: {
            display: true,
            beginAtZero: true,
            min: 0,
            max: 100,
        },
        }]
      }
    }
  }

  m_option['onClick'] = function(e) {
                                      var xLabel = this.scales['x-axis-0'].getValueForPixel(e.x);
                                      var label__ = this.scales['x-axis-0'].ticks[xLabel]
                                      if(functio_ != undefined){
                                        functio_(xLabel);
                                      }
                                      //alert("clicked x-axis area: " + xLabel);
                                    }
  if (type_chart == "bar"){
    m_backgroundColor =  "#3e95cd"
  }
  else{
    m_backgroundColor = "#f9fcfd"
  }  

  $('#' + chart_box_id).html(div_html_chart);
  var ctx = document.getElementById('chart_id').getContext('2d');
  var chart_id = new Chart(ctx, {
    type: type_chart, // line,bar...
    data: {
        labels: list_label ,
        datasets: [{
            label: label_chart,
            data: list_data,
            borderColor: "#3e95cd",  
            backgroundColor : m_backgroundColor
            
        }]
      },
      options: m_option
    });   
}

function draw_line_chart(e,div_html_chart,chart_id,data_chart_json,m_option){

  //Nếu data có 1 ngày thì vẽ căn giữa, nếu nhiều ngày thì vẽ bình thường

  if (data_chart_json.list_data_chart.length == 1){
    m_option.scales.xAxes[0].offset  = true;
  }
  
  $(e).html(div_html_chart);
  var ctx = document.getElementById(chart_id).getContext('2d');
  new Chart(ctx, {
    type: 'line', 
    data: {
        labels: data_chart_json.list_label_chart ,
        datasets: [{
            label: data_chart_json.label_chart,
            data: data_chart_json.list_data_chart,
            borderWidth: 2,
            pointRadius: data_chart_json.pointRadius != undefined ?  data_chart_json.pointRadius : 0, // độ to của point
            borderColor: 'rgba(116, 185, 255,1)',
            backgroundColor: 'rgba(116, 185, 255,0.3)',
            pointBackgroundColor: 'rgba(116, 185, 255,1)',
            fill: 'start',          
        }]
      },
      options: m_option
    });
}

// ========================================================================
// Draw Multiple chart line and bar
// ========================================================================

function draw_multiple_chart(e,div_html_chart,chart_id,m_option,data_chart_1_json,data_chart_2_json){ 

  if(m_option == ""){ //defaul option for line and bar
    m_option = {
      responsive: true,
      //hiển thị label
      tooltips: 
      {
        callbacks: 
          {
      
          label: function(tooltipItems, data) {
            if (data.datasets[0].code[tooltipItems.index]==-1){
              data.datasets[0].code[tooltipItems.index] = "Out Of Range";
            };
            var label = data.datasets[0].label + " : " + data.datasets[0].code[tooltipItems.index] + ' | ' || '' ;
            label +=  data.datasets[1].label + " : " + data.datasets[1].data[tooltipItems.index];

            return label
          }
          },
      },
      // option vẽ hai cột giá trị y  
      scales: {
        
        yAxes: 
        [
        {
          id: 'y-axis-1',
          type: 'linear',
          display: true,
          position: 'left',
          labels: 
          {
            show:false
          },
          ticks:
          {
            beginAtZero: true,
          }
        }, 
        {
          id: 'y-axis-2',
          type: 'linear',
          display: true,
          labels: 
          {
            show:false
          },
          // hiển thị đường kẻ
          gridLines: 
          {
            display: false
          },
          position: 'right',
          // thanh đo min max giá trị           
          ticks: 
          {
            max : 30,
            min: 0,
            reverse: true  
          },
        },
           
      ]
            }
      }
  }

  $(e).html(div_html_chart);
  var ctx = document.getElementById(chart_id).getContext('2d');
  new Chart(ctx, {
    type: data_chart_1_json.type_chart, // line,bar...
    data: {
        labels: data_chart_2_json.list_label_chart ,
        
        //datasets: m_dataset
        datasets: 
        [
          
          {
          lineTension: 0,
          label: data_chart_2_json.label_chart,
          yAxisID : 'y-axis-2',
          code : data_chart_2_json.list_label_rank_keyword,
          data: data_chart_2_json.list_value_chart,
          //borderColor: color_chart_line,
          borderColor: data_chart_2_json.color_chart,
          backgroundColor: data_chart_2_json.color_chart,
          pointBorderColor: data_chart_2_json.color_chart,
          pointBackgroundColor: data_chart_2_json.color_chart,
          pointHoverBackgroundColor: data_chart_2_json.color_chart,
          pointHoverBorderColor: data_chart_2_json.color_chart,
          fill: false,
          
          //
          // Changes this dataset to become a line
          type: data_chart_2_json.type_chart
          },
          {
            
            data: data_chart_1_json.list_value_chart,
            yAxisID : 'y-axis-1',
            label:data_chart_1_json.label_chart,
            //backgroundColor: color_chart_bar,
            backgroundColor: data_chart_1_json.color_chart,
            borderColor: data_chart_1_json.color_chart,
            hoverBackgroundColor: data_chart_1_json.color_chart,
            hoverBorderColor: data_chart_1_json.color_chart,
            fill: false,
            type: data_chart_1_json.type_chart,
            
            } 
      ]
      },
      options: m_option
    });
    /*
    datasets: [{
      label: array,
      data: array,   
  },]*/

}


function draw_chart_line_by_limit_yAxes(div_id, is_reverse, chart = {}, m_option = {}){

  // var chart = {
  //             'list_label' : [],
  //             'list_data' : [],
  //             'label_chart' : '',
  //   };
  // var m_option = {
  //                 'max_value' : int,
  //                 'min_value' : int,
  //       };
  var div_html_chart = '<canvas id="chart_id" height = "50%" "width=100%" ></canvas>';
  var list_data_reduce = []

  //Các giá trị mặc định cho min max
  m_option.min_value = m_option.min_value != undefined ? m_option.min_value : 0;
  m_option.max_value = m_option.max_value != undefined ? m_option.max_value : 10000;

  //Lấy list data đã được giới hạn bởi min max:
  for(i = 0; i < chart.list_data.length; i++)
  {
    if(chart.list_data[i] < m_option.min_value){
      list_data_reduce.push(m_option.min_value)
    }
    else if(chart.list_data[i] > m_option.max_value){
      list_data_reduce.push(m_option.max_value)
    }
    else{
      list_data_reduce.push(chart.list_data[i])
    }
  }

  //vẽ biểu đồ chính giữa khi có 1 1 điểm
   
  var  offset_option  = false;
  if (chart.list_data.length == 1){
    offset_option  = true;
  }

  //Data đễ vẽ chart:
  var roadsChartData = {
                      labels: chart.list_label,
                      datasets: [{
                            code: chart.list_data,
                            label: chart.label_chart != undefined ? chart.label_chart : "Title Chart",
                            data: list_data_reduce,
                            fill: false,
                            borderColor: "#3e95cd", 
                        }]
  }

  $('#' + div_id).html(div_html_chart);
  var ctx = document.getElementById('chart_id').getContext('2d');
  var chart_id = new Chart(ctx, {
      type: 'line',
      data: roadsChartData,
      options: {
        tooltips: {
            callbacks: {
              label: function(tooltipItems, data) {
                  if(data.datasets[0].code[tooltipItems.index] >= 100){
                    return chart.label_chart +":  Out of range"
                  }
                  else{
                    return chart.label_chart +":  "+ data.datasets[0].code[tooltipItems.index] 
                  }                              
              }  
            }  
        },
        responsive: true,
        elements: {
                  line: {
                      tension: 0 // disables bezier curves
                        },
                },
     
        scales: {
          xAxes : [{
            offset : offset_option,
          }],
          yAxes: [{    
            ticks: {
              min: m_option.min_value,
              max: m_option.max_value,
              reverse : is_reverse != undefined ? is_reverse : false,
            }
          }]
        },
      }
    });
}

function show_stack_bar(list_items){
  // list_item = [
  //   {
  //     'name' : 'Organic',
  //     'value' : 12
  //     'background-color' : '#fff'
  //   }
  // ]
  var total = 0
  for(var i=0; i < list_items.length;i++){
    total += parseInt(list_items[i]['value'])
  }

  var html = '<div style="height:16px; width: 100%; float:left; display: inline-block;">'

  for(var i=0; i < list_items.length;i++){
    var name = list_items[i]['name']
    var percent = parseInt(list_items[i]['value']) / total * 100
    html += `<div style="background-color: ${list_items[i]['background-color']} ; height: 100%; width: ${percent}%; float:left; display: inline-block;">`
    html += '</div>'
  }
  html += '</div>'
  
  return html
}