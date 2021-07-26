/* eslint-disable no-template-curly-in-string */
/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable jsx-a11y/anchor-is-valid */
/* eslint-disable jsx-a11y/alt-text */
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getAllUsers } from "../serverCommunication";

export default function Admin(props) {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    handleGetUsers();
  }, []);

  function handleGetUsers() {
    getAllUsers()
      .then((result) => result.json())
      .then((result) => {
        setUsers(result);
      });
  }

  function deleteUser(){
    console.log("deleted");
    // insert route to delete user
  }

  return (
    <div>
      <span>
        <h1>Admin Panel</h1>
        <p>
          Zometeen nieuwe admins aanmaken, email wijzigen van accounts,
          wachtwoord resets sturen van account en accounts subscipties geven.
          Update deze tekst met korte uitleg.
        </p>
        <table>
          <thead>
            <tr>
              <th>Firstname</th>
              <th>Lastname</th>
              <th>Email</th>
              <th>Subscription</th>
              <th>Accountstatus</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((data) => {
              return (
                <tr key={data._id}>
                  <td>{data.firstname}</td>
                  <td>{data.lastname}</td>
                  <td>{data.email}</td>
                  <td>{data.subscription}</td>
                  <td>{data.accountStatus}</td>
                  <td>
                  <Link to={`/admin/user/${data._id}`}>
                    <i class="material-icons">create</i>
                    </Link>
                    <a class="modal-trigger" data-target="delete"><i class="material-icons">delete_forever</i></a>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </span>
      <div id="delete" class="modal">
        <div class="modal-content">
          <h3 align="center">!WARNING!</h3>
          <h5 align="center">
            You're about to delete this account and everything connected to it. <br />
            Are you abosolutely sure this is what you want to do? <br />
            There is no return when you click agree. <br /> <br />
            No files can be retrieved.
          </h5>
          
        </div>
        <div class="modal-footer">
        <a href="#!" class="modal-close waves-effect waves-green btn-flat">
            Agree
          </a>
        </div>
      </div>
    </div>
  );
}
