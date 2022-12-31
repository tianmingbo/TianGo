package state;

public enum State {
    //所有状态
    SMALL(0),
    SUPER(1),
    FIRE(2),
    CAPE(3);
    private int value;

    private State(int value) {
        this.value = value;
    }

    public int getValue() {
        return this.value;
    }
}
