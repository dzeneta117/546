import Board from './board.js';
const url = 'http://127.0.0.1:8000';
const SIZE = 10;
const mapErrorsWithSentences = new Map();
let board =new Board();
let gameHasFinished = false;
let novaIgraButtonPressed = false;

function kreirajPorukuZaKraj(whitePoints,blackPoints){
    if(whitePoints > blackPoints) return "Pobednik je beli igrac!";
    else if (whitePoints < blackPoints) return "Pobednik je crni igrac!";
    return "Nereseno!"
}

function getOffset( el ) {
    let rect = el.getBoundingClientRect();
    return {
        left: rect.left + window.pageXOffset,
        top: rect.top + window.pageYOffset,
        width: rect.width || el.offsetWidth,
        height: rect.height || el.offsetHeight
    };
}

function connect(div1, div2, directionFlag, color= "green", thickness = 5) { // draw a line connecting elements
    let off1 = getOffset(div1);
    let off2 = getOffset(div2);
    // bottom right
    let x1 = off1.left;
    let y1 = off1.top;
    // top right
    let x2 = off2.left + off2.width;
    let y2 = off2.top + off2.height;
    //horizontalni pravac
    if(directionFlag==2){
        y1+=off1.height/2;
        y2-=off2.height/2;
    
    }else if(directionFlag==3) // vertikalni pravac
    {
        x1+=off1.width/2;
        x2-=off2.width/2;
    }else if(directionFlag == 4){
        x1+=off1.width;
        x2-= off2.width;
    }

    // distance
    let length = Math.sqrt(((x2-x1) * (x2-x1)) + ((y2-y1) * (y2-y1)));
    // center
    let cx = ((x1 + x2) / 2) - (length / 2);
    let cy = ((y1 + y2) / 2) - (thickness / 2);
    // angle
    let angle = Math.atan2((y1-y2),(x1-x2))*(180/Math.PI);
    // make hr
     let htmlLine = "<div class='htmlLine' style='padding:0px; margin:0px; height:" + thickness + "px; background-color:" + color + "; line-height:1px; position:absolute; left:" + cx + "px; top:" + cy + "px; width:" + length + "px; -moz-transform:rotate(" + angle + "deg); -webkit-transform:rotate(" + angle + "deg); -o-transform:rotate(" + angle + "deg); -ms-transform:rotate(" + angle + "deg); transform:rotate(" + angle + "deg);'> </div>";
    // //
    // // alert(htmlLine);
     document.body.insertAdjacentHTML("beforeend",htmlLine);
}

function drawLinesOverValidCombinations(arrForDrawing){
    arrForDrawing.forEach(el=>{
        // what direction should we draw a green line
        let directionFlag = 1;
        const id1 = el[0];
        const id2 = el[1];
        const veciId = id1 > id2 ? id1 : id2;
        const manjiId = id1 > id2 ? id2 : id1;
        if((veciId-manjiId< 10)  ){
            directionFlag = 2;
        }else if( veciId % 10 == manjiId % 10){
            console.log("Usao 3. flag");
            directionFlag=3;
        }else if(manjiId % 10 > veciId % 10){
            directionFlag = 4;
        }
        const startDiv = document.getElementById(`${el[0]}`);
        const endDiv = document.getElementById(`${el[1]}`);
        connect(startDiv,endDiv,directionFlag);
    });
   
}
const printArr = arr=>arr.forEach(el=>console.log(el))
const finsihGame = (obj={})=>{
     fetch(`${url}/finish`,{
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(obj)
    })
    .then(response=>response.json())
    .then(data=>{
       
        gameHasFinished = true;
        const whitePoints = data['whitePoints'];
        const whiteArr = data['whiteArr'];
        const blackPoints = data['blackPoints'];
        const blackArr = data['blackArr'];
        document.getElementById('skorBeli').innerHTML = whitePoints;
        document.getElementById('skorCrni').innerHTML = blackPoints;
        document.getElementById('krajIgre').style.display='block'
        document.getElementById('rezultatIgre').innerHTML = kreirajPorukuZaKraj(whitePoints,blackPoints);
        document.getElementById('neIgramPotez').style.display='none';
       
        console.log("whiteArr");
        printArr(whiteArr);
        console.log("blackArr");
        printArr(blackArr)

        //return;
        //Moze postojati cetiri slucaja za pravljenje linija
        drawLinesOverValidCombinations(whiteArr);
        drawLinesOverValidCombinations(blackArr);
    })
    .catch(error=>{});
}

function checkErrorCode(errorCode){
    const message=mapErrorsWithSentences.get(errorCode);
        if(errorCode==1 || errorCode==2){
            alert(message);
        }
}
function setMapErrorsWithSentencesValues(){
    mapErrorsWithSentences.set(1,"To polje je vec popunjeno");
    mapErrorsWithSentences.set(2,"Molimo vas odigrajte figuru pored vaseg protivnika.")
}

