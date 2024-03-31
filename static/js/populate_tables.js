
function decodeHtmlEntities(encodedJson) {
    var textarea = document.createElement('textarea');
    textarea.innerHTML = encodedJson;
    return textarea.value;
}

function populateTable(jsonstring, tbl_id) {
    var data = {}
    if (typeof jsonstring === 'string') {
        let decodedJson = decodeHtmlEntities(jsonstring);
        data = JSON.parse(decodedJson);
    }
    else {
        data = jsonstring;
    }

    keysToIgnore = ['time_epoch', 'date_time', 'timestamp_date', 'timestamp_time'];
    // Select the table
    var table = document.getElementById(tbl_id);
    table.innerHTML = '';

    var header = table.createTHead();
    var cols = Object.keys(data[0]);
    cols.forEach(function(col) {
        if (!keysToIgnore.includes(col)) {
            let splitted = col.split('_');
            let newCol;
            if (splitted.length > 1) {
                splitted.forEach(function (word) {
                    splitted[splitted.indexOf(word)] = word.charAt(0).toUpperCase() + word.slice(1);
                })
                newCol = splitted.join(' ');
            } else {
                if (col === "uv") {
                    newCol = col.toUpperCase()
                } else {
                    newCol = col.charAt(0).toUpperCase() + col.slice(1);
                }
            }
            cols[cols.indexOf(col)] = newCol;
        }
    });
    let headerRow = document.createElement('thead');
    let firstRow = document.createElement('tr');
    // headerRow.classList.add('tr', 'sticky-table-header')
    cols.forEach(function(col) {
        if (!keysToIgnore.includes(col)) {
            let th = document.createElement('th');

            th.textContent = col;
            // th.classList.add('th', 'sticky-table-header');
            let hdrcls = col.replace(/_/g, '-').toLowerCase();
            hdrcls = hdrcls.replace(/ /g, '-');
            th.classList.add('th', 'sticky-table-header', `cb-${hdrcls}`);
            // th.classList.add('th');
            firstRow.appendChild(th);
        }
    });
    // firstRow.classList.add('t', 'sticky-table-header');
    header.appendChild(firstRow);
    header.classList.add('th', 'sticky-table-header');
    // Loop over the rows in the data
    for (var i = 0; i < data.length; i++) {
        // Create a new table row
        var row = document.createElement('tr');
        row.classList.add('tr')
        // Loop over the columns in the row
        for (var key in data[i]) {
            if (data[i].hasOwnProperty(key)) {
                if (!keysToIgnore.includes(key)) {
                    var cell = document.createElement('td');
                    cell.classList.add('td')
                    console.log(key)
                    cell.classList.add('cb-' + key.replace(/_/g, '-'));
                    // cell.classList.add('table-cb');
                    if (key === 'date_time') {
                        // let cell = document.createElement('td');
                        // cell.classList.add('td')
                        // cell.classList.add('cb-' + key);
                        let date = new Date(data[i][key] * 1000);
                        cell.textContent = date.toLocaleString();
                        // row.appendChild(cell);
                    } else {
                        // Create a new table data element and set its text content
                        // var cell = document.createElement('td');
                        // cell.classList.add('td')
                        // cell.classList.add('cb-' + key);
                        cell.textContent = data[i][key];
                        formatCellColor(cell, key);
                        // Append the table data element to the row
                        // row.appendChild(cell);
                    }
                    row.appendChild(cell);
                }
            }
        }
        // Append the row to the table
        table.appendChild(row);
    }
    // var elem = document.querySelector('.sticky-table-header');
    console.log(window.getComputedStyle(firstRow).getPropertyValue('position'));
}

