function activeButton() {
    let forecastButtons = document.querySelectorAll('.forecast-button-box-button');
    let activeButton;
    let tblId;
    let caption;
    let keysToIgnore = [];
    let urlBranch;
    forecastButtons.forEach(function (button) {
        if (button.classList.contains('active')) {
            activeButton = button;
        }
    });
    try {
            // activeButton = document.getElementById('fc-btn-1');
        index = activeButton.id.slice(-1);
    } catch (e) {
        console.log(e);
        // activeButton = document.getElementById('fc-btn-1');
        return null
    }
    // index = activeButton.id.slice(-1);
    if (index === '1') {
        tblId = 'daily-table';
        caption = 'Forecast by Day';
        keysToIgnore = ['day', 'timestamp_date', 'timestamp_time'];
        urlBranch = 'daily';
    } else if (index === '2') {
        tblId = 'hourly-table';
        caption = 'Forecast by Hour';
        keysToIgnore = ['day', 'time_epoch', 'date_time', 'timestamp_date', 'timestamp_time'];
        urlBranch = 'hourly';
    } else {
        tblId = 'astro-table';
        caption = 'Astronomy Data';
        keysToIgnore = ['day', 'time_epoch', 'date_time', 'timestamp_date', 'timestamp_time'];
        urlBranch = 'astro';
    }
    // console.log([tblId, caption, keysToIgnore]);
    return [tblId, caption, keysToIgnore, urlBranch];
    // buttons.forEach(function (button) {
    //     if (button.classList.contains('active')) {
    //         return button;
    //     }
    // });
}
// let forecastButtons = document.querySelectorAll('.forecast-button');
// let activeButton;
//
// forecastButtons.forEach(function (button) {
//     if (button.classList.contains('active')) {
//         activeButton = button;
//     }
// });
//
// console.log(activeButton);
// function filterByDay(obj) {
try {


    // let dayBtns = document.querySelectorAll('.day-btn');
    document.getElementById('day-btns').addEventListener('click', function (event) {
    // dayBtns.forEach(function (btn) {
    //     btn.addEventListener('click', function (event) {
        if (event.target.classList.contains('day-button-box-button')) {
            // console.log(event.target.value)
            let value = event.target.value.split('.');

            let context = activeButton();
            let tableId = context[0]
            let captionSnippet = context[1]
            let keysToIgnore = context[2]
            let urlBranch = context[3]
            const input_url = '/filter-data/' + value[0] + '/' + urlBranch + '/' + value[1];
            fetch(input_url)
                .then(response => response.json())
                .then(data => {
                    let jsonObj = JSON.parse(data);
                    const filteredData = jsonObj.filter(item => item.day === value[1]);
                    let table = document.getElementById(tableId);
                    let header = table.createTHead();
                    let caption;
                    // = document.getElementById('main-box-header').innerHTML;
                    caption = value[1] + ' ' + captionSnippet;
                    document.getElementById('main-box-header').innerHTML = caption;
                    while (table.firstChild) {
                        table.removeChild(table.firstChild);
                    }
                    hds = header.children.item(0);
                    // console.log([hds.children[0].textContent === 'Day', hds.textContent])
                    if (hds.children[0].textContent === 'Day') {
                        // console.log(hds.item(0));
                        hds.removeChild(hds.children[0]);
                    }
                    // console.log(header.children.item(0));
                    // keysToIgnore = ['day', 'time_epoch', 'date_time', 'timestamp_date', 'timestamp_time'];
                    table.appendChild(header);
                    for (let item of jsonObj) {
                        // console.log(item)
                        // delete item['day'];
                        // console.log(item)
                        let row = document.createElement('tr');
                        // let firstCol = document.createElement('td');
                        // let text = document.createTextNode(item.day);
                        // firstCol.appendChild(text);
                        // row.appendChild(firstCol);
                        for (let key in item) {
                            if (!keysToIgnore.includes(key)) {
                                let cell = document.createElement('td');
                                let text = document.createTextNode(item[key]);
                                cell.appendChild(text);
                                // console.log([cell, key])
                                row.appendChild(cell);
                            }
                            // console.log([key, row])
                        }
                        table.appendChild(row);
                    }
                });
        };
    });
// });
// });
} catch (e) {
    console.log('No forecast button is active.');

}
// document.getElementById('.day-button-box-button').addEventListener('click', function(event) {
//     if (event.target.classList.contains('day-btn')) {
//         var value = event.target.value.split('.')
//
//         const input_url = '/filter-data/' + value[0] + '/hour/' + value[1]
//         fetch(input_url)
//             .then(response => response.json())
//             .then(data => {
//                 let jsonObj = JSON.parse(data);
//                 const filteredData = jsonObj.filter(item => item.day === value[1]);
//                 // console.log(filteredData)
//                 let table = document.getElementById('forecast-hourly');
//                 let header = table.createTHead();
//                 // console.log(header)
//                 let caption = document.getElementById('hourly-header').innerHTML
//                 caption = value[1] + ' Forecast by Hour'
//                 console.log(caption)
//                 document.getElementById('hourly-header').innerHTML = caption
//                 while (table.firstChild) {
//                     table.removeChild(table.firstChild);
//                 }
//                 keysToIgnore = ['day', 'time_epoch', 'date_time', 'timestamp_date', 'timestamp_time']
//                 table.appendChild(header);
//                 for (let item of jsonObj) {
//                     let row = document.createElement('tr');
//
//                     for (let key in item) {
//                         // cell.textContent = item[key];
//                         if (!keysToIgnore.includes(key)) {
//                             let cell = document.createElement('td');
//                             let text = document.createTextNode(item[key]);
//                             cell.appendChild(text);
//                             // console.log(cell)
//                             row.appendChild(cell);
//                         }
//                     }
//                     table.appendChild(row);
//                 }
//
//             });
//     }
// });
