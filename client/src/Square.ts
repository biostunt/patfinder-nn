import P5 from 'p5';

export class Square {

    private static entities: Array<Square> = [];
    
    private colors = ['white', 'green', 'red'];
    public colorIndex = 0;
    private static startIndex = 2;
    private static finishIndex = 1;

    private static resetMainColors(index: number) {
        Square.entities.forEach(square =>
            square.colorIndex = square.colorIndex == index ? 0 : square.colorIndex
        );
    }

    public static getStartSquare(): Square {
        const { entities, startIndex } = Square;
        return entities.find(square => square.colorIndex == startIndex);
    }
    public static getFinishSquare(): Square {
        const { entities, finishIndex } = Square;
        return entities.find(square => square.colorIndex == finishIndex);
    }

    public static updateCurrentPosition(x: number, y: number): boolean {
        const finish = Square.getFinishSquare().getSquarePosition();
        Square.resetMainColors(1);
        Square.resetMainColors(2);
        if (finish.x == x && finish.y == y) {
            return false;
        }
        Square.entities.forEach(square => {
            let pos = square.getSquarePosition();
            if (pos.x == x && pos.y == y)
                square.colorIndex = 2;
            if (pos.x == finish.x && pos.y == finish.y)
                square.colorIndex = 1;
        })
        return true;
    }

    constructor(private name: string, private x, private y, private s) {
        Square.entities.push(this);
    }

    public setup(engine: P5, mouseEvents: Array<Function>) {
        mouseEvents.push(this.onMouseClicked.bind(this, engine));
    }

    public draw(engine: P5) {
        engine.fill(this.colors[this.colorIndex]).noStroke().square(this.x, this.y, this.s);
    }

    public getSquarePosition(): { x: number, y: number } {
        let pos = this.name.split(' ');
        return { x: parseInt(pos[0]), y: parseInt(pos[1]) };
    }

    private onMouseClicked(engine: P5) {
        const { mouseX, mouseY } = engine;
        if (this.x < mouseX &&
            this.x + this.s > mouseX &&
            this.y < mouseY &&
            this.y + this.s > mouseY
        ) {
            let colorIndex = this.colorIndex + 1 == this.colors.length ? 0 : this.colorIndex + 1;
            if (colorIndex > 0) {
                Square.resetMainColors(colorIndex);
            }
            this.colorIndex = colorIndex;
        }
    }
}