function formatCellColor(cell, column) {
    if (column === 'temperature') {
        if (cell.textContent < 10) {
            cell.style.backgroundColor = '#00008B';
            cell.style.color = 'white';
        } else if (cell.textContent < 20) {
            cell.style.backgroundColor = '#0058fc';
        } else if (cell.textContent < 30) {
            cell.style.backgroundColor = '#0095ff';
        } else if (cell.textContent < 40) {
            cell.style.backgroundColor = '#00f8d3';
        } else if (cell.textContent < 50) {
            cell.style.backgroundColor = '#00f804';
        } else if (cell.textContent < 60) {
            cell.style.backgroundColor = '#b2f800';
        } else if (cell.textContent < 70) {
            cell.style.backgroundColor = '#f8d700';
            cell.style.color = 'white';
        } else if (cell.textContent < 80) {
            cell.style.backgroundColor = '#f88d00';
            cell.style.color = 'white';
        } else if (cell.textContent < 90) {
            cell.style.backgroundColor = '#f84a00';
        } else {
            cell.style.backgroundColor = '#FF0000';
            cell.style.color = 'white';
        }
    }
    else if (column === 'is_day') {
        if (cell.textContent === '1') {
            cell.style.backgroundColor = '#eeff00';
            cell.textContent = 'Yes';
        } else {
            cell.style.backgroundColor = '#171717';
            cell.style.color = 'white';
            cell.textContent = 'No';
        }
    }
    // else if (column === 'condition') {
    //     if (cell.textContent === 'Clear ') {
    //         cell.style.backgroundColor = '#fff984';
    //     } else if (cell.textContent === 'Partly Cloudy ' || cell.textContent === 'Partly cloudy ' || cell.textContent === 'Partly cloudy') {
    //         cell.style.backgroundColor = 'orange';
    //     } else if (cell.textContent === 'Cloudy ') {
    //         cell.style.backgroundColor = '#8d8d8d';
    //     } else if (cell.textContent === 'Overcast ') {
    //         cell.style.backgroundColor = '#313131';
    //         cell.style.color = 'white';
    //     } else if (cell.textContent === 'Light sleet') {
    //         cell.style.backgroundColor = '#67d2ff';
    //         cell.style.color = 'black';
    //     } else if (cell.textContent === 'Light rain shower' || cell.textContent === 'Patchy light drizzle') {
    //         cell.style.backgroundColor = 'blue';
    //         cell.style.color = 'white';
    //     } else if (cell.textContent === 'Patchy rain nearby') {
    //         cell.style.backgroundColor = '#3b52cb';
    //         cell.style.color = 'white';
    //     } else if (cell.textContent === 'Patchy snow possible ') {
    //         cell.style.backgroundColor = 'white';
    //         cell.style.color = 'black';
    //     } else if (cell.textContent === 'Patchy sleet possible ') {
    //         cell.style.backgroundColor = 'white';
    //         cell.style.color = 'black';
    //     } else if (cell.textContent === 'Patchy freezing drizzle possible ') {
    //         cell.style.backgroundColor = 'white';
    //         cell.style.color = 'black';
    //     } else if (cell.textContent === 'Thundery outbreaks possible ') {
    //         cell.style.backgroundColor = 'red';
    //         cell.style.color = 'white';
    //     } else if (cell.textContent === 'Blowing snow ') {
    //         cell.style.backgroundColor = 'white';
    //         cell.style.color = 'black';
    //     } else if (cell.textContent === 'Blizzard ') {
    //         cell.style.backgroundColor = 'white';
    //         cell.style.color = 'black';
    //     } else if (cell.textContent === 'Fog ') {
    //         cell.style.backgroundColor = 'blue';
    //         cell.style.color = 'white';
    //     } else if (cell.textContent === 'Freezing fog ') {
    //         cell.style.backgroundColor = 'blue';
    //         cell.style.color = 'white';
    //     } else if (cell.textContent === 'Patchy light drizzle') {
    //         cell.style.backgroundColor = 'blue';
    //         cell.style.color = 'white';
    //     } else if (cell.textContent === 'Light drizzle ') {
    //         cell.style.backgroundColor = 'blue';
    //         cell.style.color = 'white';
    //     } else if (cell.textContent === 'Freezing drizzle ') {
    //         cell.style.backgroundColor = 'blue';
    //         cell.style.color = 'white';
    //     }
    // }
    else if (column === 'wind_mph') {
        if (cell.textContent < 5) {
            cell.style.backgroundColor = '#d0fcd0';
        } else if (cell.textContent < 10) {
            cell.style.backgroundColor = '#a0fca0';
        } else if (cell.textContent < 15) {
            cell.style.backgroundColor = '#70fcbd';
        } else if (cell.textContent < 20) {
            cell.style.backgroundColor = '#40e0fc';
        } else {
            cell.style.backgroundColor = '#0076fc';
        }
    }
    // else if (column === 'wind_degree') {
    //     if (cell.textContent < 45) {
    //         cell.style.backgroundColor = 'green';
    //     } else if (cell.textContent < 90) {
    //         cell.style.backgroundColor = 'yellow';
    //     } else if (cell.textContent < 135) {
    //         cell.style.backgroundColor = 'orange';
    //     } else if (cell.textContent < 180) {
    //         cell.style.backgroundColor = 'red';
    //     } else {
    //         cell.style.backgroundColor = 'purple';
    //     }
    // }

// NOT YET FORMATTED
    else if (column === 'pressure') {
        if (cell.textContent < 1000) {
            cell.style.backgroundColor = 'green';
        } else if (cell.textContent < 1010) {
            cell.style.backgroundColor = 'yellow';
        } else if (cell.textContent < 1020) {
            cell.style.backgroundColor = 'orange';
        } else if (cell.textContent < 1030) {
            cell.style.backgroundColor = 'red';
        } else {
            cell.style.backgroundColor = 'purple';
        }
    }
    else if (column === 'precipitation') {
        if (cell.textContent < 0.1) {
            cell.style.backgroundColor = 'green';
        } else if (cell.textContent < 0.25) {
            cell.style.backgroundColor = 'yellow';
        } else if (cell.textContent < 0.5) {
            cell.style.backgroundColor = 'orange';
        } else if (cell.textContent < 1) {
            cell.style.backgroundColor = 'red';
        } else {
            cell.style.backgroundColor = 'purple';
        }
    }
    else if (column === 'snow') {
        if (cell.textContent < 0.1) {
            cell.style.backgroundColor = 'green';
        } else if (cell.textContent < 0.25) {
            cell.style.backgroundColor = 'yellow';
        } else if (cell.textContent < 0.5) {
            cell.style.backgroundColor = 'orange';
        } else if (cell.textContent < 1) {
            cell.style.backgroundColor = 'red';
        } else {
            cell.style.backgroundColor = 'purple';
        }
    }
    else if (column === 'humidity') {
        if (cell.textContent < 30) {
            cell.style.backgroundColor = 'green';
        } else if (cell.textContent < 50) {
            cell.style.backgroundColor = 'yellow';
        } else if (cell.textContent < 70) {
            cell.style.backgroundColor = 'orange';
        } else if (cell.textContent < 90) {
            cell.style.backgroundColor = 'red';
        } else {
            cell.style.backgroundColor = 'purple';
        }
    }
    else if (column === 'cloud') {
        if (cell.textContent < 25) {
            cell.style.backgroundColor = 'green';
        } else if (cell.textContent < 50) {
            cell.style.backgroundColor = 'yellow';
        } else if (cell.textContent < 75) {
            cell.style.backgroundColor = 'orange';
        } else if (cell.textContent < 100) {
            cell.style.backgroundColor = 'red';
        } else {
            cell.style.backgroundColor = 'purple';
        }
    }
    else if (column === 'real_feel') {
        if (cell.textContent < 32) {
            cell.style.backgroundColor = 'green';
        } else if (cell.textContent < 50) {
            cell.style.backgroundColor = 'yellow';
        } else if (cell.textContent < 68) {
            cell.style.backgroundColor = 'orange';
        } else if (cell.textContent < 86) {
            cell.style.backgroundColor = 'red';
        } else {
            cell.style.backgroundColor = 'purple';
        }
    }
    else if (column === 'windchill') {
        if (cell.textContent < 32) {
            cell.style.backgroundColor = 'blue';
            cell.style.color = 'white';
        } else if (cell.textContent < 50) {
            cell.style.backgroundColor = 'green';
        } else if (cell.textContent < 68) {
            cell.style.backgroundColor = 'yellow';
        } else if (cell.textContent < 86) {
            cell.style.backgroundColor = 'orange';
        } else {
            cell.style.backgroundColor = 'red';
        }
    }
    else if (column === 'heat_index') {
        if (cell.textContent < 32) {
            cell.style.backgroundColor = 'blue';
            cell.style.color = 'white';
        } else if (cell.textContent < 50) {
            cell.style.backgroundColor = 'green';
        } else if (cell.textContent < 68) {
            cell.style.backgroundColor = 'yellow';
        } else if (cell.textContent < 86) {
            cell.style.backgroundColor = 'orange';
        } else {
            cell.style.backgroundColor = 'red';
        }
    }
    else if (column === 'dewpoint') {
        if (cell.textContent < 32) {
            cell.style.backgroundColor = 'blue';
            cell.style.color = 'white';
        } else if (cell.textContent < 50) {
            cell.style.backgroundColor = 'green';
        } else if (cell.textContent < 68) {
            cell.style.backgroundColor = 'yellow';
        } else if (cell.textContent < 86) {
            cell.style.backgroundColor = 'orange';
        } else {
            cell.style.backgroundColor = 'red';
        }
    }
    else if (column === 'will_it_rain') {
        if (cell.textContent === '0') {
            cell.style.backgroundColor = 'green';
        } else {
            cell.style.backgroundColor = 'red';
        }
    }
    else if (column === 'chance_of_rain') {
        if (cell.textContent < 25) {
            cell.style.backgroundColor = 'green';
        } else if (cell.textContent < 50) {
            cell.style.backgroundColor = 'yellow';
        } else if (cell.textContent < 75) {
            cell.style.backgroundColor = 'orange';
        } else if (cell.textContent < 100) {
            cell.style.backgroundColor = 'red';
        } else {
            cell.style.backgroundColor = 'purple';
        }
    }
    else if (column === 'will_it_snow') {
        if (cell.textContent === '0') {
            cell.style.backgroundColor = 'green';
        } else {
            cell.style.backgroundColor = 'red';
        }
    }
    else if (column === 'chance_of_snow') {
        if (cell.textContent < 25) {
            cell.style.backgroundColor = 'green';
        } else if (cell.textContent < 50) {
            cell.style.backgroundColor = 'yellow';
        } else if (cell.textContent < 75) {
            cell.style.backgroundColor = 'orange';
        } else if (cell.textContent < 100) {
            cell.style.backgroundColor = 'red';
        } else {
            cell.style.backgroundColor = 'purple';
        }
    }
    else if (column === 'visibility_range') {
        if (cell.textContent < 1) {
            cell.style.backgroundColor = 'red';
        } else if (cell.textContent < 2) {
            cell.style.backgroundColor = 'orange';
        } else if (cell.textContent < 3) {
            cell.style.backgroundColor = 'yellow';
        } else if (cell.textContent < 4) {
            cell.style.backgroundColor = 'green';
        } else {
            cell.style.backgroundColor = 'purple';
        }
    }
    else if (column === 'gust_mph') {
        if (cell.textContent < 5) {
            cell.style.backgroundColor = 'green';
        } else if (cell.textContent < 10) {
            cell.style.backgroundColor = 'yellow';
        } else if (cell.textContent < 15) {
            cell.style.backgroundColor = 'orange';
        } else if (cell.textContent < 20) {
            cell.style.backgroundColor = 'red';
        } else {
            cell.style.backgroundColor = 'purple';
        }
    }
    else if (column === 'uv') {
        if (cell.textContent < 3) {
            cell.style.backgroundColor = 'green';
        } else if (cell.textContent < 6) {
            cell.style.backgroundColor = 'yellow';
        } else if (cell.textContent < 8) {
            cell.style.backgroundColor = 'orange';
        } else if (cell.textContent < 11) {
            cell.style.backgroundColor = 'red';
        } else {
            cell.style.backgroundColor = 'purple';
        }
    }
}
