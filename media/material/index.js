const express = require('express')
const app=express()





//----------Writing Data to Database



// const mongoose = require('mongoose');

// const connectionString = "mongodb+srv://mehediahamed:alisjs008@cluster0.zflpd4y.mongodb.net/?retryWrites=true&w=majority";


// (async () => {
//   await mongoose.connect(connectionString);

//   // Create a model and schema for your data
//   const userSchema = new mongoose.Schema({
//     name: { type: String, required: true },
//     email: { type: String, required: true, unique: true },
//     password: { type: String, required: true },
//   });

//   const User = mongoose.model('user', userSchema);

//   // Insert a new document into the collection
//   const user = new User({
//     name: 'John Doe',
//     email: 'john.d0oe@example.com',
//     password: 'password123',
//   });

//   await user.save();

//   // Close the connection to MongoDB
//   await mongoose.disconnect();
// })();




//----------Reading Data from Database


const mongoose = require('mongoose');

const connectionString = "mongodb+srv://mehediahamed:alisjs008@cluster0.zflpd4y.mongodb.net/?retryWrites=true&w=majority";


(async () => {
    await mongoose.connect(connectionString);
  
    // Get the collection you want to read data from
    const collection = mongoose.connection.db.collection('users');
  
    // Find all documents in the collection
    const documents = await collection.find().toArray();
  
    // Do something with the documents
    console.log(documents);
  
    // Close the connection to MongoDB
    await mongoose.disconnect();
  })();


  app.listen(5001,()=>{
    console.log("I an listening to port 5000")
})

app.get("/",(req,res)=>{
    res.send("Home Page")
})
