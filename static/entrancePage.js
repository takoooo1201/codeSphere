
        
        // .catch(error => {
        //     console.error('Error:', error);
        //     terminalContent.textContent += '\nServer error, please try again later';
        // });

        





// const terminalContent = document.getElementById('terminal-content');
// const terminalInput = document.getElementById('terminal-input');
// const prompt = document.getElementById('prompt');

// const accounts = {
//     'user1': 'password1',
//     'user2': 'password2'
// };

// function handleInput(event) {
//     if (event.key === 'Enter') {
//         const command = terminalInput.value.trim();
//         terminalInput.value = '';
//         processCommand(command);
//     }
// }

// function processCommand(command) {
//     terminalContent.textContent += '\n' + prompt.textContent + command;

//     if (command === 'guest') {
//         window.location.href = './../home/homePage.html';
//     } else if (command === 'new') {
//         window.location.href = './../register/registerPage.html';
//     } else if (accounts[command]) {
//         terminalContent.textContent += '\nprompt.textContent'+command;
//         prompt.textContent = 'CodeSphere@'+command+':~$ ';
//         terminalInput.onkeypress = handlePasswordInput.bind(null, command);
//     } else {
//         terminalContent.textContent += '\nInvalid account, please enter again';
//         //terminalContent.textContent += '\n' + prompt.textContent;
//         terminalInput.focus();
//     }
// }

// function handlePasswordInput(account, event) {
//     if (event.key === 'Enter') {
//         const password = terminalInput.value.trim();
//         if (password === accounts[account]) {
//             window.location.href = './../home/homePage.html';
//         } else {
//             terminalContent.textContent += '\nInvalid password, enter again';
//             prompt.textContent = 'CodeSphere@entrance:~$ ';
//             terminalInput.onkeypress = handleInput;
//         }
//         terminalInput.value = '';
//     }
// }

// Initialize terminal without adding an extra prompt
