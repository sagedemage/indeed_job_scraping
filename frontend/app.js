import createError from "http-errors"
import express from "express"
import path from "path"
import {dirname} from "path"
import cookieParser from "cookie-parser";
import logger from "morgan"
import { fileURLToPath } from "url";

import {router as indexRouter} from "./routes/index.js"
import {router as usersRouter} from "./routes/users.js"

export var app = express();

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'hbs');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);

app.use(function (req, res, next) {
  res.status(404).render('page_not_found', { title: '404 - Page Not Found' });
})

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

console.log("Frontend server running at http://localhost:3000")
