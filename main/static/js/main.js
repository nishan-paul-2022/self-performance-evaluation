let information = {
    "event": {
        "2003": "",
        "2004": "class-1",
        "2005": "class-2",
        "2006": "class-3",
        "2007": "class-4",
        "2008": "class-5 / psc",
        "2009": "class-6",
        "2010": "class-7",
        "2011": "class-8 / jsc",
        "2012": "class-9",
        "2013": "class-10 / ssc",
        "2014": "clg-ad / clg-1st",
        "2015": "clg-2nd / clg-3rd",
        "2016": "hsc / uni-ad",
        "2017": "bsc-1st / bsc-2nd",
        "2018": "bsc-3rd / bsc-4th",
        "2019": "bsc-5th / bsc-6th",
        "2020": "lockdown",
        "2021": "bsc-7th-a / bsc-8th-a",
        "2022": "bsc-7th-b / bsc-8th-b"
    },

    "v1stStart"   : "2004",
    "v2ndLast"    : "2021",
    "v3rdCurrent" : "2022",

    "undergraduate_options" : [
        "undergraduate", "result", "exam", "short",
        "l1t1", "l1t2", "l2t1", "l2t2", "l3t1", "l3t2", "l4t1", "l4t2",
        "dept", "nondept", "theo", "sess", "theo_dept", "sess_dept", "theo_nondept", "sess_nondept", "sess_only"
    ]
}

let chart = '';


function create_options_a() {
    let xhr = new XMLHttpRequest();
    xhr.open('get', 'main', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let element = document.getElementById("id01");
            element.innerHTML = xhr.responseText;
        }
    }
    xhr.send();
}


function create_options_b() {
    let xhr = new XMLHttpRequest();
    xhr.open('get', 'main', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let element = document.getElementById('id05');
            let df = document.createDocumentFragment();

            for(let options of information['undergraduate_options']) {
                let node = document.createElement('option');
                let node_child = document.createTextNode(options)
                node.value = options;
                node.appendChild(node_child);
                df.appendChild(node);
            }
            element.appendChild(df);
        }
    }
    xhr.send();
}


function create_options_c() {
    let xhr = new XMLHttpRequest();
    xhr.open('get', 'main', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let element = document.getElementById('id06');
            let df = document.createDocumentFragment();
            let temp1 = parseInt(information['v1stStart']);
            let temp2 = parseInt(information['v3rdCurrent']);

            for(let year = temp1; year <= temp2; year++) {
                let node = document.createElement('option');
                node.value = String(year);
                node.appendChild(document.createTextNode(node.value));
                df.appendChild(node);
            }
            element.appendChild(df);
        }
    }
    xhr.send();
}


function get_desired_template(value) {
    let filemapping = ['main_undergraduate_summary', 'main_analysis'];
    let filename = filemapping.indexOf(value) > -1? value : 'main_undergraduate_details?options='+value;

    let xhr = new XMLHttpRequest();
    xhr.open('get', filename, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let element = document.getElementById("id03");
            element.innerHTML = xhr.responseText;
        }
    }
    xhr.send();
}


function imonlyhuman_evaluate(imonlyhuman_summary) {
    let element = document.getElementById('id03');
    element.innerHTML = '';
    element.setAttribute("class", "id07");

    for(let key in imonlyhuman_summary) {
        let value = imonlyhuman_summary[key];
        let node1 = document.createElement("div"), node2 = document.createElement("div");
        node1.setAttribute("id", "id08");
        node2.setAttribute("id", "id09");
        node2.style.width = value + '%';
        node2.innerHTML = key;
        node1.appendChild(node2);
        element.appendChild(node1);
    }
}


function toggleDataSeries(e) {
    e.dataSeries.visible = !(typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible);
    chart.render();
}


function data_labeling_a(key, value, indexLabel) {
    let data = {};
    data.label = key;
    data.y = parseInt(value);
    data.indexLabel = indexLabel;
    data.indexLabelPlacement = 'outside';
    data.indexLabelOrientation = 'vertical';
    data.indexLabelFontSize = 18;
    return data;
}


function data_labeling_b(key, value) {
    let datapos = {}, dataneg = {};
    datapos.y = parseInt(value);
    datapos.indexLabel = key;
    datapos.indexLabelPlacement = 'outside';
    datapos.indexLabelFontSize = 12;
    dataneg.y = 100 - datapos.y;
    return [datapos, dataneg];
}


function graph_rendering_a(text, title, data) {
    chart = new CanvasJS.Chart("id03", {
        animationEnabled: true,
        exportEnabled: true,
        title: {text: text},
        axisX: {title: title},
        axisY: {title: "grade"},
        toolTip: {shared: true},
        legend: {cursor:"pointer", itemclick: toggleDataSeries},
        data: data
    });
    chart.render();
}


function graph_rendering_b(text, title, pos, neg) {
    chart = new CanvasJS.Chart("id03", {
        animationEnabled: true,
        title: {text: text},
        axisX: {title: title},
        axisY: {interval: 5, suffix: "%"},
        toolTip: {shared: true},
        legend: {cursor:"pointer"},
        data: [
            {type: "stackedBar100",	showInLegend: true, name: "positive", dataPoints: pos},
            {type: "stackedBar100", showInLegend: true, name: "negative", dataPoints: neg}
        ]
    });
    chart.render();
}


function graph_rendering_days(statistics_days) {
    let text = "from " + information['v2ndLast'] + " - " + information['v3rdCurrent'];
    let title = "day";
    let type = "splineArea";
    let xy = {};

    for(let year in statistics_days) {
        let datelist = statistics_days[year];
        xy[year] = [];

        for(let date in datelist) {
            let value = datelist[date];
            let node = data_labeling_a(date, value[0], value[1]);
            xy[year].push(node);
        }
    }

    let data = [];
    for(let year in xy) {
        let node = {type: type, name: year, visible: true, showInLegend: true, dataPoints: xy[year]};
        data.push(node);
    }
    graph_rendering_a(text, title, data);
}


function graph_rendering_years(statistics_years) {
    let text = "from " + information['v1stStart'] + " - " + information['v3rdCurrent'];
    let title = "year";
    let type = "column";
    let name = "psych eval";
    let xy = [];
    let event = information['event'];

    for(let year in statistics_years) {
        let node = data_labeling_a(year, statistics_years[year], event[year]);
        xy.push(node);
    }

    let data = [{type: type, name: name, showInLegend: true, dataPoints: xy}];
    graph_rendering_a(text, title, data);
}


function graph_rendering_years_details(statistics_years_details, year) {
    let text = "Year " + String(year);
    let title = "parameter";
    let eventlist = statistics_years_details[year];
    let datapos = [], dataneg = [];

    for(let event in eventlist) {
        let value = eventlist[event][1];
        let node = data_labeling_b(event, value);
        datapos.push(node[0]);
        dataneg.push(node[1]);
    }
    graph_rendering_b(text, title, datapos, dataneg);
}


create_options_a();
create_options_b();
create_options_c();