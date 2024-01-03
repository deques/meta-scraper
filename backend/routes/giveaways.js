const express = require("express");
const router = express.Router();
const Giveaway = require("../models/giveaways");

// Getting all
router.get("/", async (req, res) => {
  try {
    const giveaways = await Giveaway.find()
      .select("-_id")
      .sort({ prizes: "desc" });
    //.limit(25); // Remove this line to see all givers
    res.json(giveaways);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});
// Getting one
router.get("/:id", getGiveaway, (req, res) => {
  res.json(res.giveaway);
});

// Creating one
router.post("/", async (req, res) => {
  const giveaway = new Giveaway({
    name: req.body.name,
    prizes: req.body.prizes,
  });

  try {
    const newGiveaway = await giveaway.save();
    res.status(201).json(newGiveaway);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// Updating one
router.patch("/id", (req, res) => {});

// Deleting one
//router.delete("/:id", getGiveaway, async (req, res) => {});

async function getGiveaway(req, res, next) {
  let giveaway;
  try {
    console.log(req.params.id);
    giveaway = await Giveaway.findById(req.params.id);
    if (giveaway == null) {
      return res.status(404).json({ message: "Cannot find giveaway" });
    }
  } catch (err) {
    return res.status(500).json({ message: err.message });
  }

  res.giveaway = giveaway;
  next();
}

module.exports = router;
