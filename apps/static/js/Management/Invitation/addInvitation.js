let fieldCount = 1;

function addFormField() {
    fieldCount++;
    const formGroup = document.createElement('div');
    formGroup.className = 'form-group row';
    formGroup.id = `form-group-${fieldCount}`;

    // Create div group element
    const inputGroup = document.createElement('div');
    inputGroup.className = 'col-sm-12 col-md-4';

    const switchGroup = document.createElement('div');
    switchGroup.className = 'col-sm-12 col-md-3';

    const buttonGroup = document.createElement('div');
    buttonGroup.className = 'col-sm-12 col-md-3';

    const inputLabel = document.createElement('label');
    inputLabel.textContent = '';
    inputLabel.className = 'col-sm-12 col-md-2 col-form-label';
    inputLabel.htmlFor = `galeri-${fieldCount}`;
    
    // Create input field element
    const inputField = document.createElement('input');
    inputField.className = 'form-control-file form-control height-auto';
    inputField.type = 'file';
    inputField.name = `galeri-${fieldCount}`;


    // const sliderSpan = document.createElement('span');
    // sliderSpan.className = 'slider';

    const removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.className = 'btn btn-outline-danger';
    removeButton.textContent = 'Delete';
    removeButton.onclick = () => removeFormField(formGroup.id);

    
    inputGroup.appendChild(inputField);
    switchGroup.appendChild(switchLabel);
    switchGroup.appendChild(switchInput);
    buttonGroup.appendChild(removeButton);
    formGroup.appendChild(inputLabel);
    formGroup.appendChild(inputGroup);
    formGroup.appendChild(switchGroup);
    formGroup.appendChild(buttonGroup);

    // Find the modal-footer div
    // const modalFooter = document.querySelector('.modal-footer');

    document.getElementById('dynamic-form').appendChild(formGroup);

    // Initialize Switchery on the new input
    new Switchery(switchInput, { color: '#7A26C1', size: 'small' });
}

function removeFormField(id) {
    const formGroup = document.getElementById(id);
    if (formGroup) {
        formGroup.remove();
    }
}