function createCircle(currentField,i,j,whiteOnMove){
    let circle = document.createElement('div');
    circle.setAttribute('data-i',i);
    circle.setAttribute('data-j',j);
    circle.classList.add('circle');
    currentField.appendChild(circle);
    if(whiteOnMove) circle.style.backgroundColor = 'white';
    else circle.style.backgroundColor = 'black';
}
function addMessageToThirdDiv(whiteMove,x,y){
    let thirdDiv = document.getElementById('thirdDiv');
    let newDiv = document.createElement('div');
    const boja = whiteMove ? 'Beli' : 'Crni';
    newDiv.innerHTML = `${boja} igrac odigrao potez na kordinatama: x= ${x} i y= ${y}`;
    thirdDiv.appendChild(newDiv);
}
//funkcija za igranje poteza kompjutera
function playComputerMove(computerMoves){
    let i = computerMoves[0];
    let j = computerMoves[1];
    let targetField = document.getElementById(`${i*10 + j}`);
    createCircle(targetField,i,j,false);
    addMessageToThirdDiv(false,j,i);
}
function movePlayed(e){
    if(!novaIgraButtonPressed) return;
    if(gameHasFinished) return;
    const currentField =   e.target;
    const i = Number.parseInt(currentField.getAttribute('data-i'));
    const j = Number.parseInt(currentField.getAttribute('data-j'));
    const obj = {i,j};
    fetch(`${url}/play`,
    {
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(obj)
    })
    .then(response=>response.json())
    .then(data=>{
        const errorCode = data['errorCode'];
        const whiteOnMove = data['whiteOnMove'];
        const lastMove = data['lastMove'];
        const gameFinished = data['gameFinished'];
        const computerMoves = data['computerMoves']; // polja koja je odigrao kompjuter
        
        if(errorCode!=0){
            checkErrorCode(errorCode);
            return;
        }

        console.log(computerMoves);
        // if the move is valid
        createCircle(currentField,i,j,whiteOnMove);
        addMessageToThirdDiv(whiteOnMove,j,i);

        //if computer is playing
        if(computerMoves.length>0){
            playComputerMove(computerMoves)
        }
        //if game has finished
        if(gameFinished){
            console.log('Game has finished');
            finsihGame();
        }
        else if(lastMove){
            document.getElementById('neIgramPotez').style.display='block';
        }
    })
    .catch(error=>{
      
    })
}

function drawBoard(){
    const boardDiv = document.getElementById("board");
    const topRow = document.getElementById('topRow');
    const leftRow = document.getElementById('leftRow');
    for(let i=0;i<SIZE;i++){
        const divNumTop = document.createElement('div');
        const divNumLeft = document.createElement('div');
        divNumTop.innerHTML = i;
        divNumLeft.innerHTML = i;
        let boardRow = document.createElement("div");
        for(let j = 0; j< SIZE; j++){
            let boardField= document.createElement("div");
            boardField.classList.add("boardField");
            boardField.setAttribute('data-i',j);
            boardField.setAttribute('data-j',i);
            boardField.id = j * 10 + i;
            boardField.addEventListener('click',movePlayed);
            boardRow.append(boardField);
        }
        boardDiv.appendChild(boardRow);
        topRow.appendChild(divNumTop);
        leftRow.appendChild(divNumLeft);
    }
}
function startNewGame(e){
    console.log("Starting new game...");
    let chosenPlayer = document.querySelector('input[name="nivo"]:checked').id;
    let obj = {chosenPlayer};
    console.log(obj)
    fetch(`${url}/game`,{
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(obj)
    })
    .then(response=>response.json())
    .then(data=>{
        document.querySelectorAll('.htmlLine').forEach(e => e.remove());
        const board = document.getElementById('board');
        board.style.border = 'none';
        Array.from(document.getElementsByClassName('boardField')).forEach(el=>{
            el.style.border = '0.5px black solid';
            el.style.backgroundColor = '#e3900b';
        });
        novaIgraButtonPressed = true;
        console.log(data);
        Array.from(document.getElementsByClassName('boardField')).forEach(el=>{
            el.innerHTML = '';
        });
        document.getElementById('thirdDiv').innerHTML = '';
        document.getElementById('krajIgre').style.display='none'
        gameHasFinished = false;
        //Ova linija sama dodaje figure i omogucava lakse crtanje
        //addTestingData();
    })
    .catch(error=>{

    })
}


document.addEventListener("DOMContentLoaded",()=>{
    setMapErrorsWithSentencesValues();
    const novaIgraButton = document.getElementById('novaIgra');
    const neIgramPotez = document.getElementById('neIgramPotez');
    drawBoard();
    novaIgraButton.addEventListener('click',startNewGame);
    neIgramPotez.addEventListener('click',()=>finsihGame());
});

///////////////////////////////////////////////////////////////////////////////////
//TEST FUNCTIONS ONLY FOR TESTING
async function addTestingData(){
//ONLY FOR TESTING
    let k = 0
    let increment = true
    for(let i = 0; i < 10;i++){
        for(let j = 0; j< 10; j++){
            let pomId = i * 10 + k
            document.getElementById(`${pomId}`).click();
            await sleep(50);
            if(increment) k++;
            else k--;
        }
        if(increment) k--;
        else k++;
        increment = !increment;
    }
}
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
///////////////////////////////////////////////////////////////////////////////////