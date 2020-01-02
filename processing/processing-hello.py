#testing processing - didn't work - these are main commands
def rect():
    x = 250, y =200 , w, h 
    return rect
rect()

void setup(){
    #setup for the conditions
    size(500, 400); #w x h canvas
    #I can move the background here to trace the drawing
}

void draw() {
    #run this code forever
    background(0); #black
    stroke(255, 255, 255); #outline rgb
    fill(128);
    ellipse(mouseX+50, mouseY,100,); #variable of a start mouseX/-Y follows the mouse
    rect(250,200,200,10);

}

#conditional statement
if (mousePressed) {
    rect()
} 

#ex
void setup(){
    size(500,400);
    }

void draw() {
    background(0); #black

    stroke(255, 255, 255); #outline rgb
    fill(128);
    ellipse(mouseX+50, mouseY,100,); #variable of a start mouseX/-Y follows the mouse

    if (mousePressed) {
        rect(250,200,100,100);
    } else {
        ellipse(mouseX, 200, 30, 30);
    }
}
