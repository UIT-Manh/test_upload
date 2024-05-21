$(document).ready(function () {
    const temp = {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: "Delta temperature plot",
                backgroundColor: 'rgba(255, 69, 0, 0.5)',
                borderColor: 'rgb(255, 69, 0)',
                data: [],
                fill: true,
                lineTension: 0.5
            }],
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Delta temperature plot'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Khw'
                    }
                }]
            }
        }
    };

    

    const tempContext = document.getElementById('tempChart').getContext('2d');


    const tempChart = new Chart(tempContext, temp);


    const source = new EventSource("/chart-data");

    source.onmessage = function (event) {
        const data = JSON.parse(event.data);
        temp.data.labels.push(data.temp_time);
        temp.data.datasets[0].data.push(data.temp_value);
        tempChart.update();
    }
    
});
