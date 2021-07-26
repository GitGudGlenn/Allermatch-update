const path = require("path");
const express = require("express");
const app = express();
const dotenv = require("dotenv");
const connectDB = require("./config/db");
const http = require("http");
const cookieParser = require("cookie-parser");
const cors = require("cors");
const session = require("express-session");

const morgan = require("morgan");
app.use(cookieParser());
app.use(express.json());

// Initialize CORS
app.use(cors({ origin: true, credentials: true }));
app.options("*", cors({ origin: true, credentials: true }));

// Load config
dotenv.config({ path: "./config/config.env" });

// Load DB connection
connectDB();
// Logging function
if (process.env.NODE_ENV === "development") {
  app.use(morgan("dev"));
}

// Routes
app.use("/user", require("./routes/user"));
app.use("/admin", require("./routes/admin"));

// Sessionparser
const sessionParser = session({
  saveUninitialized: false,
  secret: "$eCuRiTy",
  resave: false,
});
app.use(sessionParser);

// Server initialization
const httpServer = http.createServer(app);

const PORT = process.env.PORT || 4000;

httpServer.listen(PORT);
