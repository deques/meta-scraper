const mongoose = require("mongoose");

const winnerSchema = new mongoose.Schema({
  name: { type: String, required: true },
  times: { type: Number, required: true },
});

module.exports = mongoose.model("winners", winnerSchema);
