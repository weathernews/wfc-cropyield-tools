var chart;
var chart2;
var chart3;

function main(content,state,year){


    // 画像、テーブル初期化
    $('img').remove();
    $('table').remove();

    if (content == 'YIELD'){
	
	//make map
	const url = './plot_us.cgi?year='+year+'&content='+content;
	$(document).ready(function() {
	    var image = new Image();
	    image.src = url;
	    //image.src = "./png/crop_yield_"+year+".png";
	    image.width = 700;
	    $('#map').append(image);
	});
    };
    
    var $secondDropdown = $('#secondDropdown');

    if (content == 'PROG'){
	$('img').remove();

        $secondDropdown.empty();  // 既存のオプションをクリア
	
	
	
        var selects = ['EMERGED', 'BLOOMING', 'SETTING PODS','DROPPING LEAVS','HARVESTED'];
        $.each(selects, function(index, select) {
            $secondDropdown.append($('<option></option>').val(select).html(select));
        });
        $secondDropdown.show();
	const stage = $('select[name="stage"] option:selected').val();
	const url1 = './png/'+stage+'_usa.png';

	$(document).ready(function() {
	    var image = new Image();
	    image.src = url1;
	    image.width = 700;
	    $('#map').append(image);
	    console.log(url1);
	});
	//make map
	$('#secondDropdown').change(function() {
	    // 画像、テーブル初期化
	    $('img').remove();

	    var selectedOption = $(this).val();
	    const url1 = './png/'+selectedOption+'_usa.png';
	    
	    $(document).ready(function() {
		var image = new Image();
		image.src = url1;
		image.width = 700;
		$('#map').append(image);
	    });
	});
	
    }else {
	$secondDropdown.hide();
    };
    
    
    // table読み込み
    var tblfile = './tbl/state.tbl';
    
    $.ajax({
	url: tblfile,
        async : false,
	success: function(data){
	    tbl = data.split(/\r\n|\r|\n/);  // 改行コードで分割
	}
    });
    



    //<li><img src="image1.jpg" width="300" height="200" alt=""></li>
    //var image1 = new Image();
    //image1.src = url1;
	    //image1.width = 700;
	    //var image2 = new Image();
	    //image2.src = url2;
	    //image2.width = 700;
	    //$('#map').append(image1);
	    //$('#map').append(image2);
	    
    //});
    //};
    
    
    // サーバー上のCSVファイルのURL
    if (content == 'YIELD'){
	var csvUrl = './data/YIELD_output.csv';
	var csvUrl2 = './data/field_output.csv';
    }
    
    if ( content == 'PROG'){
	var csvUrl = './data/PROG.csv'

    }
    if ( content == 'WX'){

	let s = state.replace(" ","");
	var csvUrl = './data/'+state+'_WX_output.csv';
	var csvUrl2 = './data/'+state+'_WX_lrf.csv';
	var csvUrl3 = './data/'+state+'_WX_historical.csv';
	var csvUrl4 = './data/'+s+'_WX_mrf.csv';
	//var csvUrl4 = './data/'+state+'_WX_mrf.csv';
	var csvUrl5 = './data/'+state+'_latest.csv';


    }
    //
    
    console.log(csvUrl);
    $.ajax({
	url: csvUrl,
        async : false,
    }).done(function(data, textStatus, jqXHR){
        csv = $.csv.toArrays(data);
    });


    if (content == 'YIELD'){
	document.getElementById('point-table').style.display = 'block';
	document.getElementById('table-container').style.visibility = 'block';
	document.getElementById('wx-table').style.display = 'none';
	document.getElementById('myChart').style.display = 'none';
	document.getElementById('myChart2').style.display = 'none';

	$.ajax({
	    url: csvUrl2,
            async : false,
	}).done(function(data, textStatus, jqXHR){
            csv2 = $.csv.toArrays(data);
	});
	var headers = 	csv.shift();
	csv2.shift();
	console.log(headers);

	
	var c = 0;

	var ave = Array(6);

	ave[0]  = 'All State Average';
	csv.forEach(function(row){

	    csv[c][1] = csv[c][1] * csv2[c][1] / 1000;
	    csv[c][2] = csv[c][2] * csv2[c][2] / 1000;
	    csv[c][3] = csv[c][3] * csv2[c][3] / 1000;
	    csv[c][4] = csv[c][4] * csv2[c][4] / 1000;
	    csv[c][5] = csv[c][5] * csv2[c][5] / 1000;
	    csv[c][6] = csv[c][6] * csv2[c][6] / 1000;

	    c = c+1;
	});
	var average = function(arr) { //引数として渡された配列の平均値(average)を算出
	    var sum = 0;
	    for (var i = 0,len = arr.length; i < len; i++) {
		sum += arr[i];
	    }  
	    return sum / arr.length; //平均値を返す
	};
	var average_arr = function(arr) { //2次元配列の列ごとの平均値を求める
	    var arr_2d = [];
	    for (var i = 0, len_1 = arr[i].length; i < len_1; i++) {
		var arr_temp = []; 
		for (var j = 0, len_2 = arr.length; j < len_2; j++) {
		    arr_temp.push(arr[j][i]); //2次元配列の各列を1次元配列として抽出
        }
		arr_2d.push(average(arr_temp)); //2次元配列の各列ごとの平均値を抽出
	    }
	    return arr_2d; //平均値の配列を返す
	}
	
	var array1 = [];
	var array2 = [];
	var array3 = [];
	var array4 = [];
	var array5 = [];
	var array6 = [];
	
	csv.forEach(function(row){
	    var flag = tbl.indexOf(row[0]);
	    if (flag != -1){
		array1.push(row[1]);
		array2.push(row[2]);
		array3.push(row[3]);
		array4.push(row[4]);
		array5.push(row[5]);
		array6.push(row[6]);
	    }
	
	});
	
	ave[1] = average(array1);
	ave[2] = average(array2);
	ave[3] = average(array3);
	ave[4] = average(array4) ;
	ave[5] = average(array5);
	ave[6] = average(array6);
	

	csv.sort(function(a,b){return(b[6] - a[6]);});
	addpoint(csv,state);	

	addtable_crop(csv,headers,ave,tbl);
    };

    if (content == 'PROG'){


	document.getElementById('point-table').style.display = 'none';
	document.getElementById('table-container').style.visibility = 'block';
	document.getElementById('wx-table').style.display = 'none';
	document.getElementById('myChart').style.display = 'none';
	document.getElementById('myChart2').style.display = 'none';
	document.getElementById('myChart3').style.display = 'none';
	addtable_prog(csv);	
    };
    if (content == 'WX'){
	document.getElementById('point-table').style.display = 'none';
	document.getElementById('table-container').style.visibility = 'none';
	document.getElementById('wx-table').style.display = 'block';
	document.getElementById('myChart').style.display = 'block';
	document.getElementById('myChart2').style.display = 'block';
	document.getElementById('myChart3').style.display = 'block';
	$.ajax({
	    url: csvUrl3,
            async : false,
	}).done(function(data, textStatus, jqXHR){
            csv2 = $.csv.toArrays(data);
	});

	addtable_wx(csv,csv2);

	$.ajax({
	    url: csvUrl2,
            async : false,
	}).done(function(data, textStatus, jqXHR){
           csv_lrf = $.csv.toArrays(data);
	});

	$.ajax({
	    url: csvUrl4,
            async : false,
	}).done(function(data, textStatus, jqXHR){
            csv_mrf = $.csv.toArrays(data);
	});

	$.ajax({
	    url: csvUrl5,
            async : false,
	}).done(function(data, textStatus, jqXHR){
            csv_latest = $.csv.toArrays(data);
	});
	
	addchart_wx(csv_lrf);
	addchart_wx_mrf(csv_mrf);
	addchart_wx_latest(csv_latest);
    }
    
}





