const mongoose = require("mongoose");

const gamesSchema = new mongoose.Schema({
  name: { type: String, required: true },
  times: { type: Number, required: true },
});

module.exports = mongoose.model("games", gamesSchema);
