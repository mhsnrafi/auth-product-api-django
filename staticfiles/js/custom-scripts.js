document.getElementById('search').addEventListener('input', function (e) {
    const query = e.target.value;
    fetch(`/api/products/search/?search=${query}`)
        .then(response => response.json())
        .then(data => {
            let tableBody = document.getElementById('productTableBody');
            tableBody.innerHTML = ''; // Clear current results
            data.forEach(product => {
                let row = `
                    <tr>
                      <td>${product.id}</td>
                      <td>${product.name}</td>
                      <td>${product.description}</td>
                      <td>${product.price}</td>
                      <td>${product.available_stock}</td>
                      <td>
                        <button class="btn btn-sm btn-primary" onclick="selectProduct(${product.id})">Select</button>
                        <button class="btn btn-sm btn-danger" onclick="reportProduct(${product.id})">Report</button>
                      </td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            });
        });
});

// Function to handle product selection
function selectProduct(productId) {
    fetch(`/api/products/select/${productId}/`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            alert('Product selected!');
        });
}

// Function to handle product reporting
function reportProduct(productId) {
    const reason = prompt('Why are you reporting this product?');
    if (reason) {
        fetch(`/api/products/report/${productId}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ reason })
        }).then(response => response.json())
          .then(data => {
              alert('Product reported!');
              location.reload();  // Refresh the page after reporting
          });
    }
}
