const express = require("express");
const router = express.Router();
const UsersSchema = require("../models/users");

// Getting all
router.get("/", async (req, res) => {
  try {
    const games = await UsersSchema.find()
      .select("-_id")
      .sort({ won_games: "desc" });
    //.limit(25); // Remove this line to see all givers
    res.json(games);
  } catch (err) {
    res.status(500).json({ message: "err.message" });
  }
});

router.get("/:user", getUser, async (req, res) => {
  res.send(res.user);
});

async function getUser(req, res, next) {
  let user;
  try {
    user = await UsersSchema.findOne({ name: req.params.user }); //.findById(req.params.id);
    if (user == null) {
      return res.status(404).json({ message: "Cannot find user" });
    }
  } catch (err) {
    return res.status(500).json({ message: err.message });
  }

  res.user = user;
  next();
}

module.exports = router;
