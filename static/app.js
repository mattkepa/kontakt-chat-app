// References to html elements
const toggleUsersBtn = document.querySelector('.toggle-users-btn');
const hideUsersBtn = document.querySelector('.hide-users-btn');
const usersSection = document.querySelector('.users-container');

//
//
// Binding event listeners to buttons to interact with interface
toggleUsersBtn.addEventListener('click', handleToggleUsers);
hideUsersBtn.addEventListener('click', handleToggleUsers);

function handleToggleUsers(e) {
  usersSection.classList.toggle('active');
}
