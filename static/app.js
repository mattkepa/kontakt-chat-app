// References to html elements
const toggleUsersBtn = document.querySelector('.toggle-users-btn');
const hideUsersBtn = document.querySelector('.hide-users-btn');
const usersSection = document.querySelector('.users-container');
const usersList = document.getElementById('users-list');
const logoutBtn = document.querySelector('.logout-btn');
const messageForm = document.querySelector('.message-form');
const messageInput = document.querySelector('.message-form input');
const messagesList = document.getElementById('messages');

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
    const users_map = res.data;
    users = [];
    for (const key in users_map) {
      users.push(users_map[key]);
    }
    renderUsersList(users);
  } catch (error) {
    console.log(error);
  }
});

//
//
// Initialize socket.io and add event listeners
const socket = io.connect(window.location.origin);

socket.on('connect', () => {
  socket.emit('ehlo', currUser);
});

socket.on('broadcast', message => {
  let msgElem;
  if (!message.author) {
    msgElem = createNotificationElem(message);
  } else {
    msgElem = createMessageElem(message);
  }
  messagesList.appendChild(msgElem);
  msgElem.scrollIntoView({
    behavior: 'smooth',
    block: 'end',
    inline: 'nearest',
  });
});

socket.on('user-disconnected', users_map => {
  users = [];
  for (const key in users_map) {
    users.push(users_map[key]);
  }
  renderUsersList(users);
});

socket.on('user-connected', users_map => {
  users = [];
  for (const key in users_map) {
    users.push(users_map[key]);
  }
  renderUsersList(users);
});

//
//
// Binding event listener to form - send message
messageForm.addEventListener('submit', handleSendMessage);

function handleSendMessage(e) {
  e.preventDefault();
  if (!messageInput.value) {
    console.log('InvalidInput: message cannot be empty');
    return;
  }

  const message = {
    sender_id: currUser.id,
    author: currUser.username,
    content: messageInput.value,
    time: Math.floor(Date.now() / 1000),
  };

  socket.emit('message-sent', message);

  messageInput.value = '';
}

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

function createMessageElem(msg) {
  const elem = document.createElement('li');
  elem.classList.add('message');

  if (msg.sender_id == currUser.id) {
    elem.classList.add('message--sent');
  } else {
    elem.classList.add('message--received');
  }

  const innerHtml = `\
    <span class="message__time">${msg.time}</span>
    <div>
      <span class="message__author">${msg.author}</span>
      <span class="message__text">${msg.content}</span>
    </div>`;

  elem.innerHTML = innerHtml;
  return elem;
}

function createNotificationElem(msg) {
  const elem = document.createElement('li');
  elem.classList.add('message');
  elem.classList.add('message--notification');
  const innerHtml = `\
    <span class="notification__text">${msg.content}</span>`;
  elem.innerHTML = innerHtml;
  return elem;
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
    socket.disconnect();
    currUser = null;
    document.cookie =
      'session=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/; domain=' +
      window.location.hostname +
      ';';
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
