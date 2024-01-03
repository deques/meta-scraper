const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  given_games: { type: Number, required: false },
  won_games: { type: Number, required: false },
});

module.exports = mongoose.model("meta_users", userSchema);
