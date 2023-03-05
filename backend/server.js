require("dotenv").config();

const express = require("express");
const app = express();
const cors = require("cors");
const mongoose = require("mongoose");

const PORT = process.env.PORT || 3000;

mongoose.connect(process.env.DATABASE_URL);
const db = mongoose.connection;
db.on("error", (error) => console.log(error));
db.once("open", () => console.log("Connected to the database"));

app.use(cors());
app.use(express.json());

const giveawaysRouter = require("./routes/giveaways");
app.use("/giveaways", giveawaysRouter);

const gamesRouter = require("./routes/games");
app.use("/games", gamesRouter);
app.listen(PORT, () => console.log("Server has started"));
