document.getElementById('moodForm')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const moodInput = document.getElementById('mood').value;

    fetch('/log_mood', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mood: moodInput }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').innerText = data.message;
        document.getElementById('mood').value = ''; 
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById('refreshButton')?.addEventListener('click', function() {
    fetch('/get_moods')
    .then(response => response.json())
    .then(data => {
        const moodTableBody = document.querySelector('#moodTable tbody');
        moodTableBody.innerHTML = ''; 
        data.forEach(mood => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${mood.mood}</td>
                <td>${mood.sentiment}</td>
                <td>${new Date(mood.timestamp).toLocaleString()}</td>
            `;
            moodTableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

if (document.getElementById('moodTable')) {
    document.getElementById('refreshButton').click(); 
}
