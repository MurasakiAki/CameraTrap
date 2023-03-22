const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000; // Use the provided PORT environment variable or default to 3000

const server = http.createServer((req, res) => {
  // Serve index.html for requests to the root URL
  if (req.url === '/') {
    const filePath = path.join(__dirname, 'index.html');
    const contentType = 'text/html';

    fs.readFile(filePath, (err, content) => {
      if (err) {
        res.writeHead(500);
        res.end(`Error loading ${filePath}: ${err}`);
      } else {
        res.writeHead(200, { 'Content-Type': contentType });
        res.end(content, 'utf-8');
      }
    });
  }
  // Serve style.css and the Streetwear.otf font for requests to those files
  else if (req.url === '/style.css') {
    const filePath = path.join(__dirname, 'style.css');
    const contentType = 'text/css';

    fs.readFile(filePath, (err, content) => {
      if (err) {
        res.writeHead(500);
        res.end(`Error loading ${filePath}: ${err}`);
      } else {
        res.writeHead(200, { 'Content-Type': contentType });
        res.end(content, 'utf-8');
      }
    });
  } else if (req.url === '/Streetwear.otf') {
    const filePath = path.join(__dirname, 'Streetwear.otf');
    const contentType = 'font/opentype';

    fs.readFile(filePath, (err, content) => {
      if (err) {
        res.writeHead(500);
        res.end(`Error loading ${filePath}: ${err}`);
      } else {
        res.writeHead(200, { 'Content-Type': contentType });
        res.end(content);
      }
    });
  } else if (req.url === '/script.js') {
    const filePath = path.join(__dirname, 'script.js');
    const contentType = 'text/javascript';

    fs.readFile(filePath, (err, content) => {
      if (err) {
        res.writeHead(500);
        res.end(`Error loading ${filePath}: ${err}`);
      } else {
        res.writeHead(200, { 'Content-Type': contentType });
        res.end(content, 'utf-8');
      }
    });
  } else if (req.url === '/picture') {
    const pictures = ['picture1', 'picture2', 'picture3', 'picture4']; // Array of picture names
    const randomIndex = Math.floor(Math.random() * pictures.length); // Get a random index into the array
    const filePath = path.join(__dirname, 'pictures', pictures[randomIndex] + '.jpg'); // Build the path to the randomly selected picture
    const contentType = 'image/jpeg';

    fs.readFile(filePath, (err, content) => {
      if (err) {
        res.writeHead(500);
        res.end(`Error loading ${filePath}: ${err}`);
      } else {
        res.writeHead(200, { 'Content-Type': contentType });
        res.end(content);
      }
    });
  } else {
    // Handle other requests
    res.writeHead(404);
    res.end('Page not found');
  }
});

server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});