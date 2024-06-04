function fetchModuleDetails(fullModuleName) {
  let parts = fullModuleName.split('/');
  let moduleType = parts[0];
  let moduleName = parts.slice(1).join('/');
  moduleType = moduleType.endsWith('s') ? moduleType.slice(0, -1) : moduleType;

  const url = `/module_details?module_type=${encodeURIComponent(moduleType)}&module_name=${encodeURIComponent(moduleName)}`;

  const modalContentElement = document.getElementById('modalContent');
  const modalNameElement = document.getElementById('modalName');
  modalContentElement.style.opacity = '0.2';
  modalNameElement.style.opacity = '0.2';

  const loadingIndicator = document.getElementById('loading-module-details');
  loadingIndicator.classList.remove('hidden');

  fetch(url)
    .then(response => response.json())
    .then(data => {
      modalContentElement.innerHTML = '';
      modalNameElement.innerHTML = data.name;
      const details = {
        'Module': fullModuleName,
        'Provided by': data.authors.join(', '),
        'Rank': data.rank,
        'Disclosure': data.disclosuredate || 'No record',
        'Description': data.description,
        // 'References': data.references.map(ref => ref.join(': ')).join(', ')
      };

      for (const [key, value] of Object.entries(details)) {
        if (value) {
            if (key === 'Module') {
                modalContentElement.innerHTML += `<p data-full-module-name="${value}"><strong>${key}:</strong> ${value}</p>`;
            } else {
                modalContentElement.innerHTML += `<p><strong>${key}:</strong> ${value}</p>`;
            }
        }
    }

      // Handle 'References' separately to account for possible URLs
      if (data.references && data.references.length > 0) {
        let referencesContent = '<p><strong>References:</strong></p>';
        data.references.forEach(ref => {
          // Assuming ref[1] might be a URL. Adjust as needed.
          if (ref[1].startsWith('http://') || ref[1].startsWith('https://')) {
            referencesContent += `<div><a href="${ref[1]}" target="_blank" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">${ref[0]}: ${ref[1]}</a></div>`;
          } else {
            referencesContent += `<div>${ref[0]}: ${ref[1]}</div>`;
          }
        });
        modalContentElement.innerHTML += referencesContent;
      }



      // Add options if available
      // if (data.options && Object.keys(data.options).length > 0) {
      //     modalContentElement.innerHTML += '<br/><strong>Options:</strong>';
      //     const optionsList = document.createElement('ul');
      //     for (const [optionKey, optionValue] of Object.entries(data.options)) {
      //         if (optionValue && optionValue.hasOwnProperty('desc') && optionValue.desc) { // Check if option description exists
      //             const li = document.createElement('li');
      //             li.textContent = `${optionKey}: ${optionValue.desc}`;
      //             optionsList.appendChild(li);
      //         }
      //     }
      //     modalContentElement.appendChild(optionsList);
      // }

      modalContentElement.style.opacity = '1';
      modalNameElement.style.opacity = '1';
      loadingIndicator.classList.add('hidden');
    })
    .catch(error => {
      console.error('Error fetching module details:', error);
      modalContentElement.style.opacity = '1';
      modalNameElement.style.opacity = '1';
      loadingIndicator.classList.add('hidden');
    });
}
