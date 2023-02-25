// References to html elements
const toggleUsersBtn = document.querySelector('.toggle-users-btn');
const hideUsersBtn = document.querySelector('.hide-users-btn');
const usersSection = document.querySelector('.users-container');
const logoutBtn = document.querySelector('.logout-btn');

//
//
// Global Variable
let currUser = null;

//
//
// Fetch current user
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const response = await axios.get('/api/user');
    currUser = response.data;
  } catch (error) {
    console.log(error);
  }
});

//
//
// Binding event listeners to buttons to interact with interface
toggleUsersBtn.addEventListener('click', handleToggleUsers);
hideUsersBtn.addEventListener('click', handleToggleUsers);
logoutBtn.addEventListener('click', handleLogout);

function handleToggleUsers(e) {
  usersSection.classList.toggle('active');
}

async function handleLogout(e) {
  try {
    console.log({ uid: currUser.id });
    await axios({
      method: 'post',
      url: '/api/logout',
      data: { uid: currUser.id },
      headers: { 'Content-Type': 'application/json' },
    });
    currUser = null;
    window.location.pathname = '/login';
  } catch (error) {
    console.log(error);
  }
}
