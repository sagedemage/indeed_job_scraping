export var router = express.Router();

import express from "express"
import fetch from "node-fetch"

const backend_url = "http://localhost:8000"

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/about', function(req, res, next) {
  res.render('about', { title: 'About' });
});

router.get('/jobs', async function(req, res, next) {
  const response = await fetch(`${backend_url}/job-data`)
  const data = await response.json();
  res.render('jobs', { title: 'Indeed Jobs', rows: data.rows });
});
