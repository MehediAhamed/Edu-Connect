const express = require('express')
const mongoose = require('mongoose');
const todoHandler = require('./routeHandler/todoHandler')

const app = express();
app.use(express.json());


// database connection with mongoose
mongoose
    .connect("mongodb+srv://mehediahamed:alisjs008@cluster0.zflpd4y.mongodb.net/?retryWrites=true&w=majority") // return promise
    .then(()=>{console.log('connection successful')})
    .catch((err)=>console.log(err));

// application routes
app.use('/todo', todoHandler);


// default error handler
function errorHandler(err, req, res, next){
    if(res.headerSent){
        return next(err);
    }
    res.status(500).json({error: err});
}

app.listen(3000, ()=>{
    console.log("App is listening at port 3000");
})