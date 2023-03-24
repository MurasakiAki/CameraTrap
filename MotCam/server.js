const http = require('http');
const fs = require('fs');
const path = require('path');
const express = require('express');
const app = express();

app.use(express.static('pictures'));

const PORT = process.env.PORT || 22109;

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
        const jsPath = path.join(__dirname, 'page_script.js');
        fs.readFile(jsPath, (jsErr, jsContent) => {
          if (jsErr) {
            res.writeHead(500);
            res.end(`Error loading ${jsPath}: ${jsErr}`);
          } else {
            const modifiedContent = content.toString().replace('</body>', `<script>${jsContent}</script></body>`);
            res.end(modifiedContent);
          }
        });
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
  
  } else if (req.url.startsWith('/pictures/')) {
      const filePath = path.join(__dirname, req.url);
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