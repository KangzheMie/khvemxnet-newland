const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const app = express();

const db = new sqlite3.Database('blogs.db');

app.get('/getBlog', (req, res) => {
   const blogId = req.query.blog;
   db.get('SELECT FileName FROM MarkdownFiles WHERE id = ?', [blogId], (err, row) => {
       if (err) {
           res.status(500).send('Database error');
       } else {
           res.json(row);
       }
   });
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});