/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable jsx-a11y/anchor-is-valid */
/* eslint-disable jsx-a11y/alt-text */
import React, { useState, useEffect } from "react";
import { searchUserByID, confirmUserChanges } from "../serverCommunication";
import M from "materialize-css";

export default function EditUser(props) {
  const [user, setUser] = useState("");
  const [accountStatus, setAccountStatus] = useState("");
  const [subscription, setSubscription] = useState("");

  useEffect(() => {
    M.AutoInit();
    getUser();
  }, []);

  const getUser = () => {
    let url = window.location.href;
    let id = url.substring(url.lastIndexOf("/") + 1);
    searchUserByID(id).then((response) => {
      setUser(response[0]);
      setAccountStatus(response[0].accountStatus);
      setSubscription(response[0].subscription);
    });
  };

  const updateUser = () => {
    confirmUserChanges(user._id, subscription, accountStatus);
    M.toast({ html: "User info succesfully saved" });
  };

  return (
    <div>
      <span>
        <h1>
          {user.firstname} {user.lastname}
        </h1>
        <h5>Account type</h5>
        <select onChange={(e) => setAccountStatus(e.target.value)}>
          <option value="" disabled selected>
            Unmodified
          </option>
          <option value="User">User</option>
          <option value="Admin">Admin</option>
        </select>

        <h5>Account subscriptie</h5>
        <select onChange={(e) => setSubscription(e.target.value)}>
          <option value="" disabled selected>
            Unmodified
          </option>
          <option value="Unverified">Unverified</option>
          <option value="Verified">Verified</option>
          <option value="Basic">Basic</option>
          <option value="Plus">Plus</option>
        </select>
        <p>
          <label>
            <input type="checkbox" class="filled-in" />
            <span>Reset password</span>
          </label>
        </p>
        <p>
          <label>
            <input type="checkbox" class="filled-in" />
            <span>Reset email</span>
          </label>
        </p>
        <a class="waves-effect waves-light btn" onClick={updateUser}>
          Save
        </a>
      </span>
    </div>
  );
}
