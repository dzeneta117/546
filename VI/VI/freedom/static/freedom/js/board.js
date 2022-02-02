import Field from './field.js'

export default class Board{

    constructor(){
        this.size = 10;
        this.matrix = [];
        this.populateMatrix();
    }
    populateMatrix(){
        for(let i=0;i<this.size;i++){
            this.matrix.push([]);
            for(let j=0;j<this.size;j++){
                this.matrix[i].push(new Field());
            }
        }
    }
    isFieldFree(i,j){
        console.log(i,j)
        return this.matrix[i][j].isEmpty();
    }
    setFieldUsed(i,j){
        this.matrix[i][j].setIsNotEmpty();
    }
    getMatrix(){
        return this.matrix;
    }
}