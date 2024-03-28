const outputElem = document.querySelector('#outputs');

function handleDisplay(userData) {
    outputElem.innerHTML = '';

    userData.forEach((data) => {
        const displayDiv = document.createElement('div');
        displayDiv.classList.add('display-div');
        displayDiv.innerHTML = `
            <p>User ID: ${data.id}</p>
            <p>First Name: ${data.firstname}</p>
            <p>Last Name: ${data.lastname}</p>
            <p>Email: ${data.email}</p>
            <p>Age: ${data.age}</p>
            <p>Image: ${data.image}</p>
            <p>Created At: ${data.created_at}</p>
            <p>Bio: ${data.bio}</p>
            <hr>
        `;

        outputElem.appendChild(displayDiv);
    });
}

function handleFetchData() {
    fetch('/api/users')
        .then((res) => res.json())
        .then((data) => handleDisplay(data))
        .catch((error) => {
            console.error(error, 'error while fetching data');
        });
}
