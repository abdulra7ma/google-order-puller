$(document).ready(async function () {
    await addTotal("total-value");
});

anychart.onDocumentReady(async function () {
    // create a data set on our data
    var dataSet = anychart.data.set(await getData());

    // map data for the first series,
    // take x from the zero column and value from the first column
    var SeriesData = dataSet.mapAs({
        x: 0,
        value: 1
    });

    // create a line chart
    var chart = anychart.line();

    // turn on the line chart animation
    chart.animation(true);

    // configure the chart title text settings
    chart.title("Orders over price chart");

    // set the y axis title
    chart.yAxis().title("Max price reached");

    // turn on the crosshair
    chart.crosshair().enabled(true).yLabel(false).yStroke(null);

    // create the first series with the mapped data
    var Series = chart.line(SeriesData);
    Series.name("price").stroke("3 #f49595").tooltip();

    // turn the legend on
    chart.legend().enabled(true);

    // set the container id for the line chart
    chart.container("container");

    // draw the line chart
    chart.draw();
});

async function getData() {
    var points = [];
    var data = await getOrders();
    var items = data.data;

    items.forEach(function (item) {
        points.push([item.date, item.usd_price]);
    });

    return points;
};

async function getTotal() {
    var data = await getOrders();
    const total = data.total;
    return total;
};

async function getOrders() {
    let response = await fetch("http://127.0.0.1:8000/api/order/");
    let data = await response.json();

    return data;
};

async function addTotal(variable) {
    var s = document.getElementById(variable);
    s.innerHTML = await getTotal();

};
