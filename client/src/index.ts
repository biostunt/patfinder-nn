import P5 from 'p5'
import './style.scss'
import {ConnectionManager} from './connection-manager'
import { Square } from './Square';

const squareSize = 8;
const width = 50;

const init = (engine: P5) => {

    const squares: Array<Array<Square>> = [];
    const mouseEvents: Array<Function> =[];


    for (let i = 0; i < width; i++) {
        let temp: Array<Square> = [];
        for (let j = 0; j < width; j++){
            temp.push(new Square(`${j} ${i}`,squareSize * j, squareSize * i, squareSize));
        }
        squares.push(temp);

    }
    engine.setup = () => {
        const canvas = engine.createCanvas(squareSize * width, squareSize * width);
        canvas.parent('#frame');
        squares.forEach(row => row.forEach(el => el.setup(engine, mouseEvents)));
        document.getElementById('check-connection').addEventListener('click', () => {
            ConnectionManager.checkConnection((data: {isAlive: boolean}) => {
                document.getElementById('states').innerText = `connection alive?: ${data.isAlive}`
            })
        })

        document.getElementById('predict-route').addEventListener('click', () => {
            const id = setInterval(() => {
                const curr = Square.getStartSquare().getSquarePosition();
                const finish = Square.getFinishSquare().getSquarePosition();
                ConnectionManager.predictRoute({
                    currX: curr.x,
                    currY: curr.y,
                    finishX: finish.x,
                    finishY: finish.y
                }, (data: { x: number, y: number }) => {
                    if (!Square.updateCurrentPosition(data.x, data.y)) {
                        console.log('success');
                        clearInterval(id);
                    }     
                })
            }, 100);
        })
    }
    engine.draw = () => {
        engine.background('white');
        squares.forEach(row => row.forEach(el => el.draw(engine)));
    }
    engine.mouseClicked = () => mouseEvents.forEach(evt => evt());
}



new P5(init);

