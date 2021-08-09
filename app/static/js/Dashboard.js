/*I  advice that you find a a way to populate this from the csv file
Enjoy*/

function parseData(createGraph) {
    Papa.parse("http://127.0.0.1:5000/static/StudentReport.csv", {
        download: true,
        complete: function(results) {
            createGraph(results.data);
        }
    })
}



function createGraph(data) {

    var subject = [];
    var score1 = [];
    var score2 = [];

    for (i = 0; i <= 5; i++) {
        subject.push(data[i + 1][0]);
        score1.push(data[i][2]);
        score2.push(data[i][3])
    }


    var chart = c3.generate({
        bindto: '#chartDiv',
        padding: {
            right: 7,
            bottom: 15
        },
        data: {
            columns: [
                score1,
                score2
            ]
        },
        axis: {
            x: {
                type: 'category',
                categories: subject,
                tick: {
                    fit: true
                },
                padding: {
                    bottom: 5000
                }
            },
            y: {
                max: 100
            }
        },
        zoom: {
            enabled: true
        },
    });
    setTimeout(function() {
        chart.unload({
            columns: [
                ['Score 1', 94, 68, 45, 80, 91]
            ]
        });
    }, 1500);
    setTimeout(function() {
        chart.unload({
            columns: [
                ['Score 2', 84, 58, 95, 70, 91]
            ]
        });
    }, 1500);
    setTimeout(function() {
        chart.load({
            columns: [
                score1
            ]
        });
    }, 1500);
    setTimeout(function() {
        chart.load({
            columns: [
                score2
            ]
        })
    }, 2000);
    setTimeout(function() {
        chart.resize({ height: 190 })
    }, 1000);
}
parseData(createGraph)