function addpoint(csv,state){
    var table = '<table border="1">';
    table += '<thead><tr>';


    var headers = ['State','2024 Crop Yield(k ton)','5year average(k ton)','2023 Crop Yeild(k ton)'];

    
    headers.forEach(function(header) {
        table += '<th>' + header + '</th>';
    });
    table += '</tr></thead>';
    // データをテーブルに追加
    table += '<tbody><tr>';
    
    var c = 0;
    csv.forEach(function(row) {
	if ( row[0] == state){
	    table +='<td>'+row[0]+'</td>';
	    row = row.map(Number);
	    table +='<td>'+Math.round(row[6]* 100)/100+'</td>';
	    const mean = ( row[1]+ row[2] + row[3] + row[4]  + row[5])/5;
	    table +='<td>'+Math.round(mean * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[5]  * 100)/100+'</td>';
	    table +='</tr>'
	}
	c = c + 1;
    });

    table += '</tbody>';            
    table += '</table>';
    
    // テーブルを表示
    document.getElementById('point-table').innerHTML = table;


}

function addtable_crop(csv,headers,ave,tbl){

    var table = '<table border="1">';
    table += '<thead><tr>';

    
    // ヘッダーをテーブルに追加
    data = csv.data;

    
    headers.forEach(function(header) {
        table += '<th>' + header + '</th>';
    });

    table += '<th>5 year Average</th>';
    table += '<th>Previous year ratio</th>';
    table += '<th>5 year average ratio</th>';
    
    table += '</tr></thead>';


    // データをテーブルに追加
    table += '<tbody><tr>';
    var c = 0;

    csv.forEach(function(row) {
	var flag = tbl.indexOf(row[0]);

	console.log(row[0],flag);
	if ( flag != -1) {
	    console.log(row);
	    table +='<td>'+row[0]+'</td>';
	    row = row.map(Number);
	    console.log(row);
	    table +='<td>'+Math.round(row[1] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[2] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[3] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[4] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[5] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[6] * 100)/100+'</td>';
	    const mean = ( row[1] + row[2] + row[3] + row[4] + row[5])/5;
	    table +='<td>'+Math.round(mean * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[6]/row[5] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[6]/mean * 100)/100 +'</td>';
	    table +='</tr>'
	}
    });
    
    table +='<td>'+ave[0]+'</td>';

    table +='<td>'+Math.round(ave[1] * 100)/100+'</td>';
    table +='<td>'+Math.round(ave[2] * 100)/100+'</td>';
    table +='<td>'+Math.round(ave[3] * 100)/100+'</td>';
    table +='<td>'+Math.round(ave[4] * 100)/100+'</td>';
    table +='<td>'+Math.round(ave[5] * 100)/100+'</td>';
    table +='<td>'+Math.round(ave[6] * 100)/100+'</td>';
    const mean = ( ave[1] + ave[2] + ave[3] + ave[4] + ave[5])/5;
    table +='<td>'+Math.round(mean * 100)/100+'</td>';
    table +='<td>'+Math.round(ave[6] / ave[5] * 100)/100+'</td>';
    table +='<td>'+Math.round(ave[6] /mean * 100)/100 +'</td>';
    table +='</tr>'
    table += '</tbody>';            
    table += '</table>';
    
    // テーブルを表示
    document.getElementById('table-container').innerHTML = table;
    
    
    
}

