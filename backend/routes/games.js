const express = require("express");
const router = express.Router();
const Games = require("../models/games");

// Getting all
router.get("/", async (req, res) => {
  try {
    const games = await Games.find().select("-_id").sort({ times: "desc" });
    //.limit(25); // Remove this line to see all givers
    res.json(games);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

async function getGame(req, res, next) {
  let game;
  try {
    console.log(req.params.id);
    game = await Games.findById(req.params.id);
    if (game == null) {
      return res.status(404).json({ message: "Cannot find game" });
    }
  } catch (err) {
    return res.status(500).json({ message: err.message });
  }

  res.game = game;
  next();
}

module.exports = router;
