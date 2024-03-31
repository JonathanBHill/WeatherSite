function toggleHamburgerMenu(x) {
    x.classList.toggle("change");
    let sidebar = document.getElementById("hamburger-menu");
    let hideSubMenuTimeOut;
    const submenus = document.querySelectorAll('.sidebar-submenu');
    const submenuArray = Array.from(submenus);
    sidebar.classList.toggle("active");
    const sidebarItems = document.querySelectorAll('.sidebar-item');
    sidebarItems.forEach(function (item) {
        item.addEventListener('mouseover', function() {
            if (item.textContent === 'Home') {
                // console.log('home moused over; no submenu to display');
                // submenu.style.visibility = 'hidden';
            } else if (item.textContent === 'Tables') {
                let submenu = submenuArray[0];
                submenu.innerHTML = '';
                const cities = ["Boulder", "Erie", "Lafayette", "Longmont", "Louisville", "Superior", "Thornton"];
                cities.forEach(function(city) {
                    let h2 = document.createElement("h2");
                    let a = document.createElement("a");
                    a.classList.add("sidebar-item");
                    a.href = "/cities/" + city + '/tables';
                    a.textContent = city;
                    h2.appendChild(a);
                    submenu.appendChild(h2);
                });
                submenu.style.visibility = 'visible';
                submenuArray[1].visibility = 'hidden';
            } else if (item.textContent === 'Visualizations') {
                let submenu = submenuArray[1];
                submenu.innerHTML = '';
                const visualizations = ["Boulder", "Erie", "Lafayette", "Longmont", "Louisville", "Superior", "Thornton"];
                visualizations.forEach(function(visualization) {
                    let h2 = document.createElement("h2");
                    let a = document.createElement("a");
                    a.classList.add("sidebar-item");
                    a.href = "/visualizations/v2/" + visualization + '/visuals';
                    a.textContent = visualization;
                    h2.appendChild(a);
                    submenu.appendChild(h2);
                });
                submenu.style.visibility = 'visible';
                submenuArray[0].visibility = 'hidden';
                // console.log('moused over ' + item.textContent);
            }
        });
        item.addEventListener('mouseout', function() {
            if (item.textContent === 'Tables') {
                submenuArray[0].style.visibility = 'hidden';
            } else if (item.textContent === 'Visualizations') {
                submenuArray[1].style.visibility = 'hidden';
            }
        });
    });

    submenus.forEach(function(submenu) {
        submenu.addEventListener('mouseover', function() {
            submenu.style.visibility = 'visible';
        });
        submenu.addEventListener('mouseout', function() {
            submenu.style.visibility = 'hidden';
        });
    });
}
function toggleArrowMenu(x) {
    x.classList.toggle("change");
    let tableBar = document.getElementById("arrow-menu");
    let tableDiv = document.getElementById("arrow-menu");
    const filterBar = document.getElementById('filter-bar');
    // const arrObj = document.getElementById('ab1');
    // const arrObj2 = document.getElementById('ab2');
    const icon = x.querySelector('i');
    icon.classList.toggle('rotate-chevron');
    const filterBarBtn = document.getElementById('arrow-menu-btn');
    // const currentLeft = parseInt(window.getComputedStyle(arrObj).getPropertyValue('left'), 10);
    tableBar.classList.toggle("active");
    console.log('arrow menu clicked');
    const filterBarHeaders = tableDiv.querySelectorAll('h3');
    const filterList = [
        ['Temperature', 'cb-1-temperature', false],
        ['Is Day', 'cb-2-is-day', false],
        ['Condition', 'cb-3-condition', false],
        ['Wind Speed', 'cb-4-wind-mph', false],
        ['Wind Degree', 'cb-5-wind-degree', false],
        ['Wind Direction', 'cb-6-wind-direction', false],
        ['Pressure', 'cb-7-pressure', false],
        ['Precipitation', 'cb-8-precipitation', false],
        ['Snow', 'cb-9-snow', false],
        ['Humidity', 'cb-10-humidity', false],
        ['Cloud Cover', 'cb-11-cloud', false],
        ['Feels Like', 'cb-12-real-feel', false],
        ['Windchill', 'cb-13-windchill', false],
        ['Heat Index', 'cb-14-heat-index', false],
        ['Dewpoint', 'cb-15-dewpoint', false],
        ['Will it Rain', 'cb-16-will-it-rain', false],
        ['Chance of Rain', 'cb-17-chance-of-rain', false],
        ['Will it Snow', 'cb-18-will-it-snow', false],
        ['Chance of Snow', 'cb-19-chance-of-snow', false],
        ['Visibility', 'cb-20-visibility-range', false],
        ['Gust Speed', 'cb-21-gust-mph', false],
        ['UV Index', 'cb-22-uv', false],
    ];

    // tableDiv.innerHTML = '';
    if (tableBar.classList.contains('active')) {
        filterBarBtn.style.right = '250px';
        // console.log(filterBarHeaders);
        let lbl = document.createElement('label');
        let cbExclude = document.createElement('input');
        cbExclude.type = 'checkbox';
        cbExclude.id = 'cb-exclusion';
        lbl.textContent = 'Exclude';
        cbExclude.checked = true;
        // cb.style.float = 'right';
        lbl.appendChild(cbExclude);
        lbl.classList.add('filter-bar-item');
        tableBar.insertBefore(lbl, filterBarHeaders[1]);
        filterList.forEach(function(filter) {
            // console.log(filter);
            let lbl = document.createElement('label');
            let cb = document.createElement('input');
            lbl.textContent = filter[0];
            cb.id = filter[1];
            cb.checked = filter[2];
            cb.type = 'checkbox';
            cb.addEventListener('change', function() {
                // console.log(`${this.id} is ${this.checked ? 'checked' : 'not checked'}`);
                // toggleColumnVisibility(this.id, this.checked);
                if (cbExclude.checked) {
                    toggleColumnVisibility(this.id, this.checked);
                    console.log(`${this.id} will be ${this.checked ? 'excluded from' : 'included in'} the list`);
                } else {
                    toggleColumnVisibility(this.id, !this.checked);
                    console.log(`${this.id} will be ${this.checked ? 'included in' : 'excluded from'} the list`);
                }
            });
            lbl.appendChild(cb);
            lbl.classList.add('filter-bar-item');
            tableBar.appendChild(lbl);
        });
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        cbExclude.addEventListener('change', function() {
            checkboxes.forEach(function(checkbox) {
                if (checkbox !== cbExclude) {

                checkbox.checked = false;
                toggleColumnVisibility(checkbox.id, !cbExclude.checked);
                }
            });
        });
        // <label class="filter-box-grid-filter"><input type="checkbox" id="cb-1-temp">Temperature</label>-->
    //     let exclusionL = document.createElement('label');
    //     let exclusionCB = document.createElement('input');
    //     exclusionCB.type = 'checkbox';
    //     exclusionCB.id = 'cb-exclusion';
    //     exclusionL.textContent = 'exclusion';
    //     exclusionCB.checked = true;
    //     exclusionCB.style.float = 'right';
    //     exclusionL.appendChild(exclusionCB);
    //     exclusionL.classList.add('filter-bar-item');
    //     tableDiv.appendChild(exclusionL);
    } else {
    //     // arrObj.style.left = 0;
    //     // arrObj2.style.left = 0;
        filterBarBtn.style.right = '20px';
    //     filterBarBtn.style.opacity = 1;
    }
}

function toggleColumnVisibility(columnId, isVisible) {
    // Convert the checkbox id to the corresponding column class
    // This assumes that the checkbox id and the column class are the same
    // You might need to adjust this based on your actual ids and classes
    let columnClass = columnId[5] !== '-' ? `.cb-${columnId.slice(5)}` : `.cb-${columnId.slice(6)}`;
    // let columnClass = columnId.replace('cb-', '');
    // let testing = columnId[5] !== '-' ? columnId[5] : columnId[6];
    // console.log(columnClass);
    // Select all cells in the column
    let cells = document.querySelectorAll(columnClass);
    // console.log(cells);
    // Show or hide the cells based on the checkbox state
    cells.forEach(function(cell) {
        if (isVisible) {
            cell.style.display = 'none';
        } else {
            cell.style.display = '';
        }
    });
}