function addtable_prog(csv){

    var table = '<table border="1">';
    table += '<thead><tr>';

    
    // ヘッダーをテーブルに追加
    data = csv.data;
    console.log(csv[0]);    

    //var headers = ['State','EMERGED','BLOOMING','SETTING PODS','DROPPING LEAVES','HARVESTED'];
    var headers = ['州','発芽','開花','結実','落葉','収穫済み'];
    
    headers.forEach(function(header) {
        table += '<th>' + header + '</th>';
    });
    table += '</tr></thead>';


    
    // データをテーブルに追加
    table += '<tbody><tr>';
    var c = 0;
    csv.forEach(function(row) {
	if (row[0] != "State"){
	    table +='<td>'+row[0]+'</td>';
	    row = row.map(Number);
	    console.log(row);
	    table +='<td>'+Math.round(row[1] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[2] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[3] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[4] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[5] * 100)/100+'</td>';
	    table +='</tr>'	    
	}
	c = c+1;
    });

    table += '</tbody>';            
    table += '</table>';
    
    // テーブルを表示
    document.getElementById('table-container').innerHTML = table;

    
    
}

function addtable_wx(csv,csv2){

    console.log(csv2);
    console.log(csv);
    var table = '<table border="1">';
    table += '<thead><tr>';

    
    // ヘッダーをテーブルに追加
    data = csv.data;
    console.log(csv[0]);    


    var headers = ['Month',
		   '2024 月最大気温[℃]','2024 月最低気温[℃]','2024 月平均気温[℃]','2024 月降水量[mm]',
		   '2023 月最大気温[℃]','2023 月最低気温[℃]','2024 月平均気温[℃]','2023 月降水量[mm]',
		   '5年平均 月最高気温[℃]','5年平均 月最低気温[℃]','5年平均 月平均気温[℃]','5年平均 月降水量[mm]']

    
    headers.forEach(function(header) {
        table += '<th>' + header + '</th>';
    });
    table += '</tr></thead>';


    
    // データをテーブルに追加
    table += '<tbody><tr>';
    let c = 0;
    csv.forEach(function(row) {
	if (row[0] != 'Month'){
	    table +='<td>'+row[0]+'</td>';
	    row = row.map(Number);

	    table +='<td>'+Math.round(row[2] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[4] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[8] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[6] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[1] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[3] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[7] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[5] * 100)/100+'</td>';
	    table +='<td>'+Math.round(csv2[c+1][0] * 100)/100+'</td>';
	    table +='<td>'+Math.round(csv2[c+1][1] * 100)/100+'</td>';
	    table +='<td>'+Math.round(csv2[c+1][3] * 100)/100+'</td>';
	    table +='<td>'+Math.round(csv2[c+1][2] * 100)/100+'</td>';
	    
	    table +='</tr>'
	    c = c+1;
	}
    });
    
    table += '</tbody>';            
    table += '</table>';
    
    // テーブルを表示
    document.getElementById('wx-table').innerHTML = table;
}

