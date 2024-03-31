document.addEventListener('DOMContentLoaded', (event) => {
    // * Refresh Functionality
    // Select elements
    const buttonElement = document.getElementById('reset-btn');
    const updateText = document.getElementById('update-time2');

    // Add event listeners
    buttonElement.addEventListener('click', function() {
        let city = window.city;
        let tables = window.table_names;
        fetch(`/refresh/${city}`)
            .then(response => response.json())
            .then(data => {
                hourly_json = data['hourly-table'];
                daily_json = data['daily-table'];
                astro_json = data['astro-table'];

                tables.forEach(function (table) {
                    populateTable(data[table], table);
                });
                console.log(data['location'][0]['localtime'].split(' ')[1]);
                updateText.innerHTML = `<strong>Last Updated:</strong> ${data['location'][0]['localtime'].split(' ')[1]}`;
            });
    });

    // * Filter Functionality
    // const exclusionBehavior = document.getElementById('cb-exclusion');

    // document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
    //     checkbox.addEventListener('change', function() {
    //         console.log(`${this.id} is ${this.checked ? 'checked' : 'not checked'}`);
    //     });
    // });

    // const filterBar = document.getElementById('arrow-menu');
    const filterBarBtn = document.getElementById('arrow-menu-btn');
    // const arrObj = document.getElementById('ab1');
    // const arrObj2 = document.getElementById('ab2');
    // const currentLeft = parseInt(window.getComputedStyle(arrObj).getPropertyValue('left'), 10);
    // filterBarBtn.addEventListener('click', function(event) {
    //     // if (event.target.classList.contains('filter-box-grid-filter')) {
    //     //     console.log('filter box clicked');
    //     // }
    //     // event.stopPropagation();
    //     // filterBarBtn.style.display = 'hidden';
    //     const newLeft = currentLeft - 100;
    //     arrObj.style.left = newLeft + 'px';
    //     arrObj2.style.left = newLeft + 'px';
    //     filterBarBtn.style.opacity = 0;
    // });



    // * Sidebar Functionality
    const sidebar = document.getElementById('hamburger-menu');
    sidebar.addEventListener('click', function(event) {
        event.stopPropagation();
    });
    // exclusionBehavior.addEventListener('change', function() {
    //     if (this.checked) {
    //         console.log('checked');
    //     } else {
    //         console.log('unchecked');
    //     }
    // });
});
