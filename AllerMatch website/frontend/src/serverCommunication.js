const port = 4000;
const serverHostname = `${window.location.hostname}:${port}`;
const serverFetchBase = `${window.location.protocol}//${serverHostname}`;
const axios = require('axios').default;


export async function callPythonFunc(sequences, orf, length, word, cutoff, database, table, propeptide) {
  const options = {
    url: serverFetchBase+`/user/search`,
    method: 'PUT',
    data: {
      sequences, orf, length, word, cutoff, database, table, propeptide
    },
    withCredentials: true,
    responseType: 'blob',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json;charset=UTF-8'
    }
  };
  
  return axios(options)
}

export async function getAllUsers() {
  const fetchOptions = {
    method: "GET",
    responseType: 'arraybuffer',
    headers: {
      "Content-Type": "application/pdf",
      Accept: 'application/pdf'
    },
    credentials: "include",
    mode: "cors",
  };

  return fetch(serverFetchBase + `/admin/users`, fetchOptions);
}

export async function confirmUserChanges(
  user_id,
  subscription,
  accountStatus,
) {
  const body = {
    user_id,
    subscription,
    accountStatus,
  };
  const fetchOptions = {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    mode: "cors",
    body: JSON.stringify(body),
  };
  return fetch(serverFetchBase + `/admin/user`, fetchOptions);
}

export async function searchUserByID(id) {
  const fetchOptions = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    mode: "cors",
  };

  return fetch(serverFetchBase + `/admin/user/${id}`, fetchOptions).then((response) =>
  response.json()
  );
}

export async function loginUser(email, password) {
  const body = {
    email: email,
    password: password,
  };

  const fetchOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    mode: "cors",
    body: JSON.stringify(body),
  };
  return fetch(serverFetchBase + `/user/login`, fetchOptions).then((response) =>
    response.json()
  );
}

export async function logoutUser() {
  const fetchOptions = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    mode: "cors",
  };
  return fetch(serverFetchBase + `/user/logout`, fetchOptions);
}

export async function registerUser(email, password, firstname, lastname) {
  const body = {
    email: email,
    password: password,
    firstname: firstname,
    lastname: lastname,
  };
  const fetchOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    mode: "cors",
    body: JSON.stringify(body),
  };
  return fetch(serverFetchBase + `/user/register`, fetchOptions);
}

export async function checkAuthenticated() {
  const fetchOptions = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    mode: "cors",
  };
  return fetch(
    serverFetchBase + `/user/authenticated`,
    fetchOptions
  ).then((response) => response.json());
}