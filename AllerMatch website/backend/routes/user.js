const express = require("express");
const router = express.Router();
const passport = require("passport");
const passportConfig = require("../config/passport");
const JWT = require("jsonwebtoken");
const ObjectID = require("mongodb").ObjectID;
const User = require("../models/User");
const { PythonShell } = require("python-shell");

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

router.post("/register", (req, res) => {
  const { email, password, firstname, lastname } = req.body;
  let emailFormat =
    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
  let minPasswordLength = 7;

  if (emailFormat.test(email)) {
    if (password.length > minPasswordLength) {
      User.findOne(
        {
          email,
        },
        (err, user) => {
          if (err)
            res.status(500).json({
              message: {
                msgBody: "Error has occured",
                msgError: true,
              },
            });
          if (user)
            res.status(400).json({
              message: {
                msgBody: "Username already taken",
                msgError: true,
              },
            });
          else {
            const newUser = new User({
              email,
              password,
              firstname,
              lastname,
            });
            let defaultTag = {
              tagName: "/",
              subTags: [],
            };
            newUser.tags = defaultTag;
            newUser.save((err) => {
              if (err)
                res.status(500).json({
                  message: {
                    msgBody: "Error has occured",
                    msgError: true,
                  },
                });
              else
                res.status(200).json({
                  message: {
                    msgBody: "Account sucessfully created",
                    msgError: false,
                  },
                });
            });
          }
        }
      );
    } else {
      res.status(500).json({
        message: {
          msgBody: "Password must be 7 characters or longer.",
          msgError: true,
        },
      });
    }
  } else {
    res.status(500).json({
      message: {
        msgBody: "Wrong email format.",
        msgError: true,
      },
    });
  }
});

router.post(
  "/login",
  passport.authenticate("local", {
    session: false,
  }),
  (req, res) => {
    if (req.isAuthenticated()) {
      const { _id, email, firstname, lastname } = req.user;
      const token = signToken(_id);
      res.cookie("access_token", token, {
        httpOnly: true,
        sameSite: true,
      });
      res.status(200).json({
        isAuthenticated: true,
        email,
        firstname,
        lastname,
        tags: req.user.tags,
        _id,
      });
    }
  }
);

router.get(
  "/logout",
  passport.authenticate("jwt", {
    session: false,
  }),
  (req, res) => {
    res.clearCookie("access_token");
    res.json({
      user: {
        email: "",
      },
      succes: true,
    });
  }
);

router.get(
  "/authenticated",
  passport.authenticate("jwt", {
    session: false,
  }),
  (req, res) => {
    const { firstname, lastname, email, accountStatus } = req.user;
    res.status(200).json({
      isAuthenticated: true,
      user: {
        email,
        firstname,
        lastname,
        accountStatus,
      },
    });
  }
);

// !WIP! Used to call python function
router.put(
  "/search",
  passport.authenticate("jwt", {
    session: false,
  }),
  (req, res) => {
    let options = {
      mode: 'text',
      scriptPath: "/home/glenn/Desktop/allermatch-website-revamp/AllerMatch-website/backend/CommandTool",
      pythonOptions: ['-u'], // get print results in real-time
      args: ['-i /home/glenn/Desktop/allermatch-website-revamp/AllerMatch-website/backend/CommandTool/allergens/data/db/AllermatchDB_2019/test.fasta'], //An argument which can be accessed in the script using sys.argv[1]
    };

    PythonShell.run("app.py", options, function (err, result) {
      if (err) throw err;
      // result is an array consisting of messages collected
      //during execution of script.
    });

    console.log("response");
    res.status(201);
  }
);

// !WIP! Used to update account info like name/email/password
router.put(
  "/update",
  passport.authenticate("jwt", {
    session: false,
  }),
  (req, res) => {
    res.status(201);
  }
);

// !WIP! Used to reset password via emailed link
router.put(
  "/reset/:token",
  passport.authenticate("jwt", {
    session: false,
  }),
  (req, res) => {
    if ((req.params.token = 0)) {
      // send email
    } else {
      // if token = 1 => abort
      // lookup token in db
      // get password from data
      // hash it and replace in db
    }
    res.status(201);
  }
);

// !WIP! Used to verify emailaddress of user by using secret token
router.put(
  "/verify",
  passport.authenticate("jwt", {
    session: false,
  }),
  (req, res) => {
    // if resettoken = 1 => abort

    res.status(201);
  }
);

module.exports = router;
