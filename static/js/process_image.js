console.log('1');
const form = document.querySelector('form');
const resultTable = document.querySelector('#result-table');
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const response = await fetch('/process_image', {
    method: 'POST',
    body: formData
  });
  const result = await response.json();
  console.log(result);
  resultTable.innerHTML = '';
  for (const key of Object.keys(result)) {
    const row = document.createElement('tr');
    const nameCell = document.createElement('td');
    nameCell.textContent = key;
    row.appendChild(nameCell);
    const rgbCell = document.createElement('td');
    rgbCell.textContent = `(${result[key].R}, ${result[key].G}, ${result[key].B})`;
    rgbCell.style.backgroundColor = `rgb(${result[key].R}, ${result[key].G}, ${result[key].B})`;
    row.appendChild(rgbCell);
    resultTable.appendChild(row);
  }
});