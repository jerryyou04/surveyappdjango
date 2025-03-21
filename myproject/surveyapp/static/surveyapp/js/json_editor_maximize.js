document.addEventListener('DOMContentLoaded', function () {
    // Function to create and add the maximize button
    function addMaximizeButton() {
        const jsonEditor = document.querySelector('.jsoneditor');
        if (!jsonEditor) return;

        // Remove any existing button to avoid duplicates
        let existingButton = document.querySelector('.maximize-btn');
        if (existingButton) existingButton.remove();

        // Create the maximize button
        const maximizeButton = document.createElement('button');
        maximizeButton.textContent = 'Maximize JSON Editor';
        maximizeButton.type = 'button';
        maximizeButton.className = 'maximize-btn';

        // Insert the button above the editor
        jsonEditor.parentElement.insertBefore(maximizeButton, jsonEditor);

        // Add click event listener to toggle full-screen mode
        maximizeButton.addEventListener('click', function () {
            if (jsonEditor.classList.contains('fullscreen')) {
                minimizeEditor(jsonEditor, maximizeButton);
            } else {
                maximizeEditor(jsonEditor, maximizeButton);
            }
        });
    }

    // Function to maximize the editor
    function maximizeEditor(jsonEditor, maximizeButton) {
        jsonEditor.classList.add('fullscreen');
        maximizeButton.textContent = 'Minimize JSON Editor';
        maximizeButton.classList.add('fullscreen-button');
        document.body.appendChild(maximizeButton); // Move button to body for visibility
    }

    // Function to minimize the editor
    function minimizeEditor(jsonEditor, maximizeButton) {
        jsonEditor.classList.remove('fullscreen');
        maximizeButton.textContent = 'Maximize JSON Editor';
        maximizeButton.classList.remove('fullscreen-button');
        jsonEditor.parentElement.insertBefore(maximizeButton, jsonEditor); // Return button to original spot
    }

    // Initial call to add the button
    addMaximizeButton();

    // Event listener to reset the editor and button when switching types
    document.addEventListener('click', function (event) {
        // Only target type-switching buttons by checking their title attribute
        const button = event.target.closest('.jsoneditor-menu button');
        if (button && button.title && button.title.toLowerCase().includes('switch')) {
            // Minimize the editor and reset the button when a type switch is detected
            const jsonEditor = document.querySelector('.jsoneditor');
            const maximizeButton = document.querySelector('.maximize-btn');
            if (jsonEditor && maximizeButton) {
                minimizeEditor(jsonEditor, maximizeButton);
            }
            // Re-add the maximize button after a slight delay to allow the editor to re-render
            setTimeout(addMaximizeButton, 100);
        }
    });
    
});
