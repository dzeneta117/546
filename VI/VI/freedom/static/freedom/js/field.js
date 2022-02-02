export default class Field{
    constructor(){
        this.empty = true;
        this.color = "";
    }
    isEmpty(){
        return this.empty;
    }
    setIsNotEmpty(){
        this.empty = false;
    }
}