function addFormField() {
    const allFormGroups = document.querySelectorAll('.form-group.row[id^="form-group-"]');
    const currentCount = allFormGroups.length;
    const newIndex = currentCount + 1;

    const formGroup = document.createElement('div');
    formGroup.className = 'form-group row';
    formGroup.id = `form-group-${newIndex}`;
    formGroup.setAttribute('data-index', newIndex);

    const inputGroup = document.createElement('div');
    inputGroup.className = 'col-sm-12 col-md-4';

    const switchGroup = document.createElement('div');
    switchGroup.className = 'col-sm-12 col-md-3';

    const buttonGroup = document.createElement('div');
    buttonGroup.className = 'col-sm-12 col-md-3';

    const inputLabel = document.createElement('label');
    inputLabel.textContent = '';
    inputLabel.className = 'col-sm-12 col-md-2 col-form-label';
    inputLabel.htmlFor = `input-fd-${newIndex}`;
    
    const inputField = document.createElement('input');
    inputField.className = 'form-control';
    inputField.type = 'text';
    inputField.name = `format-data-${newIndex}`;
    inputField.placeholder = 'Type Here';

    const switchLabel = document.createElement('label');
    switchLabel.id = 'label-cb-fd';
    switchLabel.textContent = 'Required';
    switchLabel.className = 'col-sm-6 col-form-label';
    switchLabel.htmlFor = `cb-fd-${newIndex}`;

    // const hiddenInput = document.createElement('input');
    // hiddenInput.type = 'hidden';
    // hiddenInput.name = `mandatory-${newIndex}`;
    // hiddenInput.value = '0';

    const switchInput = document.createElement('input');
    switchInput.type = 'checkbox';
    switchInput.className = 'form-control switch-btn';
    switchInput.setAttribute('data-size', 'small');
    switchInput.setAttribute('data-color', '#7A26C1');
    switchInput.setAttribute('data-switchery', 'true');
    switchInput.id = `cb-fd-${newIndex}`;
    switchInput.name = `mandatory-${newIndex}`;
    switchInput.value = '1';

    const removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.className = 'btn btn-outline-danger';
    removeButton.textContent = 'Delete';
    removeButton.setAttribute('data-index', newIndex);
    removeButton.onclick = function() {
        removeFormField(this);
    };

    inputGroup.appendChild(inputField);
    switchGroup.appendChild(switchLabel);
    // switchGroup.appendChild(hiddenInput);
    switchGroup.appendChild(switchInput);
    buttonGroup.appendChild(removeButton);
    formGroup.appendChild(inputLabel);
    formGroup.appendChild(inputGroup);
    formGroup.appendChild(switchGroup);
    formGroup.appendChild(buttonGroup);

    const modalFooter = document.querySelector('.modal-footer');
    document.getElementById('dynamic-form').insertBefore(formGroup, modalFooter);

    new Switchery(switchInput, { color: '#7A26C1', size: 'small' });
}

function removeFormField(button) {
    const index = button.getAttribute('data-index');
    const formGroup = document.querySelector(`.form-group.row[data-index="${index}"]`);
    if (formGroup) {
        formGroup.remove();
    }
}

