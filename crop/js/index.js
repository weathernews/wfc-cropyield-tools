var chart;
var chart2;
var chart3;

function main(content,state,year){

    var $firstDropdown = $('#firstDropdown');
    var $secondDropdown = $('#secondDropdown');
    $firstDropdown.empty();
    $secondDropdown.empty();

    // table読み込み
    var tblfile = './tbl/state.tbl';
    $.ajax({
	url: tblfile,
        async : false,
    }).done(function(data, textStatus, jqXHR){
        tbl = $.csv.toArrays(data);
    });

    var newtbl = new Object;
    for (i = 0; tbl[i]; i++) {
	var k = tbl[i][0];
	var v = tbl[i][1];
	newtbl[k] = v;
    }

    var names = [];
    tbl.forEach(function(row){
	names.push(row[0]);
    });
    
    // 画像、テーブル初期化
    $('img').remove();
    $('table').remove();

    if (content == 'YIELD'){
	$('img').remove();
	$('table').remove();
	var csvUrl = './data/YIELD_output.csv';
	var csvUrl2 = './data/field_output.csv';
	$secondDropdown.hide();
	$('#state_select').show();
	$('#year_select').show();
	$('#area').show();
	$('#downloadCsv').show();
	document.getElementById('wx-table').style.display = 'none';
	document.getElementById('myChart').style.display = 'none';
	document.getElementById('myChart2').style.display = 'none';
	document.getElementById('myChart3').style.display = 'none';
	//make map
	
	let selects = {
	    '収量':'YIELD',
	    '単収':'per',
	}
	
        $.each(selects, function(index, select) {
	    
            $firstDropdown.append($('<option></option>').val(select).text(index));
	});
	
        $firstDropdown.show();

	let stage = $('select[name="stage_crop"] option:selected').val();
	let url = './plot_us.cgi?year='+year+'&content='+stage;
	
	$(document).ready(function() {
	    $('img').remove();
	    

	    var image = new Image();
	    image.src = url;
	    image.width = 700;
	    $('#map').append(image);

	});
	// Set csv & make tbl
	readcsv(csvUrl,csvUrl2,tbl,newtbl,stage,state);
	

	$('#firstDropdown').change(function() {
	    $('img').remove();
	    $('table').remove();

	    // 選択されたstageを取得
	    var stage = $(this).val();
	    
	    const url = './plot_us.cgi?year='+year+'&content='+stage;
	    $(document).ready(function() {
		$('img').remove();
		var image = new Image();
		image.src = url;
		image.width = 700;
		$('#map').append(image);
	    });
	    
	    // Set csv & make tbl

	    readcsv(csvUrl,csvUrl2,tbl,newtbl,stage,state);

	    
	});
	
    }
    if (content == 'PROG'){

	$firstDropdown.hide();	
	
	
	$('#state_select').hide()
	$('#year_select').hide()
	$('#area').hide()
	$('#downloadCsv').show();



	var csvUrl = './data/PROG.csv';
	
	
	$.ajax({
	    url: csvUrl,
            async : false,
	}).done(function(data, textStatus, jqXHR){
            csv = $.csv.toArrays(data);
	});
		
	
	document.getElementById('point-table').style.display = 'none';
	document.getElementById('table-container').style.visibility = 'block';
	document.getElementById('wx-table').style.display = 'none';
	document.getElementById('myChart').style.display = 'none';
	document.getElementById('myChart2').style.display = 'none';
	document.getElementById('myChart3').style.display = 'none';
	
	let c = 0;
    
	var ave = Array(6);
	var sum = Array(6);
	ave[0]  = '州平均';
	sum[0]  = '州合計';	
	
	let array1 = [];
	let array2 = [];
	let array3 = [];
	let array4 = [];
	let array5 = [];
	let array6 = [];
	var headers = 	csv.shift();

	csv.forEach(function(row){	    
	    row = row.map(Number);
	    array1.push(row[1]);
	    array2.push(row[2]);
	    array3.push(row[3]);
	    array4.push(row[4]);
	    array5.push(row[5]);
	    array6.push(row[6]);
	    
	    
	});
	let arrays = [array1,array2,array3,array4,array5,array6];
	
	c = 1;
	arrays.forEach(function(array){
	    let [s,a] = average(array);
	    ave[c] = a;
	    sum[c] = s;
	    c = c+1;
	});
	

	
	var selects = {
	    '発芽':'EMERGED',
	    '開花':'BLOOMING',
	    '結実':'SETTING PODS',
	    '落葉':'DROPPING LEAVS',
	    '収穫済み':'HARVESTED',

	}
	let stage = "HARVESTED";
        $.each(selects, function(index, select) {

	    let selected = '';
	    if (select == stage){
		selected = "selected"
	    }
            $secondDropdown.append($('<option '+selected+'></option>').val(select).text(index));
	    
	    
	});

	
	$secondDropdown.show();

	$('img').remove();

	let url1 = './png/'+stage+'_usa.png';
	
	$(document).ready(function() {
	    $('img').remove();
	    var image = new Image();
	    image.src = url1;
	    image.width = 700;
	    $('#map').append(image);

	});


	//make map
	$('#secondDropdown').change(function() {
	    $('img').remove();

	    var selected = $(this).val();
	    console.log(selected);
	    const url1 = './png/'+selected+'_usa.png';
	    
	    $(document).ready(function() {
		    
		$('img').remove();
		var image = new Image();
		image.src = url1;
		image.width = 700;
		$('#map').append(image);
	    });
	    
	});
	
	addtable_prog(csv,ave,names,newtbl);	
    };




    if ( content == 'WX'){
	$firstDropdown.hide();	
        $secondDropdown.hide();	
	$('#state_select').show()
	$('#year_select').hide()
	$('#area').hide()
	$('#downloadCsv').hide();
	let s = state.replace(" ","");
	var csvUrl = './data/'+state+'_WX_output.csv';
	var csvUrl2 = './data/'+state+'_WX_lrf.csv';
	var csvUrl3 = './data/'+state+'_WX_historical.csv';
	var csvUrl4 = './data/'+s+'_WX_mrf.csv';
	var csvUrl5 = './data/'+state+'_latest.csv';

	document.getElementById('point-table').style.display = 'none';
	document.getElementById('table-container').style.visibility = 'none';
	document.getElementById('wx-table').style.display = 'block';
	document.getElementById('myChart').style.display = 'block';
	document.getElementById('myChart2').style.display = 'block';
	document.getElementById('myChart3').style.display = 'block';

	$.ajax({
	    url: csvUrl,
            async : false,
	}).done(function(data, textStatus, jqXHR){
            csv = $.csv.toArrays(data);
	});
	
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
				
function readcsv(csvUrl,csvUrl2,tbl,newtbl,stage,state){
    document.getElementById('point-table').style.display = 'block';
    document.getElementById('table-container').style.visibility = 'block';
    document.getElementById('wx-table').style.display = 'none';
    document.getElementById('myChart').style.display = 'none';
    document.getElementById('myChart2').style.display = 'none';
	    
    $.ajax({
	url: csvUrl,
	async : false,
    }).done(function(data, textStatus, jqXHR){
	csv = $.csv.toArrays(data);
    });
    
    $.ajax({
	url: csvUrl2,
	async : false,
    }).done(function(data, textStatus, jqXHR){
	csv2 = $.csv.toArrays(data);
    });
    
    //var headers = 	csv.shift();

    csv.shift();
    csv2.shift();
    
    let c = 0;
    
    var ave = Array(6);
    var sum = Array(6);

    ave[0]  = '州平均';
    sum[0]  = '州合計';	
    
	    
    if ( stage == "YIELD"){
	csv.forEach(function(row){
	    
	    csv[c][1] = csv[c][1] * csv2[c][1] / 100000;
	    csv[c][2] = csv[c][2] * csv2[c][2] / 100000;
	    csv[c][3] = csv[c][3] * csv2[c][3] / 100000;
	    csv[c][4] = csv[c][4] * csv2[c][4] / 100000;
	    csv[c][5] = csv[c][5] * csv2[c][5] / 100000;
	    csv[c][6] = csv[c][6] * csv2[c][6] / 100000;
		    
	    c = c+1;
	});
    }
    
    var array1 = [];
    var array2 = [];
    var array3 = [];
    var array4 = [];
    var array5 = [];
    var array6 = [];
    
    var names = [];
    tbl.forEach(function(row){
	    names.push(row[0]);
    });
    
    csv.forEach(function(row){
	
	var flag = names.includes(row[0]);
	
	if (flag){
	    array1.push(row[1]);
	    array2.push(row[2]);
	    array3.push(row[3]);
	    array4.push(row[4]);
	    array5.push(row[5]);
	    array6.push(row[6]);
	}
	c = c + 1;
    });

    let arrays = [array1,array2,array3,array4,array5,array6];
    console.log(arrays)
    c = 1;
	arrays.forEach(function(array){
	    let [s,a] = average(array);
	    ave[c] = a;
	    sum[c] = s;
	    c = c+1;
	});

	

    csv.sort(function(a,b){return(b[6] - a[6]);});
    console.log(state);
    
    if ( stage  == "YIELD"){
	headers = ['州','2024 収量予測(0.1M Bushels)','5年平均収量(0.1M Bushels)','2023年収量(0.1M Bushels)'];
	addpoint(csv,state,newtbl,headers);
    }else{
	headers = ['州','2024 収量予測(Bushels/Acre)','5年平均収量(Bushels/Acre)','2023年収量(Bushels/Acre)'];
	addpoint(csv,state,newtbl,headers);
    }
    
    headers = ['州','2019年','2020年','2021年','2022年','2023年','2024年(予測)'];
    addtable_crop(csv,headers,ave,sum,names,newtbl);
    


}

function tableToCSV() {
    var csv = [];
    $('#table-container tr').each(function() {
        var row = [];
        $(this).find('th, td').each(function() {
            var text = $(this).text();
            row.push('"' + text.replace(/"/g, '""') + '"');
        });
        csv.push(row.join(','));
    });
    return csv.join('\n');
}
    
    

function downloadCSV(csv, filename) {
    var blob = new Blob([csv], { type: 'text/csv' });
    var link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}


function average(arr){
    
    var sum = 0;
    for (var i = 0,len = arr.length; i < len; i++) {
	sum += parseFloat(arr[i]);
    }

    return [sum, sum / arr.length]; //平均値を返す
};



function addpoint(csv,state,newtbl,headers){
    var table = '<table border="1">';
    table += '<thead><tr>';
    //    console.log(csv);

    //var headers = ['州','2024 収量予測(0.1M Bushel)','5年平均収量(0.1M Bushel)','2023年収量(0.1M Bushel)'];

    
    headers.forEach(function(header) {
        table += '<th>' + header + '</th>';
    });
    table += '</tr></thead>';

    // データをテーブルに追加
    table += '<tbody><tr>';
    
    var c = 0;
    csv.forEach(function(row) {
	console.log(row[0],state);
	if ( row[0] == state){
	    table +='<td>'+newtbl[state]+'</td>';
	    //table +='<td>'+row[0]+'</td>';
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

function addtable_crop(csv,headers,ave,sum,names,newtbl){
    console.log(sum,ave);
    var table = '<table border="1">';
    table += '<thead><tr>';

    
    // ヘッダーをテーブルに追加
    data = csv.data;

    
    headers.forEach(function(header) {
        table += '<th>' + header + '</th>';
    });
    //[,'5年平均値','前年比','5年平均比'];
    table += '<th>5年平均値</th>';
    table += '<th>前年比</th>';
    table += '<th>5年平均比</th>';
    
    table += '</tr></thead>';


    // データをテーブルに追加
    table += '<tbody><tr>';
    var c = 0;
    console.log(newtbl);
    csv.forEach(function(row) {
	var flag = names.includes(row[0]);
	
	

	if (flag) {
	    table +='<td>'+newtbl[row[0]]+'</td>';
	    //table +='<td>'+row[0]+'</td>';
	    row = row.map(Number);

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

    table +='<td>'+sum[0]+'</td>';

    table +='<td>'+Math.round(sum[1] * 100)/100+'</td>';
    table +='<td>'+Math.round(sum[2] * 100)/100+'</td>';
    table +='<td>'+Math.round(sum[3] * 100)/100+'</td>';
    table +='<td>'+Math.round(sum[4] * 100)/100+'</td>';
    table +='<td>'+Math.round(sum[5] * 100)/100+'</td>';
    table +='<td>'+Math.round(sum[6] * 100)/100+'</td>';
    let mean = ( sum[1] + sum[2] + sum[3] + sum[4] + sum[5])/5;
    table +='<td>'+Math.round(mean * 100)/100+'</td>';
    table +='<td>'+Math.round(sum[6] / sum[5] * 100)/100+'</td>';
    table +='<td>'+Math.round(sum[6] /mean * 100)/100 +'</td>';
    table +='</tr>'
    
    table +='<td>'+ave[0]+'</td>';

    table +='<td>'+Math.round(ave[1] * 100)/100+'</td>';
    table +='<td>'+Math.round(ave[2] * 100)/100+'</td>';
    table +='<td>'+Math.round(ave[3] * 100)/100+'</td>';
    table +='<td>'+Math.round(ave[4] * 100)/100+'</td>';
    table +='<td>'+Math.round(ave[5] * 100)/100+'</td>';
    table +='<td>'+Math.round(ave[6] * 100)/100+'</td>';
    mean = ( ave[1] + ave[2] + ave[3] + ave[4] + ave[5])/5;
    table +='<td>'+Math.round(mean * 100)/100+'</td>';
    table +='<td>'+Math.round(ave[6] / ave[5] * 100)/100+'</td>';
    table +='<td>'+Math.round(ave[6] /mean * 100)/100 +'</td>';
    table +='</tr>'
    
    table += '</tbody>';            
    table += '</table>';
    
    // テーブルを表示
    document.getElementById('table-container').innerHTML = table;
    
    
    
}

function addtable_prog(csv,ave,names,newtbl){

    var table = '<table border="1">';
    table += '<thead><tr>';

    
    // ヘッダーをテーブルに追加
    data = csv.data;


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
	    table +='<td>'+newtbl[row[0]]+'</td>';
	    //table +='<td>'+row[0]+'</td>';
	    row = row.map(Number);

	    table +='<td>'+Math.round(row[1] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[2] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[3] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[4] * 100)/100+'</td>';
	    table +='<td>'+Math.round(row[5] * 100)/100+'</td>';
	    table +='</tr>'	    
	}
	c = c+1;
    });

    table +='<td>'+ave[0]+'</td>';
    table +='<td>'+Math.round(ave[1] * 100)/100+'</td>';
    table +='<td>'+Math.round(ave[2] * 100)/100+'</td>';
    table +='<td>'+Math.round(ave[3] * 100)/100+'</td>';
    table +='<td>'+Math.round(ave[4] * 100)/100+'</td>';
    table +='<td>'+Math.round(ave[5] * 100)/100+'</td>';
    table +='</tr>'
    table += '</tbody>';            
    table += '</table>';
    
    // テーブルを表示
    document.getElementById('table-container').innerHTML = table;

    
    
}

function addtable_wx(csv,csv2){


    var table = '<table border="1">';
    table += '<thead><tr>';

    
    // ヘッダーをテーブルに追加
    data = csv.data;



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
    var date = +y + "-" + m + "-" + d;
    document.getElementById('issue time').innerHTML = '発行日:'+y + "/" + m + "/" + d;
    return date
    

}

function addstate(state){
    

    document.getElementById('state').innerHTML = 'Selected : '+state;
    
    

}

function addchart_wx_latest(csv){
    const dates = [];
    const yield_hist = [];


    //見出し行削除
    csv.shift();//AREA1,date,State,TAVG,TAVG_NORYR,TMAX,TMAX_NORYR,TMIN,TMIN_NORYR,PRCP,PRCP_NORYR

    csv.forEach(function(row) {
	dates.push(row[1]);
	yield_hist.push(row[2]/100000)
	
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
			labelString:'日付',
			fontSize: 20,
		    }
		}],


		yAxes: [{
		    scaleLabel:{
			display:true,
			labelString:'収量[Bushels]',
			fontSize: 20
		    },
		    id: "y-axis-1",
		    type: "linear", 
		    position: "left",
		    ticks: {
			min:0,
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
		label: "降水量",
		data: prcp,
		borderColor: "rgb(100, 100,100)",
		backgroundColor: "rgba(100, 100, 100, 0.8)",
		yAxisID: "y-axis-1",// 追加
	    },{
		label: "平年降水量",
		data: prcp_nrm,
		borderColor: "rgb(150, 150,150)",
		backgroundColor: "rgba(200, 200, 200, 0.4)",
		yAxisID: "y-axis-1",// 追加
	    },{
		label: "前年降水量",
		data: prcp_prv,
		borderColor: "rgb(225, 225,225)",
		backgroundColor: "rgba(200, 200, 200, 0.4)",
		yAxisID: "y-axis-1",// 追加

	    },{
		label: "最高気温",
		data: tmax,
		type: "line",
		fill: false,
		borderColor: "rgb(235, 162,162)",
		backgroundColor: "rgba(235, 162, 162, 0.4)",
		yAxisID: "y-axis-2",// 追加
	    },{
		label: "平年最高気温",
		data: tmax_nrm,
		type: "line",
		fill: false,
		borderColor: "rgba(235, 162,162,0.2)",
		backgroundColor: "rgba(235, 162, 162, 0.2)",
		yAxisID: "y-axis-2",// 追加
	    },{
		label: "前年最高気温",
		data: tmax_prv,
		type: "line",
		fill: false,
		borderDash: [5, 5],
		borderColor: "rgba(235, 162,162,0.2)",
		backgroundColor: "rgba(235, 162, 162, 0.2)",
		yAxisID: "y-axis-2",// 追加
	    },{
		label: "最低気温",
		data: tmin,
		type: "line",
		fill: false,
		borderColor: "rgb(162, 162,235)",
		backgroundColor: "rgba(162, 162, 235, 0.4)",
		yAxisID: "y-axis-2",// 追加
	    },{
		label: "平年最低気温",
		data: tmin_nrm,
		type: "line",
		fill: false,
		borderColor: "rgba(162, 162, 235, 0.2)",
		backgroundColor: "rgba(162, 162, 235, 0.2)",
		yAxisID: "y-axis-2",// 追加
	    },{
		label: "前年最低気温",
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
			labelString:'日付',
			fontSize: 20,
		    }
		}],
		
		yAxes: [{
		    scaleLabel:{
			display:true,
			labelString:'降水量[mm]',
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
			labelString:'気温(℃)',
			fontSize: 20
		    },
		    id: "y-axis-2",
		    type: "linear", 
		    position: "right",
		    ticks: {
			max: 40,
			min: -10,
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


    //見出し行削除
    csv.shift();


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
		label: "降水量[mm]",
		data: prcp,
		borderColor: "rgb(125, 125,125)",
		backgroundColor: "rgba(125, 125, 125, 0.4)",
		yAxisID: "y-axis-1",// 追加
	    
	    },{
		label: "最高気温[℃]",
		data: tmax,
		type: "line",
		fill: false,
		borderColor: "rgb(235, 162,162)",
		backgroundColor: "rgba(235, 162, 162, 0.4)",
		yAxisID: "y-axis-2",// 追加
	    },{
		label: "最低気温[℃]",
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
			labelString:'日付',
			fontSize: 20,
		    }
		}],
		
		yAxes: [{
		    scaleLabel:{
			display:true,
			labelString:'降水量[mm]',
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
			labelString:'気温(℃)',
			fontSize: 20
		    },
		    id: "y-axis-2",
		    type: "linear", 
		    position: "right",
		    ticks: {
			max: 40,
			min: -10,
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
    let datestr = addissutime();







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

    }
    
    //addstate(state);    
    
    
    main(content,state,year);
    
    $('select[name="content"]').change(function() {
	content = $('select[name="content"] option:selected').val();
	console.log(content);
	state = $('select[name="state"] option:selected').val();
	year = $('select[name="year"] option:selected').val();

	main(content,state,year);
	
    });
    
    $('select[name="state"]').change(function() {
	content = $('select[name="content"] option:selected').val();
	state = $('select[name="state"] option:selected').val();
	console.log(state);
	year = $('select[name="year"] option:selected').val();
	//addstate(state);
	main(content,state,year);
	
    });

    
    $('select[name="year"]').change(function() {

	content = $('select[name="content"] option:selected').val();
	state = $('select[name="state"] option:selected').val();
	year = $('select[name="year"] option:selected').val();

	main(content,state,year);
	
    });

    
    $('#downloadCsv').on('click', function() {
	content = $('select[name="content"] option:selected').val();
	let name = "crop_yield";
	if ( content == "PROG"){
	    name = "crop_progress";
	}
        let csv = tableToCSV();
        let filename = datestr+'_'+name+'_data.csv';
        downloadCSV(csv, filename);
    });
				       
}
