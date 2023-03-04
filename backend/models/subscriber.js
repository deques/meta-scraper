const mongoose = require("mongoose");

const giveawaySchema = new mongoose.Schema({
  name: { type: String, required: true },
  prizes: { type: Number, required: true },
});

module.exports = mongoose.model("users", giveawaySchema);
