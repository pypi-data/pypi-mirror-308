document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.project-boxes').innerHTML = '';
    initialize();
});
// This function initializes the searchbar functionality
function startSearchbar() {
    console.log('startSearchbar LOGS');

    const searchBox = document.getElementById('search-input');
    console.log('Search box:', searchBox);
    if (searchBox) {
        searchBox.addEventListener('input', function() {
            const searchText = this.value.toLowerCase();
            console.log('Search text:', searchText);
            const tiles = document.querySelectorAll('.log-tile-container');
            console.log('Log tiles:', tiles);

            tiles.forEach(tile => {
                const content = tile.textContent.toLowerCase();
                console.log('Tile content:', content);
                if (!searchText || (content && content.includes(searchText))) {
                    tile.classList.remove('hidden');
                } else {
                    tile.classList.add('hidden');
                }
            });
        });
    } else {
        console.error('Search box not found');
    }
}


function initialize() {
    //first clear the project-boxes div
    
    window.intervals = []; // or simply use var intervals = [];
    document.querySelector('.project-boxes').innerHTML = '';
    loadLogTilesHeader();
    loadLogTiles();

    let updatetilesinterval = setInterval(updateLogTiles, 100);
    window.intervals = [updatetilesinterval];
    startSearchbar();
};


function loadLogTilesHeader() {
    document.querySelector('.pagetitle').innerHTML = 'Logs';
    //populate the header with the correct elements
    document.querySelector('.in-progress-tasks-section').style.display = 'none';
    document.querySelector('.completed-tasks-section').style.display = 'none';
    document.querySelector('.total-tasks-section').style.display = 'none';

    document.querySelector('.export-logs-button').style.display = 'block';

   

    //force grid view
    document.querySelector('.list-view').style.display = 'none';
    document.querySelector('.grid-view').style.display = 'none';
    document.querySelector('.grid-view').classList.add('active');
    document.querySelector('.project-boxes').classList.remove('jsListView');
    document.querySelector('.project-boxes').classList.add('jsGridView');
}


//this function updates the stats in the tiles based on their I
window.latestTimestamp = null;

function updateLogTiles() {
    // Get the JSON progress data from the server
    fetch('/logs')
        .then(response => response.json())
        .then(data => {
            // Clear the existing log tiles if no logs have been loaded yet
            const logBox = document.querySelector('.log-box');
            if (!window.latestTimestamp) {
                logBox.innerHTML = '';
            }

            // Filter logs to only include new logs
            const newLogs = data.logs.filter(log => !window.latestTimestamp || new Date(log.timestamp) > new Date(window.latestTimestamp));

            // Loop through the new logs array and create a tile for each log entry
            newLogs.forEach(log => {
                const tile = document.createElement('div');
                tile.classList.add('log-tile');
                tile.innerHTML = `
                    <div class="log-tile-container">
                        <div class="log-tile-level ${log.level}"><strong> [${log.level}]</strong> </div>
                        <div class="log-tile-timestamp"> ${log.timestamp} </div>
                        <div class="log-tile-filename-and-line"> ${log.filename}:${log.lineno}</div>
                        <div class="log-tile-message"> ${log.message}</div>
                        
                    </div>
                `;
                logBox.prepend(tile); // Prepend the new log tile to the top
            });

            // Update the latest timestamp
            if (newLogs.length > 0) {
                window.latestTimestamp = newLogs[newLogs.length - 1].timestamp;
            }
        });
}


function loadLogTiles() {
    //select the project-boxes div and add a new div for the log-box
    document.querySelector('.project-boxes').innerHTML = '';
    const projectBoxes = document.querySelector('.project-boxes');
    const logBox = document.createElement('div');
    logBox.classList.add('log-box');
    logBox.id = 'log-box';
    projectBoxes.appendChild(logBox);
}


// Functionality for the download logs button
document.querySelector('.export-logs-button').addEventListener('click', async function() {
    try {
        const response = await fetch('/logs');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const formattedData = JSON.stringify(data, null, 2); // Format JSON data

        const blob = new Blob([formattedData], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'logs.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
});