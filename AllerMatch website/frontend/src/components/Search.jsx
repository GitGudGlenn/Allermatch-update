/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable jsx-a11y/anchor-is-valid */
/* eslint-disable jsx-a11y/alt-text */
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { callPythonFunc } from "../serverCommunication";

export default function Search(props) {

  function handlePython() {
    callPythonFunc()
  }



  return (
    <div>
      <form onSubmit={() => {handlePython()}}>
        <label>
          Name:
          <input type="text" name="name" />
        </label>
        <input type="submit" value="Submit" />
      </form>
    </div>
  );
}