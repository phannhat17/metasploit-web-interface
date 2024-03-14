function fetchModuleDetails(fullModuleName, moduleNameNotFull, rank, date) {
    let parts = fullModuleName.split('/');
    let moduleType = parts[0];
    let moduleName = parts.slice(1).join('/');
    moduleType = moduleType.endsWith('s') ? moduleType.slice(0, -1) : moduleType;
    
    const url = `/module_details?module_type=${encodeURIComponent(moduleType)}&module_name=${encodeURIComponent(moduleName)}`;
    fetch(url)
      .then(response => response.json())
      .then(data => {
        const modalNameElement = document.getElementById('modalName');
        modalNameElement.textContent = moduleNameNotFull;
  
        const modalContentElement = document.getElementById('modalContent');
        modalContentElement.innerHTML = `<p><strong>Description:</strong> ${data.description}</p>`;
        modalContentElement.innerHTML += `<p><strong>Rank:</strong> ${rank}</p>`;

        if (date === '') {
          modalContentElement.innerHTML += `<p><strong>Disclosure Date:</strong> No record</p>`;
        } else {
          modalContentElement.innerHTML += `<p><strong>Disclosure Date:</strong> ${date}</p>`;
        }
        modalContentElement.innerHTML += '<br/><strong>Options:</strong>';
        const optionsList = document.createElement('ul');
        data.options.forEach(option => {
          const li = document.createElement('li');
          li.textContent = option;
          optionsList.appendChild(li);
        });
        modalContentElement.appendChild(optionsList);
      })
      .catch(error => console.error('Error fetching module details:', error));
  }

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('searchQuery').addEventListener('keyup', fetchModules);
    fetchModules();
});
