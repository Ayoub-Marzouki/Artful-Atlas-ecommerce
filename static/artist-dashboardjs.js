document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('myChart');
    const revenue = document.getElementById('revenue').innerHTML;
    const current_month = document.getElementById('month').innerHTML;
    let monthly_revenue = [0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0, 0];

    switch (parseInt(current_month)) {
        case 1:
            monthly_revenue[0] = revenue;
            break;
        case 2:
            monthly_revenue[1] = revenue;
            break;
        case 3:
            monthly_revenue[2] = revenue;
            break;
        case 4:
            monthly_revenue[3] = revenue;
            break;
        case 5:
            monthly_revenue[4] = revenue;
            break;
        case 6:
            monthly_revenue[5] = revenue;
            break;
        case 7:
            monthly_revenue[6] = revenue;
            break;
        case 8:
            monthly_revenue[7] = revenue;
            break;
        case 9:
            monthly_revenue[8] = revenue;
            break;
        case 10:
            monthly_revenue[9] = revenue;
            break;
        case 11:
            monthly_revenue[10] = revenue;
            break;
        case 12:
            monthly_revenue[11] = revenue;
            break;
        default:
            break;
    }

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            datasets: [{
                label: 'Money Earned so far',
                data: monthly_revenue,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });    
});
