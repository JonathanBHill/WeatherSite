document.querySelectorAll('.forecast-button-box-button').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.forecast-button-box-button').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.forecast-button-box-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById('fc-' + btn.id.slice(-1)).classList.add('active');
        filter_box = document.getElementById('filter-bx')

        // Change the height of the .layout-grid depending on the button clicked
        let layoutGrid = document.querySelector('.layout-grid');
        let mainGrid = document.querySelector('.main-box-grid-area');
        let infoGrid = document.querySelector('.info-box-grid-area');
        let locaGrid = document.querySelector('.loc-box');
        let mainBody = document.querySelector('.main-box-grid-area-body');
        if (btn.id === 'fc-btn-1') { // Daily button
            layoutGrid.style.height = '340px';
            mainGrid.style.height = '290px';
            infoGrid.style.height = '320px';
            filter_box.style.display = 'none';
        } else if (btn.id === 'fc-btn-2') { // Hourly button
            // layoutGrid.style.height = 'minmax(500px, 80vh)';
            // mainGrid.style.height = 'minmax(200px, 500px)';
            // infoGrid.style.height = 'minmax(300px, 600px';
            // mainBody.style.height = 'minmax(200px, 500px)';
            filter_box.style.display = 'grid';
        } else if (btn.id === 'fc-btn-3') { // Astro button
            layoutGrid.style.height = '340px';
            mainGrid.style.height = '290px';
            infoGrid.style.height = '320px';
            filter_box.style.display = 'none';

        }
    });
});
