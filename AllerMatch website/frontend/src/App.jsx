/* eslint-disable jsx-a11y/alt-text */
/* eslint-disable jsx-a11y/anchor-is-valid */
import React from "react";
import { Link, Switch, Route } from "react-router-dom";
import { checkAuthenticated } from "./serverCommunication";

import M from "materialize-css";
import "./materialize.css";
import "./CSS/App.css";

import Footer from "./components/Footer";
import Home from "./components/Home";
import Search from "./components/Search";
import Howto from "./components/Howto";
import About from "./components/About";
import Allergens from "./components/Allergens";
import Login from "./components/Login";
import Logout from "./components/Logout";
import Register from "./components/Register";
import Admin from "./components/Admin";
import Settings from "./components/Settings";
import Subscription from "./components/Subscription";
import EditUser from "./components/EditUser";

import pfp from "./img/default_pfp.png";
import background from "./img/pfp_background.jpg";

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      firstname: "",
      lastname: "",
      email: "",
      users: [],
      logged_in: "",
      accountStatus: "",
      subscription: "",
    };
  }

  componentDidUpdate() {
    M.AutoInit();
  }

  componentDidMount() {
    M.AutoInit();
    checkAuthenticated()
      .then((response) => {
        if (response.isAuthenticated === true) {
          this.handleEmailState(response.user.email);
          this.handleFirstnameState(response.user.firstname);
          this.handleLastnameState(response.user.lastname);
          this.handleAccountStatusState(response.user.accountStatus);
          this.handleSubscriptionState(response.user.subscription)
          this.handleLoginState(true);
        }
      })
      .catch((e) => {});
  }

  handleLoginState(value) {
    this.setState(() => ({
      logged_in: value,
    }));
  }

  handleSubscriptionState(value) {
    this.setState(() => ({
      subscription: value,
    }));
  }

  handleAccountStatus(value) {
    this.setState(() => ({
      accountStatus: value,
    }));
  }

  handleEmailState(value) {
    this.setState(() => ({
      email: value,
    }));
  }

  handleAccountStatusState(value) {
    this.setState(() => ({
      account_Status: value,
    }));
  }

  handleFirstnameState(value) {
    this.setState(() => ({
      firstname: value,
    }));
  }

  handleLastnameState(value) {
    this.setState(() => ({
      lastname: value,
    }));
  }

  render() {
    const setLoginStatus = (c) => this.handleLoginState(c);
    const setEmailState = (c) => this.handleEmailState(c);
    const setFirstnameState = (c) => this.handleFirstnameState(c);
    const setLastnameState = (c) => this.handleLastnameState(c);

    return (
      <div className="page-container">
        <div className="content-wrap">
          <nav>
            <div class="nav-wrapper green darken-4">
              <div class="container">
                <Link to="/">
                  <div class="brand-logo center">
                    AllerMatch<sup>tm</sup>
                  </div>
                </Link>
              </div>
              {this.state.logged_in ? (
                <div>
                  <ul class="right">
                    <li>
                      <Link to="/subscription">Subscription</Link>
                    </li>
                    <li>
                      <Link to="/settings">Settings</Link>
                    </li>

                    <li>
                      <Link to="/logout">Logout</Link>
                    </li>
                  </ul>
                  <a
                    data-target="slide-out"
                    class="sidenav-trigger show-on-large "
                    id="hamburger"
                  >
                    <i class="material-icons">menu</i>
                  </a>
                </div>
              ) : (
                <ul class="right">
                  <li>
                    <Link to="/login">Login</Link>
                  </li>
                  <li>
                    <Link to="/register">Register</Link>
                  </li>
                </ul>
              )}
            </div>
          </nav>
          <ul id="slide-out" class="sidenav sidenav-close">
            <li>
              <div className="user-view">
                <div class="background">
                  <img src={background} />
                </div>
                <a>
                  <img class="circle" src={pfp} />
                </a>
                <a>
                  <span class="white-text name">
                    {this.state.firstname} {this.state.lastname}
                  </span>
                </a>
                <a>
                  <span class="white-text email">{this.state.email}</span>
                </a>
              </div>
            </li>
            <Link to="/search">
              <li>
                <a>
                  <i class="material-icons" id="search">
                    search
                  </i>
                  Find allergens
                </a>
              </li>
            </Link>
            <Link to="/howto">
              <li>
                <a>
                  <i class="material-icons" id="learn">
                    question_answer
                  </i>
                  How to use AllerMatch
                </a>
              </li>
            </Link>
            <Link to="/allergens">
              <li>
                <a>
                  <i class="material-icons" id="learn">
                    article
                  </i>
                  Learn about allergens
                </a>
              </li>
            </Link>
            <Link to="/about">
              <li>
                <a>
                  <i class="material-icons" id="about">
                    business
                  </i>
                  About us
                </a>
              </li>
            </Link>
            {this.state.account_Status === "Admin" ? (
              <Link to="/admin">
                <li>
                  <a>
                    <i class="material-icons" id="about">
                      lock_open
                    </i>
                    Admin panel
                  </a>
                </li>
              </Link>
            ) : (
              <div></div>
            )}
            <div class="inner-content"></div>
          </ul>
          <div class="container">
            <Switch>
              <Route path="/login">
                {this.state.logged_in ? (
                  <Home />
                ) : (
                  <Login
                    appState={this.state}
                    handleLoginState={setLoginStatus}
                    handleEmailState={setEmailState}
                    handleFirstnameState={setFirstnameState}
                    handleLastnameState={setLastnameState}
                  />
                )}
              </Route>
              <Route path="/logout">
                {this.state.logged_in ? (
                  <Logout handleLoginState={setLoginStatus} />
                ) : (
                  <Home />
                )}
              </Route>
              <Route path="/register">
                {this.state.logged_in ? (
                  <Home />
                ) : (
                  <Register
                    handleLoginState={setLoginStatus}
                    handleEmailState={setEmailState}
                    handleFirstnameState={setFirstnameState}
                    handleLastnameState={setLastnameState}
                  />
                )}
              </Route>
              <Route path="/search">
                {this.state.logged_in ? <Search appState={this.state} /> : <Home />}
              </Route>
              <Route path="/about">
                {this.state.logged_in ? <About /> : <Home />}
              </Route>
              <Route path="/settings">
                {this.state.logged_in ? <Settings /> : <Home />}
              </Route>
              <Route path="/subscription">
                {this.state.logged_in ? <Subscription /> : <Home />}
              </Route>
              <Route exact path="/admin">
                {this.state.logged_in &&
                this.state.account_Status === "Admin" ? (
                  <Admin />
                ) : (
                  <Home />
                )}
              </Route>
              <Route path="/admin/user/:id">
                {this.state.logged_in &&
                this.state.account_Status === "Admin" ? (
                  <EditUser/>
                ) : (
                  <div>hi</div>
                )}
              </Route>
              <Route path="/howto">
                {this.state.logged_in ? <Howto /> : <Home />}
              </Route>
              <Route path="/allergens">
                {this.state.logged_in ? <Allergens /> : <Home />}
              </Route>
              <Route path="/">{<Home />}</Route>
            </Switch>
          </div>
        </div>
        <Footer />
      </div>
    );
  }
}
