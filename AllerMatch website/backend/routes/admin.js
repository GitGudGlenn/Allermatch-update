const express = require("express");
const router = express.Router();
const passport = require("passport");
const passportConfig = require("../config/passport");
const JWT = require("jsonwebtoken");
const ObjectID = require("mongodb").ObjectID;
const User = require("../models/User");

const signToken = (userID) => {
  return JWT.sign(
    {
      iss: "Laterlezen",
      sub: userID,
    },
    "LaterLezen",
    {
      expiresIn: "1h",
    }
  );
};

router.put(
  "/user",
  passport.authenticate("jwt", {
    session: false,
  }),
  (req, res) => {
    if ((req.user.accountStatus = "Admin")) {
      User.findOne({ _id: req.body.user_id }, (err, user) => {
        if (err)
          res.status(500).json({
            message: {
              msgBody: "Error has occured",
              msgError: true,
            },
          });
        else {
            console.log("hallo");
          console.log(user);
          console.log("body");
          console.log(req.body);
          user.accountStatus = req.body.accountStatus;
          user.subscription = req.body.subscription;
          user.markModified("subscription")
          user.save();
          
        }
      });
    } else {
      res.status(404);
    }
  }
);

router.get(
  "/user/:id",
  passport.authenticate("jwt", {
    session: false,
  }),
  (req, res) => {
    if ((req.user.accountStatus = "Admin")) {
      User.find(
        { _id: req.params.id },
        {
          firstname: 1,
          lastname: 1,
          email: 1,
          subscription: 1,
          accountStatus: 1,
        },
        (err, user) => {
          if (err)
            res.status(500).json({
              message: {
                msgBody: "Error has occured",
                msgError: true,
              },
            });
          else {
            let hide = user[0].email.split("@")[0].length - 3;
            let r = new RegExp(".{" + hide + "}@", "g");
            user[0].email = user[0].email.replace(r, "*****@");
            res.json(user);
          }
        }
      );
    } else {
      res.status(404);
    }
  }
);

router.get(
  "/users/",
  passport.authenticate("jwt", {
    session: false,
  }),
  (req, res) => {
    if ((req.user.accountStatus = "Admin")) {
      User.find(
        {},
        {
          firstname: 1,
          lastname: 1,
          email: 1,
          subscription: 1,
          accountStatus: 1,
        },
        (err, users) => {
          if (err)
            res.status(500).json({
              message: {
                msgBody: "Error has occured",
                msgError: true,
              },
            });
          else {
            for (let i = 0; i < users.length; i++) {
              const element = users[i];
              let hide = element.email.split("@")[0].length - 3;
              let r = new RegExp(".{" + hide + "}@", "g");
              element.email = element.email.replace(r, "*****@");
            }
            res.json(users);
          }
        }
      );
    } else {
      res.status(404);
    }
  }
);

module.exports = router;
