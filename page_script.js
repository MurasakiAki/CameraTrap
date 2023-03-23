const picture = document.getElementById('picture');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const note = document.getElementById('note')
const pictures = [
"/pictures/picture0.jpg", 
"/pictures/picture1.jpg", 
"/pictures/picture2.jpg", 
"/pictures/picture3.jpg", 
"/pictures/picture4.jpg", 
"/pictures/picture5.jpg",
"/pictures/picture6.jpg",
"/pictures/picture7.jpg",
"/pictures/picture8.jpg",
"/pictures/picture9.jpg",     
];

const notes = [
"Camera Trap!",
"You can take picture or record video",
"Easy to use!",
"Easy to set-up",
"Using OpenCv library.",
"MotCam = Motion Camera",
"Spy on your neighbours!",
"You can set-up VNC to control remotely",
"Open source!",
"Friendly"
];

//Setting the initial, random picture
function setPicture() {
  const index = Math.floor(Math.random() * pictures.length);
  picture.src = pictures[index];
}

setPicture();

function noteUpdate(index){
    var rotation = Math.floor(Math.random() * 31) - 15;

    note.innerHTML = notes[index];
    note.style.transform = "rotate(" + rotation + "deg)";
}

//Functions for scrolling through pictures
function nextPicture(){
    var full_src = picture.src;
    var src = full_src.replace(/http:\/\/localhost:3000/gm, '');
    console.log(src);
    var current_index = pictures.indexOf(src);
    console.log("Current " + current_index);
    var next_index = current_index + 1;
    if(next_index == 10){
        next_index = 0;
    }
    console.log("Next" + next_index);

    picture.src = pictures[next_index];
    noteUpdate(next_index);
}

function prevPicture(){
    var full_src = picture.src;
    var src = full_src.replace(/http:\/\/localhost:3000/gm, '');
    console.log(src);
    var current_index = pictures.indexOf(src);
    console.log("Current " + current_index);
    var prev_index = current_index - 1;
    if(prev_index == -1){
        prev_index = 9;
    }
    console.log("Next" + prev_index);

    picture.src = pictures[prev_index];
    noteUpdate(prev_index);
}

// Add click handlers to the buttons
prevBtn.addEventListener('click', prevPicture);
nextBtn.addEventListener('click', nextPicture);