function addissutime(){
    
    var y = new Date().getFullYear();
    var m = new Date().getMonth() + 1;
    var d = new Date().getDate() ;
    m = String(m).padStart(2, '0');
    d = String(d).padStart(2, '0');
    console.log(y,m,d)
    document.getElementById('issue time').innerHTML = 'Issue Time:'+y + "-" + m + "-" + d;

    

}

function addstate(state){
    

    document.getElementById('state').innerHTML = 'Selected : '+state;
    
    

}

function addchart_wx_latest(csv){
    const dates = [];
    const yield_hist = [];


    //見出し行削除
    csv.shift();//AREA1,date,State,TAVG,TAVG_NORYR,TMAX,TMAX_NORYR,TMIN,TMIN_NORYR,PRCP,PRCP_NORYR
    console.log(csv[1]);
    csv.forEach(function(row) {
	dates.push(row[1]);
	yield_hist.push(row[2]/1000)
	
    });

    var container = $('.canvas-container');
    var ctx3 = document.getElementById('myChart3').getContext('2d');
    if(chart3){
	chart3.destroy(); //すでにグラフが存在すれば消す
    }
    chart3 = new Chart(ctx3, {
	type: "bar",
	data: {
	    labels: dates,
	    datasets: [{
		label: "収穫量予測(変遷)",
		data: yield_hist,
		borderColor: "rgb(150, 100,100)",
		backgroundColor: "rgba(150, 100, 100, 0.8)",
		yAxisID: "y-axis-1",// 追加
		weight: 200,
	    }]
	},
	options: {
	    scales:{
		xAxes:[{
		    scaleLabel:{
			display:true,
			labelString:'Date',
			fontSize: 20,
		    }
		}],
		
		yAxes: [{
		    scaleLabel:{
			display:true,
			labelString:'Yield [k ton]',
			fontSize: 20
		    },
		    id: "y-axis-1",
		    type: "linear", 
		    position: "left",
		    ticks: {
			max: 10000,
			min: 0,
			stepSize: 2000,
		    }
		}],
	    },
	}
    });

    
    

}
function addchart_wx(csv){
    const dates = [];
    const tmax = [];
    const tmax_nrm = [];
    const tmax_prv = [];
    const tmin = [];
    const tmin_nrm = [];
    const tmin_prv = [];
    const prcp = [];
    const prcp_nrm = [];
    const prcp_prv = [];


    //見出し行削除
    csv.shift();//AREA1,date,State,TAVG,TAVG_NORYR,TMAX,TMAX_NORYR,TMIN,TMIN_NORYR,PRCP,PRCP_NORYR
    console.log(csv[0]);
    csv.forEach(function(row) {
	dates.push(row[2]);
	tmax.push(row[5]);
	tmax_nrm.push(row[6]);
	tmax_prv.push(row[13]);
	tmin.push(row[7]);
	tmin_nrm.push(row[8]);
	tmin_prv.push(row[14]);
	prcp.push(row[9]);
	prcp_nrm.push(row[10]);
	prcp_prv.push(row[15]);
    });
    var container = $('.canvas-container');
    var ctx = document.getElementById('myChart').getContext('2d');
    if(chart){
	chart.destroy(); //すでにグラフが存在すれば消す
    }
    chart = new Chart(ctx, {
	type: "bar",
	data: {
	    labels: dates,
	    datasets: [{
		label: "PRCP",
		data: prcp,
		borderColor: "rgb(100, 100,100)",
		backgroundColor: "rgba(100, 100, 100, 0.8)",
		yAxisID: "y-axis-1",// 追加
	    },{
		label: "PRCP_NORM",
		data: prcp_nrm,
		borderColor: "rgb(150, 150,150)",
		backgroundColor: "rgba(200, 200, 200, 0.4)",
		yAxisID: "y-axis-1",// 追加
	    },{
		label: "PRCP_PRV",
		data: prcp_prv,
		borderColor: "rgb(225, 225,225)",
		backgroundColor: "rgba(200, 200, 200, 0.4)",
		yAxisID: "y-axis-1",// 追加

	    },{
		label: "TMAX",
		data: tmax,
		type: "line",
		fill: false,
		borderColor: "rgb(235, 162,162)",
		backgroundColor: "rgba(235, 162, 162, 0.4)",
		yAxisID: "y-axis-2",// 追加
	    },{
		label: "TMAX_NORM",
		data: tmax_nrm,
		type: "line",
		fill: false,
		borderColor: "rgba(235, 162,162,0.2)",
		backgroundColor: "rgba(235, 162, 162, 0.2)",
		yAxisID: "y-axis-2",// 追加
	    },{
		label: "TMAX_PRV",
		data: tmax_prv,
		type: "line",
		fill: false,
		borderDash: [5, 5],
		borderColor: "rgba(235, 162,162,0.2)",
		backgroundColor: "rgba(235, 162, 162, 0.2)",
		yAxisID: "y-axis-2",// 追加
	    },{
		label: "TMIN",
		data: tmin,
		type: "line",
		fill: false,
		borderColor: "rgb(162, 162,235)",
		backgroundColor: "rgba(162, 162, 235, 0.4)",
		yAxisID: "y-axis-2",// 追加
	    },{
		label: "TMIN_NORM",
		data: tmin_nrm,
		type: "line",
		fill: false,
		borderColor: "rgba(162, 162, 235, 0.2)",
		backgroundColor: "rgba(162, 162, 235, 0.2)",
		yAxisID: "y-axis-2",// 追加
	    },{
		label: "TMIN_PRV",
		data: tmin_prv,
		type: "line",
		fill: false,
		borderDash: [5, 5],
		borderColor: "rgba(162, 162, 235, 0.2)",
		backgroundColor: "rgba(162, 162, 235, 0.2)",
		yAxisID: "y-axis-2",// 追加
				
	    }]
	},
	options: {
	    scales:{
		xAxes:[{
		    scaleLabel:{
			display:true,
			labelString:'Date',
			fontSize: 20,
		    }
		}],
		
		yAxes: [{
		    scaleLabel:{
			display:true,
			labelString:'Precipitation[mm]',
			fontSize: 20
		    },
		    
		    id: "y-axis-1",
		    type: "linear", 
		    position: "left",
		    ticks: {
			max: 100,
			min: 0,
			stepSize: 25
		    },
		}, {
		    scaleLabel:{
			display:true,
			labelString:'Temperature(℃)',
			fontSize: 20
		    },
		    id: "y-axis-2",
		    type: "linear", 
		    position: "right",
		    ticks: {
			max: 40,
			min: 0,
			stepSize: 10
		    },
		    gridLines: {
			drawOnChartArea: false, 
			   },
		}],
	    }
	}
    });

    
    //chart.canvas.parentNode.style.height = '128px';
    //chart.canvas.parentNode.style.width = '128px';
    
}

