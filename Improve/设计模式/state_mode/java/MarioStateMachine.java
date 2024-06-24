package state;

public class MarioStateMachine {
    private int score;
    private IMario currentState;

    public MarioStateMachine() {
        //初始化状态为small
        this.score = 0;
        this.currentState = SmallMario.getInstance();
    }

    public void obtainMushRoom() {
        //事件:碰到蘑菇
        this.currentState.obtainMushRoom(this);
    }

    public void obtainCape() {
        //事件
        this.currentState.obtainCape(this);
    }

    public void obtainFireFlower() {
        //事件
        this.currentState.obtainFireFlower(this);
    }

    public void meetMonster() {
        //事件
        this.currentState.meetMonster(this);
    }

    public int getScore() {
        return this.score;
    }

    public void setScore(int score) {
        this.score = score;
    }

    public State getCurrentState() {
        return this.currentState.getName();
    }

    public void setCurrentState(IMario currentState) {
        this.currentState = currentState;
    }
}
