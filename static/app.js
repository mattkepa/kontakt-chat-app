// References to html elements
const toggleUsersBtn = document.querySelector('.toggle-users-btn');
const hideUsersBtn = document.querySelector('.hide-users-btn');
const usersSection = document.querySelector('.users-container');
const usersList = document.getElementById('users-list');
const logoutBtn = document.querySelector('.logout-btn');

//
//
// Global Variable
let currUser = null;

//
//
// Fetch current user active users and display them when page load
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const response = await axios.get('/api/user');
    currUser = response.data;
  } catch (error) {
    console.log(error);
  }

  try {
    const res = await axios.get('/api/users');
    const users = res.data;
    renderUsersList(users);
  } catch (error) {
    console.log(error);
  }
});

//
//
// Create html elements
function createUserElem(usr) {
  const elem = document.createElement('li');
  elem.classList.add('user');
  elem.dataset.uid = usr.id;

  const innerHtml = `\
    <div class="active-indicator">
      <img src="../static/assets/plug-icon.svg" alt="Green plug icon" />
    </div>
    <p class="user__name">${usr.username}</p>`;

  elem.innerHTML = innerHtml;

  return elem;
}

function renderUsersList(users) {
  usersList.innerHTML = '';
  for (const user of users) {
    usrEl = createUserElem(user);
    usersList.appendChild(usrEl);
  }
}

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
    removeUserElem(currUser.id);
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

function removeUserElem(uid) {
  const el = usersList.querySelector(`[data-uid="${uid}"]`);
  if (el) {
    usersList.removeChild(el);
  }
}