function addchart_wx_mrf(csv){
    const dates = [];
    const tmax = [];
    const tmin = [];
    const prcp = [];

    //const dates,tmax,tmin,prcp = [],[],[],[];
    //見出し行削除
    csv.shift();//AREA1,date,State,TAVG,TAVG_NORYR,TMAX,TMAX_NORYR,TMIN,TMIN_NORYR,PRCP,PRCP_NORYR
    //datetime,TMAX,TMIN,PRCP,State
    console.log(csv[0]);
    csv.forEach(function(row) {
	dates.push(row[0]);
	tmax.push(row[1]);
	tmin.push(row[2]);
	prcp.push(row[3]);
    });
    var container = $('.canvas-container');
    var ctx2 = document.getElementById('myChart2').getContext('2d');
    if(chart2){
	chart2.destroy(); //すでにグラフが存在すれば消す
    }
    chart2 = new Chart(ctx2, {
	type: "bar",
	data: {
	    labels: dates,
	    datasets: [{
		label: "PRCP",
		data: prcp,
		borderColor: "rgb(125, 125,125)",
		backgroundColor: "rgba(125, 125, 125, 0.4)",
		yAxisID: "y-axis-1",// 追加
	    
	    },{
		label: "TMAX",
		data: tmax,
		type: "line",
		fill: false,
		borderColor: "rgb(235, 162,162)",
		backgroundColor: "rgba(235, 162, 162, 0.4)",
		yAxisID: "y-axis-2",// 追加
	    },{
		label: "TMIN",
		data: tmin,
		type: "line",
		fill: false,
		borderColor: "rgb(162, 162,235)",
		backgroundColor: "rgba(162, 162, 235, 0.4)",
		yAxisID: "y-axis-2",// 追加
		
	    }]
	},
	options: {
	    scales:{
		xAxes:[{
		    scaleLabel:{
			display:true,
			labelString:'Date',
			fontSize: 20,
		    }
		}],
		
		yAxes: [{
		    scaleLabel:{
			display:true,
			labelString:'Precipitation[mm]',
			fontSize: 20
		    },
		    
		    id: "y-axis-1",
		    type: "linear", 
		    position: "left",
		    ticks: {
			max: 100,
			min: 0,
			stepSize: 25
		    },
		}, {
		    scaleLabel:{
			display:true,
			labelString:'Temperature(℃)',
			fontSize: 20
		    },
		    id: "y-axis-2",
		    type: "linear", 
		    position: "right",
		    ticks: {
			max: 40,
			min: 0,
			stepSize: 10
		    },
		    gridLines: {
			drawOnChartArea: false, 
			   },
		}],
	    }
	}
    });
}

	       

