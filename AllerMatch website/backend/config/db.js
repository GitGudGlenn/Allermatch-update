const mongoose = require("mongoose");

const connectDB = async () => {
  try {
    const conn = await mongoose.connect(process.env.MONGO_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
      useFindAndModify: false,
    });
    console.log("db connection established");
  } catch (err) {
    console.log(err);
    process.exit(1);
  }
};
module.exports = connectDB;
