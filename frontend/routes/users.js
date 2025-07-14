export var router = express.Router();

import express from "express"

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});
