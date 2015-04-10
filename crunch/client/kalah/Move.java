package kalah;

import algorithm.Player;

/**
 * client.crunch.client.kalah.Move:
 * <brief description of class>
 */
public class Move {

    private int[] board;
    private int playerID;

    private Player player;

    public Move(int playerID) {
        super();
        this.playerID = playerID;
        this.player = new Player(playerID);
    }

    public int makeMove(int[] board) {
        this.board = board.clone();

    	return this.player.makePlay(board);
//    	// Implement algorithm
//    	if (this.me == 1) {
//    	    for(int i = 0; i < 6; i++){
//    	        if (this.board[i] > 0)
//    	            return i;
//    	    }
//    	} else {
//    	    for (int i = 7; i < 13; i++) {
//    	        if (this.board[i] > 0)
//    	            return i;
//    	    }
//    	}
//    	return 0;
    }

    public static void main(String[] argv) {

    }
}