function init(){    
    $('img').remove();
    addissutime();







    // URLのクエリ文字列を取得                                                                                        
    const queryString = window.location.search;

    // URLSearchParamsオブジェクトを作成してクエリ文字列を解析                                                        
    const params = new URLSearchParams(queryString);

    // 特定のパラメータの値を取得                                                                                     
    // lon,lat = 画面中央の位置                                                                                       
    // zoomlevel = zoomlevel                                                                                         
    let content = $('select[name="content"] option:selected').val();
    let state = $('select[name="state"] option:selected').val();
    let year = $('select[name="year"] option:selected').val();


    // 特定のパラメータの値を取得                                                                                     
    // lon,lat = 画面中央の位置                                                                                      
    let yearval = params.get('year');
    let stateval = params.get('state');
    let contentval = params.get('content');
    if ( yearval){
	year = yearval;
	
    }
    
    if (stateval){
	state = stateval
	
    }
    
    if (contentval){
	content = contentval;
	console.log(content);
    }
    
    addstate(state);    
    
    
    main(content,state,year);
    
    $('select[name="content"]').change(function() {
	const content = $('select[name="content"] option:selected').val();
	const state = $('select[name="state"] option:selected').val();
	const year = $('select[name="year"] option:selected').val();
	main(content,state,year);
	
    });
    
    $('select[name="state"]').change(function() {
	const content = $('select[name="content"] option:selected').val();
	const state = $('select[name="state"] option:selected').val();
	const year = $('select[name="year"] option:selected').val();
	main(content,state,year);
	
    });

    
    $('select[name="year"]').change(function() {

	const content = $('select[name="content"] option:selected').val();
	const state = $('select[name="state"] option:selected').val();
	const year = $('select[name="year"] option:selected').val();

	main(content,state,year);
	
    });


				       
}
