const ctx = document.getElementById('myChart');

let jsonData = Result;
let mychart;

createChart(jsonData, 'bar');

function setChartType(chartType) {
    mychart.destroy();
    createChart(jsonData, chartType)
}

function createChart(data, type) {
    mychart = new Chart(ctx, {
        type: type,
        data: {
            labels: data.map(row => row.schedule),
            datasets: [{
                label: '% of Marks',
                data: data.map(row => row.percentage),
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            maintainAspectRatio: false
        }
    });

}